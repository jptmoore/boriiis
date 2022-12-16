import requests
import urllib3
import subprocess
import time
import os

from pp import pp_exit

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Miiify:
    def __init__(self, ctx):
        assert(os.path.exists(ctx.local_repo))
        self.name = ctx.name
        self.creator = ctx.creator
        self.version = ctx.version
        self.local_server = ctx.local_server
        self.remote_server = ctx.remote_server
        self.app = ctx.app
        self.app_dir = ctx.app_dir
        self.log = ctx.log
        self.update = ctx.update

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

    def __link_only_headers__(self):
        dict = self.__basic_headers__()
        dict["Prefer"] = 'return=representation;include="http://www.w3.org/ns/oa#PreferContainedIRIs"'
        return dict        

    def __create_annotation__(self, slug, box, content, target):
        url = f"{self.local_server}/annotations/{self.name}/"
        headers = self.__slug_headers__(slug)
        payload = self.__annotation_payload__(self.creator, box, content, target)
        try:
            response = requests.post(url, json=payload, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to create annotation")
        if response.status_code != 201:
            pp_exit(f"Got a {response.status_code} code when creating annotation")
        else:
            return payload


    def __update_annotation__(self, slug, box, content, target):
        local = f"{self.local_server}/annotations/{self.name}/{slug}"
        remote = f"{self.remote_server}/annotations/{self.name}/{slug}"
        headers = self.__basic_headers__()
        payload = self.__annotation_payload__(self.creator, box, content, target)
        payload['id'] = remote 
        try:
            response = requests.put(local, json=payload, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to update annotation")
        # if we are doing an --update but there are new annotations
        if response.status_code == 400:
            return self.__create_annotation__(slug, box, content, target)
        else:
            return payload


    def create_annotation(self, slug, box, content, target):
        if self.update == True:
            return self.__update_annotation__(slug, box, content, target)
        else:
            return self.__create_annotation__(slug, box, content, target)


    def __create_manifest__(self, payload):
        url = f"{self.local_server}/manifest/{self.name}"
        headers = self.__basic_headers__()
        try:
            response = requests.post(url, json=payload, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to create manifest")
        if response.status_code != 201:
            pp_exit(f"Got a {response.status_code} code when creating manifest")
        else:
            return payload


    def __update_manifest__(self, payload):
        url = f"{self.local_server}/manifest/{self.name}"
        headers = self.__basic_headers__()
        try:
            response = requests.put(url, json=payload, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to update manifest")
        if response.status_code != 200:
            pp_exit(f"Got a {response.status_code} code when updating manifest")
        else:
            return payload


    def create_manifest(self, payload):
        if self.update == True:
            return self.__update_manifest__(payload)
        else:
            return self.__create_manifest__(payload)


    def __create_container__(self):
        url = f"{self.local_server}/annotations/"
        headers = self.__slug_headers__(self.name)
        label = f"{self.name} by {self.creator}"
        payload = self.__container_payload__(label)
        try:
            response = requests.post(url, json=payload, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to create container")
        if response.status_code != 201:
            pp_exit(f"{self.name} already exists (hint: try --update)")
        else:          
            return payload

    def create_container(self):
        if self.update == True:
            pass
        else:
            return self.__create_container__()            

    
    def annotation_exists(self, url):
        headers = self.__link_only_headers__()
        try:
            response = requests.get(url, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to get annotation")
        try:
            json = response.json()
            items = json['items']
            return response.status_code == 200 and items != []
        except Exception as e:
            pp_exit("failed to get annotation items")            


    def annotation_total(self):
        headers = self.__link_only_headers__()
        url = f"{self.local_server}/annotations/{self.name}/"
        try:
            response = requests.get(url, verify=False, headers=headers)
        except Exception as e:
            pp_exit("failed to get annotation")
        if response.status_code != 200:
            pp_exit(f"Got a {response.status_code} code when reading annotation total")
        try:
            json = response.json()       
            return json['total']
        except Exception as e:
            pp_exit("failed to get annotation total")


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

