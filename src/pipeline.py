import requests
from jsonpath_ng import jsonpath, parse

from ocr import Ocr
from alto import Alto

class Pipeline:
    def __init__(self, ctx, miiify):
        self.manifest_link = ctx.manifest_link
        self.name = ctx.name
        self.remote_server = ctx.remote_server
        self.ocr = Ocr(ctx)
        self.alto = Alto(ctx, miiify)

    def __get_content__(self):
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

    def __get_links__(self, json):
        try:
            jsonpath_expression = parse("items[*].items[*].items[*].body.id")
            lis = [match.value for match in jsonpath_expression.find(json)]
        except Exception as e:
            print(e)
            return None
        else:
            return lis

    def __get_targets__(self, json):
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

    def __get_annotation_page__(self, target):
        id = f"{self.remote_server}/annotations/{self.name}?target={target}"
        return self.__annotation_page__(id)


    def __add_annotation_pages__(self, manifest, annotation_pages):
        for (item, annotation_page) in zip(manifest['items'], annotation_pages):
            item['annotations'] = [ annotation_page ]
        return manifest

    def __zip__(self, manifest_content):
        manifest_links = self.__get_links__(manifest_content)
        manifest_targets = self.__get_targets__(manifest_content)
        content = zip(manifest_links, manifest_targets)
        return content

    def run(self):
        annotation_pages = []
        manifest_content = self.__get_content__()
        for index, (link, target) in enumerate(self.__zip__(manifest_content)):
            annotation_page = self.__get_annotation_page__(target)
            annotation_pages.append(annotation_page)
            alto = self.ocr.get_content(link)
            response = self.alto.parse(alto, target, index)
        content = self.__add_annotation_pages__(manifest_content, annotation_pages)
        return content