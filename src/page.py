import math
from urllib.parse import quote


class Page:
    def __init__(self, ctx, miiify):
        self.miiify = miiify
        self.page_limit = ctx.page_limit
        self.local_server = ctx.local_server
        self.remote_server = ctx.remote_server
        self.name = ctx.name

    def __page_count__(self):
        total = self.miiify.annotation_total()
        return math.ceil(total / self.page_limit)

    def __generate_pages__(self):
        pages = []
        count = self.__page_count__()
        for page in range(count):
            query_string = f"?page={page}"
            pages.append(query_string)
        return pages

    def __encode_target__(self, target):
        encoded_target = quote(target)
        return f"&target={encoded_target}"

    def __make_annotation_item__(self, id):
        dict = {"id": id, "type": "AnnotationPage"}
        return dict

    def __expand_targets_worker__(self, targets):
        acc = []
        pages = self.__generate_pages__()
        for target in targets:
            for page in pages:
                remote = f"{self.remote_server}/annotations/{self.name}{page}{self.__encode_target__(target)}"
                local = f"{self.local_server}/annotations/{self.name}{page}{self.__encode_target__(target)}"
                if self.miiify.annotation_exists(local):
                    item = self.__make_annotation_item__(remote)
                    acc.append(item)
        return acc

    def expand_targets(self, targets):
        acc = []
        for target in targets:
            res = self.__expand_targets_worker__(target)
            acc.append(res)
        return acc
