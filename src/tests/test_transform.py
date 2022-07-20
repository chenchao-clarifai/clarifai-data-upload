import numpy as np
import PIL
import pytest

from ..transform import data, image, label, mask, text


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


def test_pil_mask():
    arr = np.array([[i * j for i in range(10)] for j in range(10)]).astype(np.int8)
    im = PIL.Image.fromarray(arr, mode="L")
    ip = image.pil_mask_to_proto(im)
    assert isinstance(ip, image.resources_pb2.Image)
    assert ip.base64 == image.encode_image(im, "PNG")
    assert image.decode_image(image.encode_image(im)).size == im.size

    im = PIL.Image.fromarray(arr, mode="P")
    ip = image.pil_mask_to_proto(im)
    assert isinstance(ip, image.resources_pb2.Image)
    assert ip.base64 == image.encode_image(im, "PNG")
    assert image.decode_image(image.encode_image(im, "PNG")).size == im.size

    with pytest.raises(ValueError):
        im = PIL.Image.fromarray(arr, mode="P").convert("RGB")
        ip = image.pil_mask_to_proto(im)
        print(ip)

    multiclass = PIL.Image.fromarray(arr, mode="L")
    singles = image.multiclass_mask_to_binary_maskes(multiclass)
    assert len(singles) == len(np.unique(arr))
    for k, v in singles.items():
        assert k >= 0 and k <= 81
        assert v.mode == "1"
        assert v.size == multiclass.size


def test_mask():
    arr = np.array([[i * j for i in range(10)] for j in range(10)]).astype(np.int8)
    multiclass = PIL.Image.fromarray(arr, mode="L")
    singles = image.multiclass_mask_to_binary_maskes(multiclass)
    m = image.pil_mask_to_proto(singles[0])
    region = mask.zip_concept_and_mask_to_region(label.label_to_concept_proto("cat"), m)
    assert region.region_info.mask.image == m
    assert region.data.concepts[0].id == "cat"


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

    anno_proto = data.to_annotation(text=t, concepts=[c, d], image=i)
    assert anno_proto.input_id == "none"
    assert anno_proto.data.text == t
    assert anno_proto.data.concepts[0] == c
    assert anno_proto.data.concepts[1] == d
    assert anno_proto.data.image == i

    anno_proto = data.to_annotation(input_id="abc", text=t, concepts=[c, d], image=i)
    assert anno_proto.input_id == "abc"
    assert anno_proto.data.text == t
    assert anno_proto.data.concepts[0] == c
    assert anno_proto.data.concepts[1] == d
    assert anno_proto.data.image == i

    anno_batch = data.annotation_batch_to_request([anno_proto])
    assert anno_batch.annotations[0] == anno_proto
