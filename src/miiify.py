import requests
import urllib3
import subprocess
import time
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Miiify:
    def __init__(self, ctx):
        assert(os.path.exists(ctx.local_repo))
        self.name = ctx.name
        self.creator = ctx.creator
        self.version = ctx.version
        self.local_server = ctx.local_server
        self.app = ctx.app
        self.app_dir = ctx.app_dir

    def __annotation_payload__(self, creator, box, content, target):
        dict = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "type": "Annotation",
            "motivation": "commenting",
            "body": {"type": "TextualBody", "value": content, "format": "text/plain"},
            "selector": {
                "type": "FragmentSelector",
                "conformsTo": "http://www.w3.org/TR/media-frags/",
                "value": f"xywh={box}",
            },
            "target": f"{target}#xywh={box}",
            "creator": {"name": creator},
        }
        return dict

    def __container_payload__(self, label):
        dict = {
            "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                "http://www.w3.org/ns/ldp.jsonld",
            ],
            "type": ["BasicContainer", "AnnotationCollection"],
            "label": label,
        }
        return dict

    def __container_payload__(self, label):
        dict = {
            "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                "http://www.w3.org/ns/ldp.jsonld",
            ],
            "type": ["BasicContainer", "AnnotationCollection"],
            "label": label,
        }
        return dict

    def __basic_headers__(self):
        dict = {"User-Agent": f"boriiis {self.version}", "Host": "miiify.rocks"}
        return dict

    def __slug_headers__(self, slug):
        dict = self.__basic_headers__()
        dict["Slug"] = slug
        return dict

    def create_annotation(self, slug, box, content, target):
        url = f"{self.local_server}/annotations/{self.name}/"
        headers = self.__slug_headers__(slug)
        payload = self.__annotation_payload__(self.creator, box, content, target)
        response = requests.post(url, json=payload, verify=False, headers=headers)
        return payload

    def create_manifest(self, payload):
        url = f"{self.local_server}/manifest/{self.name}"
        headers = self.__basic_headers__()
        response = requests.post(url, json=payload, verify=False, headers=headers)
        return response.status_code

    def create_container(self):
        url = f"{self.local_server}/annotations/"
        headers = self.__slug_headers__(self.name)
        label = f"{self.name} by {self.creator}"
        payload = self.__container_payload__(label)
        response = requests.post(url, json=payload, verify=False, headers=headers)
        return response.status_code

    def __is_alive__(self):
        url = self.local_server
        headers = self.__basic_headers__()
        try:
            response = requests.get(url, verify=False, headers=headers)
        except:
            return False
        else:
            return response.status_code == 200

    def start(self):
        os.chdir(self.app_dir)
        subprocess.Popen(
            [self.app],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        while self.__is_alive__() == False:
            time.sleep(1.0)
        self.create_container()

