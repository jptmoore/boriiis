from ocr import Ocr
from alto import Alto
from manifest import Manifest

class Pipeline:
    def __init__(self, ctx, miiify):
        self.ocr = Ocr(ctx)
        self.alto = Alto(ctx, miiify)
        self.manifest = Manifest(ctx)
        self.log = ctx.log

    def run(self, pbar):
        annotations = []
        json = self.manifest.get_manifest()
        zipped = self.manifest.zip(json)
        pbar.total = len(list(zipped))
        for index, (link, target) in enumerate(zipped):           
            alto = self.ocr.get_alto(link)
            alto_targets = self.alto.parse(alto, target, index)
            annotation_targets = []
            for item in alto_targets:
                annotation_page = self.manifest.make_annotation_page(item)
                annotation_targets.append(annotation_page)
            annotations.append(annotation_targets)
            pbar.update(index)
        pbar.update(pbar.total)
        content = self.manifest.add_annotation_pages(json, annotations)
        return content