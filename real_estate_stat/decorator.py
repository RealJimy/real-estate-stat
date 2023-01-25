from tabulate import tabulate


def make_table(columns=2):
    """
    Decorate console output
    """
    def inner(data):
        if not data:
            print("No data received")
            return None

        # User freindly table headers
        titles = {
            'top_sales_ratio': 'Sales ratio',
            'top_volume_number': 'Number of deals',
            'top_volume_usd': 'Money',
        }

        data_len = len(data)

        # Number of columns 
        column_cnt = min(columns, data_len)

        column_keys = list(data[0].keys())

        # Calculate number of rows
        row_cnt = data_len
        if column_cnt > 1:
            row_cnt = int(data_len / column_cnt)
            if data_len % column_cnt != 0:
                row_cnt += 1

        table_rows = []
        # The first row contains keys for the table header
        table_rows.append(column_keys * column_cnt)

        # Fill the table
        for i, item in enumerate(data):

            row_number = i % row_cnt + 1

            if row_number >= len(table_rows):
                table_rows.append([])

            for key in column_keys:
                if key in item:

                    # Format cell
                    value = item[key]
                    if key != 'year':
                        value = 'Error' if 'errors' in value else '\n'.join(value['towns'])
                    table_rows[row_number].append(value)
                else:
                    table_rows[row_number].append('No data')

        # Replce keys to user friendly header 
        table_rows[0] = map(lambda x: x.capitalize() if x == 'year' else titles[x], table_rows[0])

        # Format table and return
        return tabulate(table_rows, tablefmt="fancy_grid")
            
    return inner
