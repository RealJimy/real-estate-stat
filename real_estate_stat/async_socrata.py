import aiohttp
import asyncio
from asgiref import sync
import urllib.parse

# HTTP Requests timout
_DEFAULT_TIMEOUT = 10

_DEFAULT_API_PATH = '/resource/'


class AsyncSocrata:

    # HTTP Headers
    headers = {}

    def __init__(self, host, id, token=None, timeout=_DEFAULT_TIMEOUT):
        self._api_url = f'https://{host}{_DEFAULT_API_PATH}{id}.json'
        if token:
            self.headers['X-App-Token'] = token
        self.timeout = timeout


    def collect_data(self, params_list):
        """
        Prepare list of URL to request all data and send them for async processing
        """
        for params in params_list:
            query_params = urllib.parse.urlencode(self._prep_params(**params['params']))
            params['url'] = f'{self._api_url}?{query_params}'
        return self.async_get_all(params_list)


    def async_get_all(self, request_list):
        """
        Performs asynchronous requests for all urls in the list
        """
        async def get_all(headers, tasks, timeout):

            session_timeout = aiohttp.ClientTimeout(total=timeout)
            async with aiohttp.ClientSession(headers=headers, timeout=session_timeout) as session:

                async def fetch(task):

                    async with session.get(task.get('url')) as response:
                        task['response_data'] = await response.json()
                        return task

                return await asyncio.gather(*[fetch(task) for task in tasks])

        return sync.async_to_sync(get_all)(
            headers=self.headers,
            tasks=request_list,
            timeout=self.timeout
        )


    def _prep_params(self, **kwargs):
        """
        Prepeare query string parameters (implementation was copied from sodapy)
        """
        # SoQL parameters
        params = {
            "$select": kwargs.pop("select", None),
            "$where": kwargs.pop("where", None),
            "$order": kwargs.pop("order", None),
            "$group": kwargs.pop("group", None),
            "$limit": kwargs.pop("limit", None),
            "$offset": kwargs.pop("offset", None),
            "$q": kwargs.pop("q", None),
            "$query": kwargs.pop("query", None),
            "$$exclude_system_fields": kwargs.pop("exclude_system_fields", None),
        }
        # Additional parameters, such as field names
        params.update(kwargs)
        
        def clear_empty_values(args):
            """
            Scrap junk data from a dict.
            """
            result = {}
            for param in args:
                if args[param] is not None:
                    result[param] = args[param]
            return result

        return clear_empty_values(params)
