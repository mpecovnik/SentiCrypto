def anonymize(string: str):
    """ """
    return "*" * (len(string) - 4) + string[-4:]
