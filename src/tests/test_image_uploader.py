import PIL

from ..engine import image


def test_image_upload():

    uploader = image.ImageOnly("localhost:1000", "xyz")
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(PIL.Image.new("RGB", size=(256, 512)))
    assert len(inp.data.image.base64) > 0

    uploader = image.ImageClassification("localhost:1000", "xyz")
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(PIL.Image.new("RGB", size=(256, 512)), ["1"])
    assert len(inp.data.image.base64) > 0
    assert inp.data.concepts[0].id == "1"
    assert inp.data.concepts[0].name == "1"
    assert inp.data.concepts[0].value == 1.0
