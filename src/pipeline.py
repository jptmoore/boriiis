import requests
from jsonpath_ng import jsonpath, parse

from ocr import Ocr
from alto import Alto

from urllib.parse import quote

class Pipeline:
    def __init__(self, ctx, miiify):
        self.manifest_link = ctx.manifest_link
        self.name = ctx.name
        self.remote_server = ctx.remote_server
        self.ocr = Ocr(ctx)
        self.alto = Alto(ctx, miiify)
        self.log = ctx.log

    def __get_manifest__(self):
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

    def __make_annotation_page__(self, target):
        encoded_target = quote(target)
        id = f"{self.remote_server}/annotations/{self.name}?target={encoded_target}"
        return self.__annotation_page__(id)

    def __add_annotation_pages__(self, manifest, annotation_pages):
        for (item, annotation_page) in zip(manifest['items'], annotation_pages):
            item['annotations'] = [ annotation_page ]
        return manifest

    def __zip__(self, json):
        manifest_image_links = self.__get_image_links__(json)
        manifest_targets = self.__get_targets__(json)
        if manifest_image_links == None or manifest_targets == None:
            return []
        else:
            return zip(manifest_image_links, manifest_targets)

    def run(self, pbar):
        annotations = []
        json = self.__get_manifest__()
        zipped = self.__zip__(json)
        pbar.total = len(list(zipped))
        for index, (link, target) in enumerate(zipped):           
            alto = self.ocr.get_content(link)
            alto_targets = self.alto.parse(alto, target, index)
            annotation_targets = []
            for item in alto_targets:
                annotation_page = self.__make_annotation_page__(item)
                annotation_targets.append(annotation_page)
            annotations.append(annotation_targets)
            pbar.update(index)
        pbar.update(pbar.total)
        content = self.__add_annotation_pages__(json, annotations)
        return content