import pytest
from real_estate_stat.sodapy_wrapper import SodapyWrapper
from requests.exceptions import HTTPError

def raise_(ex):
    raise ex

def mocked_client_HTTP_error(*_):
    return None
mocked_client_HTTP_error.get = lambda *args, **kwargs: raise_(HTTPError()) 

def mocked_client_exception(*_):
    return None
mocked_client_exception.get = lambda *args, **kwargs: raise_(Exception("Error text")) 


def test_tries():
    receiver = SodapyWrapper(mocked_client_HTTP_error, '', tries=3)
    result = receiver.collect_data([{'params': {'a': 1}}])
    assert len(result) == 1
    resp = result[0]
    assert resp.get('tries', 0) == 3
    assert len(resp.get('errors', [])) == 3


def test_exception():
    receiver = SodapyWrapper(mocked_client_exception, '', tries=3)
    with pytest.raises(Exception) as e:
        receiver.collect_data([{'params': {'a': 1}}])
    assert str(e.value) == "sodapy error: Error text"
