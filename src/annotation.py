import xmltodict
from jsonpath_ng import jsonpath, parse

class Annotation:
    def __init__(self, ctx):
        self.name = ctx.name

    def add(self, xml):
        dict = xmltodict.parse(xml)
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock[*].TextBlock[*]')
        textblock = [match.value for match in jsonpath_expression.find(dict)]
        for textline in textblock:
            jsonpath_expression = parse('TextLine[*].String[*].@CONTENT')
            lis = [match.value for match in jsonpath_expression.find(textline)]
            content = ' '.join(lis)
            print(content)

        
