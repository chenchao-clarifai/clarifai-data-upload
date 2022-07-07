from typing import List

from clarifai_grpc.grpc.api import resources_pb2, service_pb2


def _to_data(**kwargs) -> resources_pb2.Data:
    return resources_pb2.Data(**kwargs)


def _to_input(data: resources_pb2.Data) -> resources_pb2.Input:
    return resources_pb2.Input(data=data)


def to_input(**kwargs) -> resources_pb2.Input:
    return _to_input(_to_data(**kwargs))


def input_batch_to_request(
    input_batch: List[resources_pb2.Input],
) -> service_pb2.PostInputsRequest:
    return service_pb2.PostInputsRequest(inputs=input_batch)
