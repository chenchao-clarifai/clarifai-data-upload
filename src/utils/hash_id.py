from typing import Any


def proto_to_hash(proto: Any) -> str:
    return hex(hash(str(proto)))
