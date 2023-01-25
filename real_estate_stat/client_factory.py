from real_estate_stat.sodapy_wrapper import SodapyWrapper
from real_estate_stat.async_socrata import AsyncSocrata
from sodapy import Socrata


def get_client(*args, name="async", **kwargs):
    """
    Instance and return client based on 'name' parameter
    """
    if name == 'async':
        return _async_socrata(*args, **kwargs)
    elif name == 'sync':
        return _sync_socrata(*args, **kwargs)
    else:
        raise Exception(f'Client with name "{name}" not implemented')


def _async_socrata(host, id, token=None, timeout=None):
    """
    Asynchronous receiver based on aiohttp
    """
    params = {
        'host': host,
        'id': id,
    }
    if token:
        params['token'] = token
    if timeout:
        params['timeout'] = timeout

    return AsyncSocrata(**params)


def _sync_socrata(host, id, token=None, timeout=None):
    """
    Synchronous receiver based on Socrata client
    """
    params = {}
    if timeout:
        params['timeout'] = timeout

    socrata_client = Socrata(host, token, **params)
    return SodapyWrapper(socrata_client, id)

