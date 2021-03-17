import requests

def make_request(url, returnResult=True, result_obj=None):
    result = requests.get(url).json()
    if returnResult:
        return result
    else:
        result_obj.result = result