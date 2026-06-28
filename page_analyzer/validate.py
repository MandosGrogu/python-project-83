import validators

def validate(data):
    errors = ""
    if validators.url(data) != True:
        errors = "Указанная страница невалидна!"
    return errors