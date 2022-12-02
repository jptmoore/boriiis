import requests
from jsonpath_ng import jsonpath, parse

from ocr import Ocr
from annotation import Annotation

class Manifest:
    def __init__(self, ctx):
        self.manifest_link = ctx.manifest_link
        self.name = ctx.name
        self.remote_server = ctx.remote_server

        self.ocr = Ocr(ctx)
        self.annotation = Annotation(ctx)

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
            jsonpath_expression = parse("items[*].items[*].items[*].body.id")
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            print(e)
            return None
        else:
            return lis

    def get_targets(self, json):
        try:
            jsonpath_expression = parse("items[*].items[*].items[*].target")
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            print(e)
            return None
        else:
            return lis

    def __annotation_page__(self, id):
        dict = {"id": id, "type": "AnnotationPage"}
        return dict

    def get_annotation_page(self, target):
        id = f"{self.remote_server}/annotations/{self.name}?target={target}"
        return self.__annotation_page__(id)


    def add_annotation_pages(self, manifest, annotation_pages):
        for (item, annotation_page) in zip(manifest['items'], annotation_pages):
            item['annotations'] = [ annotation_page ]
        return manifest

    def __zip__(self, manifest_content):
        manifest_links = self.get_links(manifest_content)
        manifest_targets = self.get_targets(manifest_content)
        content = zip(manifest_links, manifest_targets)
        return content

    def run(self):
        annotation_pages = []
        manifest_content = self.get_content()
        for index, (link, target) in enumerate(self.__zip__(manifest_content)):
            annotation_page = self.get_annotation_page(target)
            annotation_pages.append(annotation_page)
            ocr_content = self.ocr.get_content(link)
            response = self.annotation.add(ocr_content, target, index)
        content = self.add_annotation_pages(manifest_content, annotation_pages)
        return content