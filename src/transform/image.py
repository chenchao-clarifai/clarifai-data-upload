import base64
from io import BytesIO
from typing import ByteString, Dict

import numpy as np
import PIL
from clarifai_grpc.grpc.api import resources_pb2
from PIL.Image import Image

MASK_MODES = {"P", "L", "1"}


def pil_to_buffer(pil_image: Image, format: str = "JPEG") -> ByteString:
    buffered = BytesIO()
    pil_image.save(buffered, format=format)
    return buffered.getvalue()


def encode_image(pil_image: Image, format: str = "JPEG") -> ByteString:
    buffered = BytesIO()
    pil_image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue())


def decode_image(byte_string: bytes) -> Image:
    return PIL.Image.open(BytesIO(base64.b64decode(byte_string)))


def pil_to_proto(pil_image: Image, format: str = "JPEG") -> resources_pb2.Image:
    s = pil_to_buffer(pil_image, format)
    return resources_pb2.Image(base64=s)


def pil_mask_to_proto(pil_mask: Image) -> resources_pb2.Image:
    if pil_mask.mode in MASK_MODES:
        return pil_to_proto(pil_mask, "PNG")
    else:
        raise ValueError(f"The image mode {pil_mask.mode} is not in {MASK_MODES}.")


def multiclass_mask_to_binary_masks(
    pil_mask: Image, ignore_idx: int = -1
) -> Dict[int, Image]:
    if pil_mask.mode not in ("P", "L"):
        raise ValueError("Multiclass masks should be in `P` or `L` modes.")
    arr_mask = np.array(pil_mask)
    unique_ints = np.unique(arr_mask)

    binary_masks = {}
    for l in unique_ints:
        if l == ignore_idx:
            continue
        binary_masks[l] = PIL.Image.fromarray(np.where(arr_mask == l, True, False))

    return binary_masks
