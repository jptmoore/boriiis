import requests

class Manifest:
    def __init__(self, ctx):
        self.manifest = ctx.manifest

    def get(self):
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
