# pylint: disable=R0401
from dataclasses import dataclass
from typing import Optional, List

from json_urley import JsonUrleyError


@dataclass
class PathElement:
    key: str
    type_hint: Optional[str] = None

    def get_typed_value(self, value: str):
        type_hint = self.type_hint
        if type_hint:
            fn = _TYPE_HINTS.get(type_hint)
            if not fn:
                raise JsonUrleyError(f"invalid_type_hint:{type_hint}")
            return fn(value)
        return _get_typed_value(value)


def parse_path(path: str) -> List[PathElement]:
    elements = []
    current_index = 0
    current_key = []
    while True:
        next_tilda = _next_index_of(path, "~", current_index)
        next_dot = _next_index_of(path, ".", current_index)
        if next_tilda < next_dot:
            if path[next_tilda + 1] in ("~", "."):
                current_key.append(path[current_index:next_tilda])
                current_key.append(path[next_tilda + 1])
                current_index = next_tilda + 2
            else:
                current_key.append(path[current_index:next_tilda])
                elements.append(
                    PathElement(
                        key="".join(current_key),
                        type_hint=path[next_tilda + 1 : next_dot],
                    )
                )
                current_key.clear()
                current_index = next_dot + 1
        elif next_dot < next_tilda:
            current_key.append(path[current_index:next_dot])
            elements.append(PathElement("".join(current_key)))
            current_key.clear()
            current_index = next_dot + 1
        else:
            if current_index < len(path):
                current_key.append(path[current_index:])
            if current_key:
                elements.append(PathElement("".join(current_key)))
            return elements


def _next_index_of(path: str, sub: str, from_index: int):
    try:
        return path.index(sub, from_index)
    except ValueError:
        return len(path)


def _s(value: str):
    return value


def _f(value: str):
    try:
        return float(value)
    except ValueError as exc:
        raise JsonUrleyError("not_float:{value}") from exc


def _i(value: str):
    try:
        return int(value)
    except ValueError as exc:
        raise JsonUrleyError("not_int:{value}") from exc


def _b(value: str):
    value = value.lower()
    if value in ("true", "1"):
        return True
    if value in ("false", "0"):
        return False
    raise JsonUrleyError(f"not_boolean:{value}")


def _n(value: str):
    if value:
        raise JsonUrleyError(f"not_empty:{value}")


def _a(value: str):
    if value:
        raise JsonUrleyError(f"not_empty:{value}")
    return []


def _o(value: str):
    if value:
        raise JsonUrleyError(f"not_empty:{value}")
    return {}


def _get_typed_value(value: str):
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value


_TYPE_HINTS = {"s": _s, "f": _f, "i": _i, "b": _b, "n": _n, "a": _a, "o": _o}
