from typing import List

from clarifai_grpc.grpc.api import resources_pb2, service_pb2


def _to_data(**kwargs) -> resources_pb2.Data:
    return resources_pb2.Data(**kwargs)


def _to_input(input_id: str, data: resources_pb2.Data) -> resources_pb2.Input:
    return resources_pb2.Input(id=input_id, data=data)


def _to_annotation(input_id: str, data: resources_pb2.Data) -> resources_pb2.Annotation:
    return resources_pb2.Annotation(input_id=input_id, data=data)


def to_input(**kwargs) -> resources_pb2.Input:
    input_id = kwargs.pop("id", "none")
    return _to_input(input_id, _to_data(**kwargs))


def to_annotation(**kwargs) -> resources_pb2.Annotation:
    input_id = kwargs.pop("input_id", "none")
    return _to_annotation(input_id, _to_data(**kwargs))


def input_batch_to_request(
    batch: List[resources_pb2.Input],
) -> service_pb2.PostInputsRequest:
    return service_pb2.PostInputsRequest(inputs=batch)


def annotation_batch_to_request(
    batch: List[resources_pb2.Annotation],
) -> service_pb2.PostAnnotationsRequest:
    return service_pb2.PostAnnotationsRequest(annotations=batch)
