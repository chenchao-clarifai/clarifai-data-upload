import base64
from io import BytesIO

import PIL
from clarifai_grpc.grpc.api import resources_pb2
from PIL.Image import Image


def pil_to_buffer(pil_image: Image, format: str = "JPEG"):
    bf = BytesIO()
    pil_image.save(bf, format=format)
    return bf


def encode_image(pil_image: Image, format: str = "JPEG"):
    buffered = BytesIO()
    pil_image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue())


def decode_image(byte_string: bytes):
    return PIL.Image.open(BytesIO(base64.b64decode(byte_string)))


def pil_to_proto(pil_image: Image, format: str = "JPEG"):
    s = encode_image(pil_image, format)
    return resources_pb2.Image(base64=s)
