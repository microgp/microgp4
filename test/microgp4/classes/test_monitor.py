import pytest
import warnings
from microgp4.classes import failure_rate

@failure_rate
def always_succeeds():
    return True

@failure_rate
def always_fails():
    return False

def test_failure_rate():
    for _ in range(100):
        assert always_succeeds()

    with pytest.warns(RuntimeWarning):
        for _ in range(100):
            assert not always_fails()

    @failure_rate
    def raises_exception():
        raise ValueError("This is an exception")

    with pytest.raises(ValueError):
        raises_exception()
