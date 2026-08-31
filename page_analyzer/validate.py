import validators

def validate(data):
    errors = ""
    res = validators.url(data)
    if not res:
        errors = "Некорректный URL"
    return errors