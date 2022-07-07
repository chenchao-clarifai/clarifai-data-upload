import warnings
from typing import Tuple

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

CHANNEL_URLS = {
    "prod": "api.clarifai.com",
    "dev": "api-dev.clarifai.com",
    "staging": "api-staging.clarifai.com",
}


class _EngineBase:
    def __init__(self, channel: str, api_key: str, batch_size: int = 100):

        if channel.lower() not in CHANNEL_URLS:
            warnings.warn(
                f"`{channel}` is not in {list(CHANNEL_URLS.keys())}."
                "It is interpreted as endpoint URL."
            )
            self.channel = channel
        else:
            self.channel = channel.lower()
        self.base_url = CHANNEL_URLS.get(channel.lower(), channel)
        self.api_key = api_key
        self.batch_size = max(batch_size, 1)
        self._stub = service_pb2_grpc.V2Stub(
            ClarifaiChannel.get_grpc_channel(base=self.base_url)
        )
        self._buffer = []
        self._request = None
        self._response = None

    @property
    def metadata(self) -> Tuple[Tuple[str, str]]:
        return (("authorization", f"Key {self.api_key}"),)

    @property
    def count(self) -> int:
        return len(self._buffer)

    def submit(self):

        if not self._buffer:
            return

        self._request = service_pb2.PostInputsRequest(inputs=self._buffer)
        self._response = self._stub.PostInputs(self._request, metadata=self.metadata)
        if self._response.status.code == status_code_pb2.SUCCESS:
            self._reset_buffer()
        else:
            raise RuntimeError(
                f"Upload is not successful (status code: {self._response.status})"
            )

    def _reset_buffer(self):
        self._buffer = []

    def _check_if_buffer_is_full(self) -> bool:
        return len(self._buffer) == self.batch_size

    def to_proto(self, *args, **kwargs) -> resources_pb2.Data:
        raise NotImplementedError(
            "This method will convert python inputs to proto `resource_pb2.Data`"
        )

    def __call__(self, *args, **kwargs):

        if args:
            raise RuntimeError("Only keyword arguments are allowed.")

        if self._check_if_buffer_is_full():
            self.submit()

        data = self.to_proto(**kwargs)
        self._buffer.append(resources_pb2.Input(data=data))

    def __repr__(self) -> str:
        args = []
        args.append(f"channel={self.channel}")
        args.append(f"api_key={self.api_key}")
        args.append(f"batch_size={self.batch_size}")
        args = ", ".join(args)

        return f"{self.__class__.__name__}({args})"

    def info(self) -> str:

        out = []
        for k, v in self.__dict__.items():
            out.append(f"{k}: {v}")

        return "\n".join(out)
