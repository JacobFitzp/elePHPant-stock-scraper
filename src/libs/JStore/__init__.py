import json
from os.path import exists


class JStore:
    file = 'cache.json'
    content = {}

    def __init__(self, file):
        self.file = file

        if exists(file):
            with open(file, 'r') as openfile:
                json_object = json.load(openfile)
                self.content = json_object

    def __del__(self):
        self.write()

    def set(self, key, value):
        self.content[key] = value

    def get(self, key):
        if key in self.content:
            return self.content[key]
        return ''

    def get_bool(self, key):
        if key in self.content:
            return self.content[key]
        return False

    def write(self):
        json_data = json.dumps(self.content, indent=4)

        with open(self.file, "w") as outfile:
            outfile.write(json_data)
