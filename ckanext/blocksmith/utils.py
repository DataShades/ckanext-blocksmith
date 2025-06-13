from typing import Any


def prepare_snippet_arguments(data_dict: dict[str, Any]) -> list[dict[str, Any]]:
    snippet_args = [
        "argument[]",
        "required[]",
        "input_type[]",
    ]

    columns = map(
        lambda key: (
            data_dict.get(key, [])
            if isinstance(data_dict.get(key, []), list)
            else [data_dict.get(key, [])]
        ),
        snippet_args,
    )

    default_value_conditions = list(zip(*columns))

    return [
        {"argument": i[0], "required": i[1], "input_type": i[2]}
        for i in default_value_conditions
    ]
