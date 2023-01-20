from requests.exceptions import HTTPError
from requests.exceptions import ReadTimeout

# Number of tries in case of HTTP error
_DEFAULT_TRIES = 2


class SodapyWrapper():

    def __init__(
        self,
        client,
        id,
        tries=_DEFAULT_TRIES
    ):
        """
        Init Socrata client from 'sodapy' package
        """
        self.client = client
        self.dataset_id = id
        self.tries = tries
    

    def collect_data(self, request_list):
        """
        Send requests by list. Can retry in case of HTTP errors
        Return list of requests with responses or errors
        """
        results = []
        while request_list:
            request = request_list.pop(0)
            request_params = request.get('params', {})

            if not request_params:
                raise Exception(f'Request params required, got structure {request}')

            try:
                # Send request using Socrata client
                request['response_data'] = self.client.get(
                    self.dataset_id, 
                    **request_params
                )

            except (HTTPError, ReadTimeout) as e:

                # Count tries and save error message after HTTP error
                request['tries'] = request.get('tries', 0) + 1
                if e.response:
                    error_msg = f'HTTP error {e.response.status_code}: {e.response.text}'
                else:
                    error_msg = f'Connection error: {e}'

                request.setdefault('errors', []).append(error_msg)

                # If can retry, add request back to queue
                if self.tries > request['tries']:
                    request_list.append(request)
                    continue

            except Exception as e:
                raise Exception(f'sodapy error: {e}')

            results.append(request)

        return results
