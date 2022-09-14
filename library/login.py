import json


class login():
    """
    A login class for login
    """

    def __init__(self, location='') -> str:
        self.location = location
        with open(f'{location}', 'r') as f:
            data = json.load(f)
            email = data['email']
            password = data['password']
            headers_value = data['user-agent']
        self.email = email
        self.password = password
        self.headers = headers_value

    @property
    def email(self) -> str:
        """
        returns string value of email from key.json
        """
        return self.email

    @property
    def password(self) -> str:
        """
        returns string value of password from key.json
        """
        return self.password

    @property
    def headers(self) -> str:
        """
        returns string value of headers from key.json
        """
        return self.headers
