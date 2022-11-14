import xmltodict
from jsonpath_ng import jsonpath, parse

class Annotation:
    def __init__(self, ctx):
        self.name = ctx.name

    def add(self, xml):
        dict = xmltodict.parse(xml)
        jsonpath_expression = parse('alto.Layout.Page.PrintSpace.ComposedBlock.TextBlock')
        lis = [match.value for match in jsonpath_expression.find(dict)]
        print(lis)
