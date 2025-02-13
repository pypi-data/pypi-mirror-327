import requests

def info():
    return "AdrianDevProjects Online Services Python SDK Authentication Module v1.0.0 by Adrian Albrecht"


def login(username, password, scopes):
    url = "https://onlineservices.adriandevprojects.com/v1/auth/login_external/"

    credentials = {
        "username": username,
        "password": password
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=credentials, headers=headers)

    if scopes == "content+code" or "code+content":
        return f"{response.status_code}\n{response.text}"
    elif scopes == "content":
        return response.text
    elif scopes == "code":
        return response.status_code
    else:
        return "Invalid scopes"