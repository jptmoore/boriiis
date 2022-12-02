import xmltodict
from jsonpath_ng import jsonpath, parse

class Alto:
    def __init__(self, ctx, miiify):
        self.name = ctx.name
        self.preview = ctx.preview
        self.miiify = miiify
    

    def __annotate__(self, slug, box, content, target):
        if self.preview:
            print(content)
            return None
        else:
            response = self.miiify.create_annotation(slug, box, content, target)
            return response

    
    def __parse_string__(self, tb):
        jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
        strings = [match.value for match in jsonpath_expression.find(tb)]
        content = ' '.join(strings)
        return content

    def __parse_textblock_worker__(self, content, target, index):
        for tb in content:
            slug = f"image_{index}_{tb['@ID']}"
            box = f"{tb['@HPOS']},{tb['@VPOS']},{tb['@WIDTH']},{tb['@HEIGHT']}"
            content = self.__parse_string__(tb)
            self.__annotate__(slug, box, content, target)

    def __parse_textblock__(self, dict, target, index):
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
        content = [match.value for match in jsonpath_expression.find(dict)]
        self.__parse_textblock_worker__(content, target, index)


    def parse(self, xml, target, index):
        dict = xmltodict.parse(xml)
        self.__parse_textblock__(dict, target, index)
        


        