import requests
from jsonpath_ng import jsonpath, parse


class Manifest:
    def __init__(self, ctx):
        self.manifest = ctx.manifest

    def get_json(self):
        try:
            response = requests.get(self.manifest)
        except Exception as e:
            print(e)
            return None
        else:
            if response.status_code == 200:
                json = response.json()
                print("ok")
                return json
            else:
                print(f"Got status code {response.status_code}")
                return None

    def get_links(self, json):
        try:
            jsonpath_expression = parse('items[*].items[*].items[*].body.id')
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            print(e)
            return None
        else:
            return lis
