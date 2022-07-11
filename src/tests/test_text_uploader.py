from ..engine import text


def test_text_upload():

    uploader = text.TextClassification("localhost:1000", "xyz")
    print(uploader)
    print(uploader.info())
