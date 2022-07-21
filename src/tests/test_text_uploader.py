from ..engine import text


def test_text_upload():

    uploader = text.TextClassification("localhost:1000", "xyz")
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(
        " ".join(["a"] * (text.MAX_RAW_TEXT_WORD_COUNT + 100)), ["1"]
    ).input
    assert len(inp.data.text.raw.split()) == text.MAX_RAW_TEXT_WORD_COUNT
    assert inp.data.concepts[0].id == "1"
    assert inp.data.concepts[0].name == "1"
    assert inp.data.concepts[0].value == 1.0
