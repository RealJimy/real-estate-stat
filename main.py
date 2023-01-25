#!/usr/bin/env python3

import time
from real_estate_stat.decorator import make_table
from real_estate_stat.real_estate_stat import RealEstateStat
from real_estate_stat.client_factory import get_client


start = time.time()

# Get client to make requests to API
cli = get_client(
    'data.ct.gov',      # Dataset domain, required
    '5mzw-sjtu',        # Dataset ID, required
    name='async',       # Name of API client, required. Options: sync|async, default: async
    # token='...',      # app_token for https://dev.socrata.com/foundry/data.ct.gov/5mzw-sjtu, optional
    timeout=20,         # Requests timeout, optional, default 10
)

# Statictics object
stat = RealEstateStat(client=cli)

# Decorator to beautify console output
decorate = make_table(columns=2)

# Collect statistics for range of years (all arguments are optional)
result = stat.collect(
    from_year=2001,
    to_year=2010,
    post_processor=decorate
)

print(result)

end = time.time()
print(f'Time: {end-start:.2f} sec')