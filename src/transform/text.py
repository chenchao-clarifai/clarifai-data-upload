from clarifai_grpc.grpc.api import resources_pb2


def raw_text_to_proto(text) -> resources_pb2.Text:
    return resources_pb2.Text(raw=text)
