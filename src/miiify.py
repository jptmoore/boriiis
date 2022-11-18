
class Miiify:
    def __init__(self, ctx):
        self.container = ctx.name
        self.creator = ctx.creator
        self.version = ctx.version

    def __annotation_payload__(self, creator, body, target):
        dict = {
            "@context": "http://www.w3.org/ns/anno.jsonld",
            "type": "Annotation",
            "motivation": "commenting",
            "body": {"type": "TextualBody", "value": body, "format": "text/plain"},
            "target": target,
            "creator": {"name": creator}
        }
        return dict

    def __container_payload__(self, label):
        dict = {
            "@context": [
                "http://www.w3.org/ns/anno.jsonld",
                "http://www.w3.org/ns/ldp.jsonld"
            ],
            "type": ["BasicContainer", "AnnotationCollection"],
            "label": label
        }
        return dict

    def __basic_headers__(self):
        dict = {'User-Agent': f"boriiis {self.version}", 'Host': 'miiify.rocks'}
        return dict

    def __slug_headers__(self, slug):
        dict = self.__basic_headers()
        dict['Slug'] = slug
        return dict 


    def create_annotation(self, box, content, target):
        payload = self.__annotation_payload__(self.creator, content, target)
        return payload