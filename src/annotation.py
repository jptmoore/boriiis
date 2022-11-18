import xmltodict
from jsonpath_ng import jsonpath, parse

from miiify import Miiify

import json

class Annotation:
    def __init__(self, ctx):
        self.name = ctx.name
        self.preview = ctx.preview
        self.miiify = Miiify(ctx)
       

    def __annotate__(self, box, content, target):
        if self.preview:
            print(content)
        else:
            annotation = self.miiify.create_annotation(box, content, target)
            json_object = json.dumps(annotation, indent = 2)
            print(json_object)

    
    def __parse_string__(self, tb):
        jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
        strings = [match.value for match in jsonpath_expression.find(tb)]
        content = ' '.join(strings)
        return content


    def __parse_textblock_worker__(self, content, target):
        for tb in content:
            box = f"{tb['@HPOS']},{tb['@VPOS']},{tb['@WIDTH']},{tb['@HEIGHT']}"
            content = self.__parse_string__(tb)
            self.__annotate__(box, content, target)

    def __parse_textblock__(self, dict, target):
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
        content = [match.value for match in jsonpath_expression.find(dict)]
        self.__parse_textblock_worker__(content, target)


    def add(self, xml, target):
        dict = xmltodict.parse(xml)
        self.__parse_textblock__(dict, target)
        


        
