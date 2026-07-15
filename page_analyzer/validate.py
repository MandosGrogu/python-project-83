import validators

def validate(data):
    errors = ""
    if not validators.url(data):
        errors = "Указанная страница невалидна!"
    return errors