from clarifai_grpc.grpc.api import resources_pb2


def label_to_concept_proto(
    label_name: str, label_value: float = 1.0
) -> resources_pb2.Concept:
    label_name = label_name.strip()
    if " " in label_name:
        kwargs = dict(
            id=label_name.replace(" ", "-"), name=label_name, value=label_value
        )
    else:
        kwargs = dict(id=label_name, name=label_name, value=label_value)

    return resources_pb2.Concept(**kwargs)
