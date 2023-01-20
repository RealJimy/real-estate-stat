from tabulate import tabulate


def make_table(cols=2):
    """
    Decorate console output
    """
    def inner(data):
        if not data:
            print("No data received")
            return None

        titles = {
            'top_sales_ratio': 'Sales ratio',
            'top_volume_number': 'Number of deals',
            'top_volume_usd': 'Money',
        }

        cols_loc = min(cols, len(data))
        keys_ = list(data[0].keys())

        rows_cnt = len(data)
        if cols_loc > 1:
            rows_cnt = int(len(data) / cols_loc)
            if len(data) % cols_loc != 0:
                rows_cnt += 1

        result = []
        result.append(keys_ * cols_loc)

        for i, item in enumerate(data):
            i_ = i % rows_cnt + 1
            if i_ >= len(result):
                result.append([])

            for key in keys_:
                if key in item:
                    result[i_].append(item[key] if key == 'year' else '\n'.join('Error' if 'errors' in item[key] else item[key]['towns']))
                else:
                    result[i_].append('???')

        result[0] = map(lambda x: x.capitalize() if x == 'year' else titles[x], result[0])
        return tabulate(result, tablefmt="fancy_grid")
            
    return inner
