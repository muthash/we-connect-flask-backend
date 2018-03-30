import re


def validate_email(email):
    """This function is used to validate a user's email"""
    if len(email) > 4:
        regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"
        if re.match(regex, email) is not None:
            return True
    return False

def validate_null(**kwargs):
    """This function is used to validate a null input"""
    messages = []
    for key in kwargs:
        if kwargs[key] is None:
            message = 'Please enter your {}'.format(key)
            messages.append(message)
        else:
            strip_text = re.sub(r'\s+', '', kwargs[key])
            if not strip_text:
                message = 'Please enter your {}'.format(key)
                messages.append(message)
    return messages

