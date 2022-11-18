import requests
from jsonpath_ng import jsonpath, parse


class Manifest:
    def __init__(self, ctx):
        self.manifest_link = ctx.manifest_link

    def get_content(self):
        try:
            response = requests.get(self.manifest_link)
        except Exception as e:
            print(e)
            return None
        else:
            if response.status_code == 200:
                content = response.json()
                return content
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

    def get_targets(self, json):
        try:
            jsonpath_expression = parse('items[*].items[*].items[*].target')
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            print(e)
            return None
        else:
            return lis