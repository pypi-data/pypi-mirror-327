import json
from pathlib import Path

from .settings import PASSWD_FILE


class Accounts:
    def __init__(self, filename=None):
        if not filename:
            filename = PASSWD_FILE
        self.filename = filename

    def read(self):
        self.passwd = json.loads(Path(self.filename).read_text())

    def write(self):
        Path(self.filename).write_text(json.dumps(self.passwd, indent=2))

    def get(self, username):
        self.read()
        return self.passwd[username]

    def set(self, username, password):
        self.read()
        self.passwd[username] = password
        self.write()

    def delete(self, username):
        self.read()
        del self.passwd[username]
        self.write()
