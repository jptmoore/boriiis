import xmltodict
from jsonpath_ng import parse
from urllib.parse import quote

class Alto:
    def __init__(self, ctx, miiify):
        self.name = ctx.name
        self.preview = ctx.preview
        self.miiify = miiify
        self.remote_server = ctx.remote_server

    def __annotate__(self, slug, box, content, target):
        if self.preview:
            print(content)
        return self.miiify.create_annotation(slug, box, content, target)
    
    def __parse_string__(self, tb):
        try:
            jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
            strings = [match.value for match in jsonpath_expression.find(tb)]
            content = ' '.join(strings)
        except Exception as e:
            self.log.warning("failed to string content")
            return None
        else:
            return content

    def __annotation_page__(self, id):
        dict = {"id": id, "type": "AnnotationPage"}
        return dict

    def __make_annotation_page__(self, target):
        encoded_target = quote(target)
        id = f"{self.remote_server}/annotations/{self.name}?target={encoded_target}"
        return self.__annotation_page__(id)

    def __make_annotation_targets__(self, targets):
        annotation_targets = []
        for item in targets:
            annotation_page = self.__make_annotation_page__(item)
            annotation_targets.append(annotation_page)
        return annotation_targets


    def __parse_textblock_worker__(self, content, target, index):
        targets = []
        for tb in content:
            slug = f"image_{index}_{tb['@ID']}"
            box = f"{tb['@HPOS']},{tb['@VPOS']},{tb['@WIDTH']},{tb['@HEIGHT']}"
            content = self.__parse_string__(tb)
            if content != None:
                response = self.__annotate__(slug, box, content, target)
                if response != None:
                    targets.append(response['target'])
        return self.__make_annotation_targets__(targets)
            

    def __parse_textblock__(self, dict, target, index):
        try:
            jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
            content = [match.value for match in jsonpath_expression.find(dict)]
        except Exception as e:
            self.log.warning("failed to parse textblock")
            return []
        else:        
            return self.__parse_textblock_worker__(content, target, index)


    def parse(self, xml, target, index):
        try:
            dict = xmltodict.parse(xml)
        except Exception as e:
            self.log.warning("failed to parse xml")
            return []
        else:
            return self.__parse_textblock__(dict, target, index)
        


        
