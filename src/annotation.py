import xmltodict
from jsonpath_ng import jsonpath, parse

class Annotation:
    def __init__(self, ctx):
        self.name = ctx.name
        self.preview = ctx.preview
       

    def __create_annotation__(self, box, content):
        pass

    def __annotate__(self, box, content):
        if self.preview:
            print(content)
        else:
            annotation = self.__create_annotation__(box, content)
            print(annotation)

    
    def __parse_string__(self, tb):
        jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
        strings = [match.value for match in jsonpath_expression.find(tb)]
        content = ' '.join(strings)
        return content


    def __parse_textblock_worker__(self, content):
        for tb in content:
            box = ( tb['@HPOS'], tb['@VPOS'], tb['@WIDTH'], tb['@HEIGHT'] )
            content = self.__parse_string__(tb)
            self.__annotate__(box, content)

    def __parse_textblock__(self, dict):
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
        content = [match.value for match in jsonpath_expression.find(dict)]
        self.__parse_textblock_worker__(content)


    def add(self, xml):
        dict = xmltodict.parse(xml)
        self.__parse_textblock__(dict)
        


        
