from ..engine import text


def test_text_upload():

    uploader = text.TextClassification("localhost:1000", "xyz")
    print(uploader)
    print(uploader.info())
    inp = uploader.to_proto(
        " ".join(["a"] * (text.MAX_RAW_TEXT_WORD_COUNT + 100)), ["1"]
    )
    assert len(inp.data.text.raw.split()) == text.MAX_RAW_TEXT_WORD_COUNT
