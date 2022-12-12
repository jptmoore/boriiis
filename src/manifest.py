import requests
from jsonpath_ng import parse

from urllib.parse import quote

class Manifest:
    def __init__(self, ctx):
        self.manifest_link = ctx.manifest_link
        self.name = ctx.name
        self.remote_server = ctx.remote_server
        self.log = ctx.log

    def get_manifest(self):
        try:
            response = requests.get(self.manifest_link)
        except Exception as e:
            self.log.warning("fail to get manifest")
            return None
        if response.status_code != 200:
            self.log.warning(f"Got a {response.status_code} code when accessing manifest")
            return None
        else:
            content = response.json()
            return content

    def __get_image_links__(self, json):
        try:
            jsonpath_expression = parse("items[*].items[*].items[*].body.id")
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            self.log.warning("failed to get image links from manifest")
            return None
        else:
            return lis

    def __get_targets__(self, json):
        try:
            jsonpath_expression = parse("items[*].items[*].items[*].target")
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            self.log.warning("failed to get targets from manifest")
            return None
        else:
            return lis

    def __annotation_page__(self, id):
        dict = {"id": id, "type": "AnnotationPage"}
        return dict

    def make_annotation_page(self, target):
        encoded_target = quote(target)
        id = f"{self.remote_server}/annotations/{self.name}?target={encoded_target}"
        return self.__annotation_page__(id)

    def add_annotation_pages(self, manifest, annotation_pages):
        for (item, annotation_page) in zip(manifest['items'], annotation_pages):
            item['annotations'] = [ annotation_page ]
        return manifest

    def zip(self, json):
        manifest_image_links = self.__get_image_links__(json)
        manifest_targets = self.__get_targets__(json)
        if manifest_image_links == None or manifest_targets == None:
            return []
        else:
            return zip(manifest_image_links, manifest_targets)