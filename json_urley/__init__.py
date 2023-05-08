from decimal import Decimal
from typing import Dict, List, Iterator, Tuple
from urllib.parse import urlencode, parse_qsl

from json_urley.json_urley_error import JsonUrleyError
from json_urley._path_element import parse_path, PathElement


def query_str_to_json_obj(query: str) -> Dict:
    params = parse_qsl(query, keep_blank_values=True)
    result = query_params_to_json_obj(params)
    return result


def query_params_to_json_obj(params: List[Tuple[str, str]]) -> Dict:
    result = {}
    for key, value in params:
        path = parse_path(key)
        _append_param(path, value, result)
    return result


def _append_param(path: List[PathElement], value: str, result: Dict):
    parent = result
    for path_element_ in path[:-1]:
        if path_element_.type_hint not in (None, "a"):
            raise JsonUrleyError(f"invalid_element:{path_element_}")
        if isinstance(parent, list):
            parent = _append_param_to_list(path_element_, parent)
        elif isinstance(parent, dict):
            parent = _append_param_to_dict(path_element_, parent)
        else:
            raise JsonUrleyError(f"path_mismatch:{path_element_}")

    path_element_ = path[-1]
    typed_value = path_element_.get_typed_value(value)
    if isinstance(parent, list):
        if path_element_.key not in ("e", "n"):
            raise JsonUrleyError(f"path_mismatch:{path_element_}")
        parent.append(typed_value)
    elif not isinstance(parent, dict):
        raise JsonUrleyError(f"path_mismatch:{path_element_}")
    elif path_element_.key in parent:
        existing_value = parent[path_element_.key]
        if isinstance(existing_value, list):
            existing_value.append(typed_value)
        else:
            parent[path_element_.key] = [existing_value, typed_value]
    else:
        parent[path_element_.key] = typed_value


def _append_param_to_list(path_element_: PathElement, parent: List):
    if path_element_.key == "e" and parent:
        return parent[-1]
    if path_element_.key in ("e", "n"):
        child = [] if path_element_.type_hint == "a" else {}
        parent.append(child)
        return child
    raise JsonUrleyError(f"path_mismatch:{path_element_}")


def _append_param_to_dict(path_element_: PathElement, parent: Dict):
    key = path_element_.key
    if key in parent:
        return parent[key]
    child = [] if path_element_.type_hint == "a" else {}
    parent[key] = child
    return child


def json_obj_to_query_params(json_obj: Dict) -> List[Tuple[str, str]]:
    if json_obj:
        result = list(_generate_query_params(json_obj, [], False))
    else:
        result = []
    return result


def json_obj_to_query_str(json_obj: Dict) -> str:
    query_params = json_obj_to_query_params(json_obj)
    result = urlencode(query_params)
    return result


def _generate_query_params(
    json_obj, current_param: List[str], is_nested_list: bool
) -> Iterator[Tuple[str, str]]:
    if json_obj is None:
        yield ".".join(current_param), "null"
    elif isinstance(json_obj, dict):
        if not json_obj:
            yield ".".join(current_param) + "~o", ""
            return
        for key, value in json_obj.items():
            key = key.replace("~", "~~").replace(".", "~.")
            current_param.append(key)
            yield from _generate_query_params(value, current_param, False)
            current_param.pop()
    elif isinstance(json_obj, list):
        yield from _generate_query_params_for_list(
            json_obj, current_param, is_nested_list
        )
    elif isinstance(json_obj, bool):
        key = ".".join(current_param)
        json_obj = "true" if json_obj else "false"
        yield key, json_obj
    elif isinstance(json_obj, (int, float, Decimal)):
        key = ".".join(current_param)
        yield key, str(json_obj)
    elif isinstance(json_obj, str):
        yield from _generate_query_params_for_str(json_obj, current_param)
    else:
        raise JsonUrleyError(f"unexpected_type:{json_obj}")


def _generate_query_params_for_list(
    json_obj: List, current_param: List[str], is_nested_list: bool
):
    if not json_obj:
        yield ".".join(current_param) + "~a", ""
        return

    has_nested = next((True for i in json_obj if isinstance(i, (list, dict))), False)
    is_single_item_array = len(json_obj) == 1

    if not has_nested and not is_nested_list and not is_single_item_array:
        # If there is nothing complicated going on, we can output
        # array items in the format item=1&item=2
        for item in json_obj:
            yield from _generate_query_params(item, current_param, False)
        return

    item_index = len(current_param)
    current_param[-1] += "~a"
    first = True
    for item in json_obj:
        current_param.append("n")
        for param_name, param_value in _generate_query_params(
            item, current_param, True
        ):
            yield param_name, param_value
            # Every element after the first one should consider the item existing
            current_param[item_index] = "e"
            if first:
                # Remove the repeat array definition to reduce verbosity
                path_item = current_param[item_index - 1]
                if path_item.endswith("~a"):
                    current_param[item_index - 1] = path_item[:-2]
                first = False
        current_param.pop()


def _generate_query_params_for_str(json_obj: str, current_param: List[str]):
    key = ".".join(current_param)
    if json_obj in ("true", "false", "null"):
        key += "~s"
    try:
        int(json_obj)
        key += "~s"
    except ValueError:
        try:
            float(json_obj)
            key += "~s"
        except ValueError:
            pass
    yield key, json_obj
