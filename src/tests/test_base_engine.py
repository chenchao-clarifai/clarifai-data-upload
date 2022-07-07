from ..engine import base


def test_channels():
    dev = base._EngineBase("dev", "xyz")
    staging = base._EngineBase("staging", "xyz")
    prod = base._EngineBase("prod", "xyz")
    localhost = base._EngineBase("localhost:3000", "xyz")
    assert dev.base_url == base.CHANNEL_URLS["dev"]
    assert staging.base_url == base.CHANNEL_URLS["staging"]
    assert prod.base_url == base.CHANNEL_URLS["prod"]
    assert localhost.base_url == "localhost:3000"


def test_repr():
    prod = base._EngineBase("prod", "xyz")
    print(prod)


def test_info():
    prod = base._EngineBase("prod", "xyz")
    assert isinstance(prod.info(), dict)


def test_context():
    with base._EngineBase("prod", "xyz") as prod:
        prod()
        print("nothing")
