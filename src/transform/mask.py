from clarifai_grpc.grpc.api import resources_pb2


def zip_concept_and_mask_to_region(
    concept: resources_pb2.Concept, mask: resources_pb2.Image
):
    region = resources_pb2.Region(
        region_info=resources_pb2.RegionInfo(
            mask=resources_pb2.Mask(image=mask),
            data=resources_pb2.Data(concepts=[concept]),
        )
    )
    return region
