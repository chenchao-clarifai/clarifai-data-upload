from typing import Any


def proto_to_hash(proto: Any) -> str:
    return hex(abs(hash(str(proto))))
