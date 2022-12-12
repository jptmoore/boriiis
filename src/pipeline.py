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
        pbar.total = self.manifest.get_image_count(json)
        for index, (image, target) in self.manifest.enumerated_data(json):
            alto = self.ocr.get_alto(image)
            annotation = self.alto.parse(alto, target, index)
            annotations.append(annotation)
            pbar.update(index)
        pbar.update(pbar.total)
        new_manifest = self.manifest.add_annotations(json, annotations)
        return new_manifest