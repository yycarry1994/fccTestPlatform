from pprint import pprint


def mapping_anything(origin_value, var_mapping):
    # processed = None
    if isinstance(origin_value, list):
        processed = mapping_list(origin_value, var_mapping)
    elif isinstance(origin_value, dict):
        processed = mapping_dict(origin_value, var_mapping)
    elif isinstance(origin_value, str):
        processed = mapping_str(origin_value, var_mapping)
    # elif isinstance(origin_value, int):
    #     processed = mapping_int(origin_value, var_mapping)
    else:
        processed = origin_value
    return processed


def mapping_int(origin_value, mapping):
    processed_int = origin_value
    return processed_int


def mapping_dict(origin_value, mapping):
    processed_dict = {}
    for k, v in origin_value.items():
        processed_dict[mapping_anything(k, mapping)] = mapping_anything(v, mapping)
    return processed_dict


def mapping_list(orgin_value, mapping):
    processed_list = []
    for value in orgin_value:
        processed_list.append(mapping_anything(value, mapping))
    return processed_list


def mapping_str(s, mapping):
    if s.startswith('$'):
        if s[1:] in mapping:
            s = mapping[s[1:]]
    return s


if __name__ == '__main__':
    json_origin = {
        "a": "$v1",
        "b": [1, "$v2"],
        "$c": {
            "d1": "222",
            "d2": "$v3"
        }
    }

    json_origin_a = {
        "a": "$v1",
        "b": [1, "$v2"],
        "$c": {
            "d1": "222",
            "d2": "$v3"
        },
        "d": 128,
        "abc": [
            {"$v1": "$v2"},
            {"$v3":
                ["abc", 123, "$c"]
            }
        ]
    }

    var_mapping = {
        "v1": 100,
        "v2": 200,
        "v3": "300",
        "c": "ok"
    }

    pprint(mapping_anything(json_origin_a, var_mapping))
