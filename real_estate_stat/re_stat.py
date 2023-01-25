from real_estate_stat.real_estate_stat import RealEstateStat
from real_estate_stat.client_factory import get_client
from real_estate_stat.decorator import make_table

import argparse
import time


def main():
    DATASET_HOST = 'data.ct.gov'
    DATASET_ID = '5mzw-sjtu'

    argParser = argparse.ArgumentParser(prog = 'Real Estate Statistics')
    argParser.add_argument("-m", "--mode", help="requests mode", default="async", choices=["sync", "async"])
    argParser.add_argument("-y1", "--from-year", type=int, help="the first year of requesting data")
    argParser.add_argument("-y2", "--to-year", type=int, help="the last year of requesting data")
    argParser.add_argument("-tk", "--token", help="Socrata app_token")
    argParser.add_argument("-l", "--limit", type=int, help="number of towns in response")
    argParser.add_argument("-to", "--timeout", type=int, help="timeout for API requests")
    argParser.add_argument("-d", "--decorate", help="flag for switch off decoration", action='store_false')
    argParser.add_argument("-b", "--benchmark", help="hide time duration", action='store_false')

    args = argParser.parse_args()

    if args.benchmark:
        start = time.time()

    # Get client to make requests to API
    client_params = {
        'name': args.mode,
    }

    if args.token:
        client_params['token'] = args.token
    if args.timeout:
        client_params['timeout'] = args.timeout


    cli = get_client(
        DATASET_HOST,      # Dataset domain, required
        DATASET_ID,        # Dataset ID, required
        **client_params,
    )

    # Statictics object
    stat = RealEstateStat(client=cli)

    collect_params = {}
    if args.from_year:
        collect_params['from_year'] = args.from_year
    if args.from_year:
        collect_params['to_year'] = args.to_year
    decorate = None
    if args.decorate:
        decorate = make_table(columns=2)
    if args.limit:
        collect_params['limit'] = args.limit


    # Collect statistics for range of years (all arguments are optional)
    print(stat.collect(**collect_params, post_processor=decorate))

    if args.benchmark:
        end = time.time()
        print(f'Time: {end-start:.2f} sec')

if __name__ == '__main__':
    main()