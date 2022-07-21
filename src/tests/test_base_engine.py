from ..engine import base


class _UnittestEngine(base._EngineBase):

    _has_annotation = True

    def to_proto(self, *args, **kwargs):
        return self.current_count


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


def test_has_annotation():
    f = base._EngineBase("prod", "xyz")
    assert f._has_annotation is False

    _UnittestEngine("prod", "xyz")
    assert _UnittestEngine._has_annotation is True


def test_count():
    up = _UnittestEngine("abc", "xyz", batch_size=200, current_count=3)
    assert up.current_count == 3
    for i in range(10):
        up(key="nothing")
        assert up.current_count == i + 1 + 3
