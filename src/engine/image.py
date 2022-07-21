from typing import List, Optional

from PIL.Image import Image

from .. import transform, utils
from .base import AnnotatedInput, _EngineBase


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

        return AnnotatedInput(input=transform.to_input(image=image))


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

        return AnnotatedInput(input=transform.to_input(image=image, concepts=concepts))


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

    _has_annotation: bool = True

    def to_proto(
        self,
        image: Image,
        labels: List[str],
        binary_maskes: List[Image],
        input_id: Optional[str] = None,
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
        input_proto = transform.to_input(image=image)
        if not input_id:
            input_id = utils.proto_to_hash(input_proto)

        annotations = []
        for l, m in zip(labels, binary_maskes):
            region = transform.zip_concept_and_mask_to_region(
                transform.label_to_concept_proto(l), transform.pil_mask_to_proto(m)
            )
            annotations.append(
                transform.to_annotation(input_id=input_id, regions=[region])
            )

        return AnnotatedInput(input=input_proto, annotation=annotations)
