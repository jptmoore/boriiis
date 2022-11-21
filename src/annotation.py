import xmltodict
from jsonpath_ng import jsonpath, parse

from miiify import Miiify

import json

class Annotation:
    def __init__(self, ctx):
        self.name = ctx.name
        self.preview = ctx.preview
        self.miiify = Miiify(ctx)
       

    def __annotate__(self, slug, box, content, target):
        if self.preview:
            print(content)
        else:
            annotation = self.miiify.create_annotation(slug, box, content, target)
            json_object = json.dumps(annotation, indent = 2)
            print(json_object)

    
    def __parse_string__(self, tb):
        jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
        strings = [match.value for match in jsonpath_expression.find(tb)]
        content = ' '.join(strings)
        return content


    def __get_image_name__(self, link):
        try:
            image_name = link.split('/')[-1]
        except Exception as e:
            print("Malformed link")
            return None
        else:
            name = image_name.split('.')
            match name:
                case []:
                    print('Unable to get name of image from link')
                    return None
                case [x]:
                    return x
                case [x, *xs]:
                    return x

    def __parse_textblock_worker__(self, content, target, link):
        image_name = self.__get_image_name__(link)
        for tb in content:
            slug = f"{image_name}_{tb['@ID']}"
            box = f"{tb['@HPOS']},{tb['@VPOS']},{tb['@WIDTH']},{tb['@HEIGHT']}"
            content = self.__parse_string__(tb)
            self.__annotate__(slug, box, content, target)

    def __parse_textblock__(self, dict, target, link):
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
        content = [match.value for match in jsonpath_expression.find(dict)]
        self.__parse_textblock_worker__(content, target, link)


    def add(self, xml, target, link):
        dict = xmltodict.parse(xml)
        self.__parse_textblock__(dict, target, link)
        


        
