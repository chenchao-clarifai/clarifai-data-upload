import PIL

from ..engine import image


def test_image_upload():

    uploader = image.ImageOnly("localhost:1000", "xyz")
    assert uploader._has_annotation is False
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(PIL.Image.new("RGB", size=(256, 512))).input
    assert len(inp.data.image.base64) > 0

    uploader = image.ImageClassification("localhost:1000", "xyz")
    assert uploader._has_annotation is False
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(PIL.Image.new("RGB", size=(256, 512)), ["1"]).input
    assert len(inp.data.image.base64) > 0
    assert inp.data.concepts[0].id == "1"
    assert inp.data.concepts[0].name == "1"
    assert inp.data.concepts[0].value == 1.0


def test_segmentation_upload():

    uploader = image.ImageSemanticSegmentation("localhost:1000", "xyz")
    assert uploader._has_annotation is True
    print(uploader)
    print(uploader.info())
    img = PIL.Image.new("RGB", size=(256, 512))
    msk = PIL.Image.new("1", size=(256, 512))
    anno_inp = uploader.to_proto(img, dict(a=msk, b=msk))
    assert len(anno_inp.input.data.image.base64) > 0
    assert anno_inp.annotation[0].data.regions[0].data.concepts[0].id == "a"
    assert anno_inp.annotation[0].data.regions[0].data.concepts[0].name == "a"
    assert anno_inp.annotation[0].data.regions[0].data.concepts[0].value == 1.0
    assert anno_inp.input.id == anno_inp.annotation[0].input_id
    assert anno_inp.annotation[0].input_id == anno_inp.annotation[1].input_id
