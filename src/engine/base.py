import warnings
from collections import Counter
from typing import Any, Dict, Tuple

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

from .. import transform

CHANNEL_URLS = {
    "prod": "api.clarifai.com",
    "dev": "api-dev.clarifai.com",
    "staging": "api-staging.clarifai.com",
}

REGISTRY = []

MAX_BATCH_SIZE = 128


class RegisteredEngine(type):
    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        if not name.startswith("_"):
            REGISTRY.append(new_cls)
        return new_cls


class _EngineBase(metaclass=RegisteredEngine):
    """
    The Base Class for all data uploader engines.

    __init__:
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
    """

    def __init__(
        self,
        channel: str,
        api_key: str,
        batch_size: int = MAX_BATCH_SIZE,
        max_num_of_trials: int = 100,
        current_count: int = 0,
    ):
        """
        Args:
            channel (str): tag in `dev`, `staging`, `prod` or custom endpoint
            api_key (str): app api key
            batch_size (int, optional): batch size of inputs. Defaults to MAX_BATCH_SIZE.
            max_num_of_trials (int, optional): max number of trials. Defaults to 100.
            current_count (int, optional): counting starts from `current_count`
        """

        if channel.lower() not in CHANNEL_URLS:
            warnings.warn(
                f"`{channel}` is not in {list(CHANNEL_URLS.keys())}. "
                "It is interpreted as endpoint URL."
            )
            self.channel = channel
        else:
            self.channel = channel.lower()
        self.base_url = CHANNEL_URLS.get(channel.lower(), channel)
        self.api_key = api_key
        self.batch_size = max(int(batch_size), 1)
        self.max_num_of_trials = max(int(max_num_of_trials), 1)
        self.current_count = 0
        self._stub = service_pb2_grpc.V2Stub(
            ClarifaiChannel.get_grpc_channel(base=self.base_url)
        )
        self._buffer = []
        self._request = None
        self._response = None
        self._error_logs = None

    @property
    def metadata(self) -> Tuple[Tuple[str, str]]:
        return (("authorization", f"Key {self.api_key}"),)

    @property
    def buffer_size(self) -> int:
        return len(self._buffer)

    def submit(self):

        if not self._buffer:
            return

        self._request = transform.input_batch_to_request(self._buffer)
        self._response = self._stub.PostInputs(self._request, metadata=self.metadata)
        error_codes_to_messages = {}
        error_codes_statistics = Counter()
        for _ in range(self.max_num_of_trials):
            if self._response.status.code == status_code_pb2.SUCCESS:
                self._reset_buffer()
                return
            error_codes_to_messages[self._response.status.code] = self._response.status
            error_codes_statistics.update([self._response.status.code])
        else:
            self._error_logs = dict(
                messages=error_codes_to_messages, statistics=error_codes_statistics
            )
            raise RuntimeError(
                f"Upload was not successful. "
                f"Max number of trials ({self.max_num_of_trials}) reached."
            )

    def _reset_buffer(self):
        self._buffer = []

    def _check_if_buffer_is_full(self) -> bool:
        return len(self._buffer) == self.batch_size

    def to_proto(self, *args, **kwargs) -> resources_pb2.Input:
        raise NotImplementedError(
            "This method will convert python inputs to proto `resource_pb2.Data`"
        )

    def __call__(self, *args, **kwargs):

        if args:
            raise RuntimeError("Only keyword arguments are allowed.")

        if self._check_if_buffer_is_full():
            self.submit()

        if kwargs:
            self._buffer.append(self.to_proto(**kwargs))
            self.current_count += 1
        else:  # if no kwargs are passed in, do force submit
            self.submit()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        try:
            # force submit the remaining data
            self.submit()
        except RuntimeError as e:
            raise RuntimeError("Unable to close the upload pipeline.") from e

    def __repr__(self) -> str:
        args = []
        args.append(f"channel={self.channel}")
        args.append(f"api_key={self.api_key}")
        args.append(f"batch_size={self.batch_size}")
        args.append(f"current_count={self.current_count}")
        args = ", ".join(args)

        return f"{self.__class__.__name__}({args})"

    def info(self) -> Dict[str, Any]:

        out = {}
        for k, v in self.__dict__.items():
            if k.startswith("_"):
                continue
            out[k] = v

        return out
