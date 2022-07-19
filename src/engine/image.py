from typing import List

from PIL.Image import Image

from .. import transform
from .base import _EngineBase


class ImageOnly(_EngineBase):
    """
    Image Data Uploader.

    __init__:
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
    """

    def to_proto(self, image: Image) -> transform.data.resources_pb2.Input:
        """
        to_proto.

        Args:
            image (Image): PIL Image object

        Returns:
            resources_pb2.Input: input proto
        """

        image = transform.pil_to_proto(image)

        return transform.to_input(image=image)


class ImageClassification(_EngineBase):
    """
    Image Classification Data Uploader.

    __init__:
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
    """

    def to_proto(
        self, image: Image, labels: List[str]
    ) -> transform.data.resources_pb2.Input:
        """
        to_proto.

        Args:
            image (Image): PIL Image object
            labels (List[str]): list of string labels

        Returns:
            resources_pb2.Input: input proto
        """

        image = transform.pil_to_proto(image)
        concepts = [transform.label_to_concept_proto(l) for l in labels]

        return transform.to_input(image=image, concepts=concepts)


class ImageSegmentation(_EngineBase):
    """
    Image Segmentation Data Uploader.

    __init__:
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
    """

    def to_proto(
        self, image: Image, labels: List[str], binary_maskes: List[Image]
    ) -> transform.data.resources_pb2.Input:
        """
        to_proto.

        Args:
            image (Image): PIL Image object
            labels (List[str]): list of string labels
            binary_maskes (List[Image]): list of black-white PNG (mode=`1`)

        Returns:
            resources_pb2.Input: input proto
        """

        image = transform.pil_to_proto(image)
        # region = todo region contains the concepts and maskes

        return transform.to_input(image=image)
