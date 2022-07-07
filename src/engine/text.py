from typing import List

from .. import transform
from .base import _EngineBase


class TextClassification(_EngineBase):
    """
    Text Classification Data Uploader.

    __init__:
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
    """

    def to_proto(
        self, text: str, labels: List[str]
    ) -> transform.data.resources_pb2.Input:
        raw_text = transform.raw_text_to_proto(text)
        concepts = [transform.label_to_concept_proto(l) for l in labels]
        return transform.to_input(text=raw_text, concepts=concepts)
