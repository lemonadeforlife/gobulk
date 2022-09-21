import json


class login():
    """
    login CLASS returns three values:
    * email    -> return email address
    * password -> returns password
    * headers  -> post custom headers to not get rejected from servers
    """

    def __init__(self, path: str) -> str:
        with open(path, 'r') as f:
            data = json.load(f)
            self.data = data

    @property
    def email(self):
        return self.data['email']

    @property
    def password(self):
        return self.data['password']

    @property
    def headers(self):
        return self.data['user-agent']
