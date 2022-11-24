import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Miiify:
    def __init__(self, ctx):
        self.name = ctx.name
        self.creator = ctx.creator
        self.version = ctx.version

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

    def __basic_headers__(self):
        dict = {"User-Agent": f"boriiis {self.version}", "Host": "miiify.rocks"}
        return dict

    def __slug_headers__(self, slug):
        dict = self.__basic_headers__()
        dict["Slug"] = slug
        return dict

    def create_annotation(self, slug, box, content, target):
        url = f"https://localhost:8080/annotations/{self.name}/"
        headers = self.__slug_headers__(slug)
        payload = self.__annotation_payload__(self.creator, box, content, target)
        response = requests.post(url, json=payload, verify=False, headers=headers)
        return response
