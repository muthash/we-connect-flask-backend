import re, uuid

from flask import request, jsonify
from functools import wraps
from usernames import is_safe_username
from flask_mail import Message
from email_validator import validate_email, EmailNotValidError
from app import mail


def require_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.get_json(silent=True) is None:
            response = {'message': 'The Request should be JSON format'}
            return jsonify(response), 422
        return func(*args, **kwargs)
    return wrapper

def check_email(email):
    try:
        validate_email(email, check_deliverability=False)
        return False
    except EmailNotValidError as error:
        response = {'message': str(error)}
        return jsonify(response), 400

def normalise_email(email):
    validator_response = validate_email(email, check_deliverability=False)
    email = validator_response["email"]
    return email

def check_username(username):
    regex = re.compile('^[a-zA-Z0-9_]{3,}$')
    res = re.match(regex, str(username))
    if not is_safe_username(username):
        response = {'message': "The username you provided is not allowed, " +
                               "please try again but with a different name."}
        return jsonify(response), 400
    if not res:
        response = {'message': "The Username should contain atleast four alpha-numeric characters. " +
                               "The optional special character allowed is _ (underscore)."}
        return jsonify(response), 400

def check_password(password):
    if re.match(r'[a-zA-Z_]+[A-Za-z0-9@#!$%^&+=]{8,}', str(password)):
        return False
    response = {'message': 'Password should contain at least eight ' +
                            'characters with at least one digit, one ' +
                            'uppercase letter and one lowercase letter'}
    return jsonify(response), 400

def check_missing_field(**kwargs):
    errors={}
    for key in kwargs:
        if kwargs[key] is None:
            error_key = key + '-error'
            errors[error_key] = f'The {key} should not be missing'
        else:
            strip_text = re.sub(r'\s+', '', str(kwargs[key]))
            if not strip_text:
                error_key = key + '-error'
                errors[error_key] = f'The {key} should not be empty'
    return errors

def validate_registration(email, username, password):
    email = str(email)
    username = str(username)
    password = str(password)
    if check_email(email):
        return check_email(email)
    if check_username(username):
        return check_username(username)
    if check_password(password):
        return check_password(password)
    return False

def send_reset_password(email, password):
    """Returns a random string of length string_length"""
    message = Message(
        subject='Weconnect Account Password Reset',
        recipients=[email],
        html=f'Your new password is: {password}'
    )
    mail.send(message)

def random_string(string_length=8):
    """Returns a random string of length string_length"""
    random = str(uuid.uuid4())
    random = random.replace("-", "")
    return random[:string_length]

def remove_more_spaces(user_input):
    """Maximum number os spaces between words should be one"""
    strip_text = user_input.strip()
    return re.sub(r'\s+', ' ', strip_text)

def remove_none_fields(**kwargs):
    update_data={}
    for key in kwargs:
        if kwargs[key] is not None:
            update_data[key] = kwargs[key]
    return update_data

def filter_business(data, category=False, location=False):
    if category and location:
        businesses = [business.serialize() for business in data.items 
                      if (category == business.category and location == business.location)]
        return return_filter(data, businesses)
    if category:
        business = data
        businesses = [business.serialize() for business in data.items 
                      if category == business.category]
        return return_filter(data, businesses)
    if location:
        businesses = [business.serialize() for business in data.items 
                      if location == business.location]
        return return_filter(data, businesses)

def return_filter(page_items, page_items_list):
    if page_items_list:
        next_url = page_items.next_num  if page_items.has_next else None
        prev_url = page_items.prev_num  if page_items.has_prev else None
        response = {'businesses': page_items_list,
                    'next_page': next_url,
                    'prev_page': prev_url
        }
        return jsonify(response), 200
    response = {'message': f'Your filter criteria did not match any business'}
    return jsonify(response), 200

messages = {
    'account_created': 'Account created successfully',
    'exists': 'A User with that email already exists.',
    'valid_email': 'The email provided is not registered',
    'login': 'Login successfull',
    'valid_epass': 'Invalid email or password',
    'sent_mail': 'Password reset successfull. Check your email for your new password',
    'not_reset': 'Password was not reset. Try again',
    'password': 'Password change successfull',
    'valid_pass': 'Old password entered is not correct',
    'valid_login': 'Please login to continue',
    'delete': 'Account deleted successfully',
    'business_created': 'Business created successfully',
    'business_updated': 'Business updated successfully',
    'forbidden': 'The operation is Forbidden',
    'business_delete': 'Business deleted successfully',
    'businesses': 'The following business are available',
    'no_business': 'There are no businesses registered currently',
    'not_found': 'The business was not found',
    'one_update': 'Enter atleast one input to update',
    'incorrect': 'Enter correct password to delete'
}