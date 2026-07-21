import validators

def validate(data):
    errors = ""
    res = validators.url(data)
    if not res:
        errors = "Указанная страница невалидна!"
    return errors