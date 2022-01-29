
import requests


def prepare_request(func):

    def wrapper(*args, **kwargs):

        func(*args, **kwargs)

    return wrapper


@prepare_request
def get():
    return requests.get

@prepare_request
def post():
    return requests.post

@prepare_request
def put():
    return requests.put