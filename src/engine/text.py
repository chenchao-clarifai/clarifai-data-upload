import warnings
from typing import List

from .. import transform
from .base import _EngineBase

MAX_RAW_TEXT_WORD_COUNT = 500


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
        """
        to_proto.

        Args:
            text (str): raw text string
            labels (List[str]): list of string labels

        Returns:
            resources_pb2.Input: input proto
        """
        words = text.split()
        if len(words) > MAX_RAW_TEXT_WORD_COUNT:
            warnings.warn(
                f"Current word count ({len(words)}) > "
                f"max supported word count ({MAX_RAW_TEXT_WORD_COUNT}). "
                "The text will be truncated."
            )
            text = " ".join(words[:MAX_RAW_TEXT_WORD_COUNT])
        raw_text = transform.raw_text_to_proto(text)
        concepts = [transform.label_to_concept_proto(l) for l in labels]
        return transform.to_input(text=raw_text, concepts=concepts)
