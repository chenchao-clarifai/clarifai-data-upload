import PIL

from ..transform import data, image, label, text


def test_text():
    s = text.raw_text_to_proto("Hello World")
    assert s.raw == "Hello World"


def test_label():
    cat = label.label_to_concept_proto("cat")
    assert cat.id == "cat"
    assert cat.name == "cat"
    assert cat.value == 1.0

    dog = label.label_to_concept_proto(" dog ", label_value=0.5)
    assert dog.id == "dog"
    assert dog.name == "dog"
    assert dog.value == 0.5

    mix = label.label_to_concept_proto(" cat or dog ")
    assert mix.id == "cat-or-dog"
    assert mix.name == "cat or dog"
    assert mix.value == 1.0


def test_image():

    im = PIL.Image.new(mode="RGB", size=(256, 500))
    ip = image.pil_to_proto(im)
    assert isinstance(ip, image.resources_pb2.Image)
    assert ip.base64 == image.encode_image(im)

    assert image.decode_image(image.encode_image(im)).size == im.size


def test_data():
    t = text.raw_text_to_proto("Hello World")
    c = label.label_to_concept_proto("cat")
    d = label.label_to_concept_proto("dog")
    im = PIL.Image.new(mode="RGB", size=(256, 500))
    i = image.pil_to_proto(im)
    input_proto = data.to_input(text=t, concepts=[c, d], image=i)
    assert input_proto.data.text == t
    assert input_proto.data.concepts[0] == c
    assert input_proto.data.concepts[1] == d
    assert input_proto.data.image == i

    input_batch = data.input_batch_to_request([input_proto])
    assert input_batch.inputs[0] == input_proto
