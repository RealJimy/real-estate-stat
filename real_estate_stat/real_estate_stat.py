class RealEstateStat:

    _MIN_YEAR = 2001
    _MAX_YEAR = 2020
    _RESULT_LIMIT = 10

    _OPTIONS = {
        # the highest sales ratio
        'top_sales_ratio': {
            'select': 'town',
            'group': 'town',
            'order': 'avg(salesratio::number) DESC',
        },

        # the highest volume of sales, number of deals
        'top_volume_number': {
            'select': 'town',
            'group': 'town',
            'order': 'count(serialnumber) DESC',
        },

        # the highest volume of sales, amount of money
        'top_volume_usd': {
            'select': 'town',
            'group': 'town',
            'order': 'sum(saleamount) DESC',
        },
    }

    get_town = lambda x: x.get('town')

    _MAPPINGS = {
        'top_sales_ratio': get_town,
        'top_volume_number': get_town,
        'top_volume_usd': get_town,
    }


    def __init__(self, client):
        self.client = client


    def collect(
        self,
        from_year=_MIN_YEAR,
        to_year=_MAX_YEAR,
        names=None,
        limit=_RESULT_LIMIT,
        post_processor=None
    ):
        # Validate years
        if from_year < self._MIN_YEAR or from_year > self._MAX_YEAR:
            raise Exception(
                f"Year expected between {self._MIN_YEAR} and {self._MAX_YEAR}, got {from_year}"
            )
        if to_year < self._MIN_YEAR or to_year > self._MAX_YEAR:
            raise Exception(
                f"Year expected between {self._MIN_YEAR} and {self._MAX_YEAR}, got {to_year}"
            )
        if to_year < from_year:
            raise Exception(f"Incorrect range of years: {from_year} - {to_year}")

        # Prepare list of options to request data
        options = []
        if names:
            for name in names:
                if name not in self._OPTIONS:
                    raise Exception(f'Unexpected option: {name}')
                options.append(name)
        else:
            options = self._OPTIONS.keys()

        # Prepare set of parameters for each pair of year and option
        request_params = []
        for year in range(from_year, to_year + 1):
            for option in options:
                request_params.append({
                    'params': self._prepare_options(option, year, limit),
                    'key': self._format_key(year, option),
                })

        # Request data
        responses = self.client.collect_data(request_params)

        # Map response
        result = self._process_responses(responses, from_year, to_year)

        # function to convert/save/print results 
        if post_processor:
            return post_processor(result)

        return result


    def _process_responses(self, responses, from_year, to_year):
        result = [None] * (to_year - from_year + 1)

        responses.sort(key=lambda x: x['key'])

        # Process data from responses
        for item in responses:
            year, option = self._parse_key(item.get('key'))
            index = year - from_year

            if not result[index]:
                result[index] = {}
            
            result[index]['year'] = year
            result[index][option] = {
                'towns': list(map(self._MAPPINGS[option], item['response_data']))
            }
            if 'errors' in item:
                result[index][option]['errors'] = item['errors']

        return result


    def _prepare_options(self, option, year, limit):
        data = {
            'listyear': year,
            'limit': limit,
        }
        data.update(self._OPTIONS[option])
        return data


    def _format_key(self, year, option):
        return f'{year}_{option}'

    def _parse_key(self, key):
        year, option = key.split('_', 1)
        return (int(year), option)

