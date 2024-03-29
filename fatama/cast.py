def string_to_boolean(value: str) -> bool:
    value = value.lower()
    if value in ["true", "1", "yes"]:
        return True
    elif value in ["false", "0", "no"]:
        return False
    else:
        raise ValueError(f"Inconclusive value to cast as boolean: '{value}'")
