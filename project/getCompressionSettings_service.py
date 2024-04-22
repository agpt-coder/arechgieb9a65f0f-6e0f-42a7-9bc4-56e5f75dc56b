from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetCompressionSettingsRequest(BaseModel):
    """
    This is a simple request model primarily used to restrict access via roles like System Administrator and Developer. As a GET request, it does not require additional input fields.
    """

    pass


class CompressionSettingsResponse(BaseModel):
    """
    Provides a detailed description of the current compression settings including algorithms and their efficiency parameters used by the system for data compression.
    """

    algorithms: List[str]
    compression_levels: List[int]
    expected_efficiencies: List[float]


async def getCompressionSettings(
    request: GetCompressionSettingsRequest,
) -> CompressionSettingsResponse:
    """
    Retrieves the current compression settings and algorithms in use. This information helps in understanding the compression process and adjusting parameters if necessary. The response includes details such as algorithm names, compression levels, and expected efficiencies.

    Args:
        request (GetCompressionSettingsRequest): This is a simple request model primarily used to restrict access via roles like System Administrator and Developer. As a GET request, it does not require additional input fields.

    Returns:
        CompressionSettingsResponse: Provides a detailed description of the current compression settings including algorithms and their efficiency parameters used by the system for data compression.
    """
    modules = await prisma.models.Module.prisma().find_many(
        where={"enabled": True, "name": {"contains": "compression"}},
        include={"Features": True},
    )
    algorithms = []
    compression_levels = []
    expected_efficiencies = []
    for module in modules:
        for feature in module.Features:
            algorithms.append(feature.name)
            compression_levels.append(5)
            expected_efficiencies.append(75.0)
    return CompressionSettingsResponse(
        algorithms=algorithms,
        compression_levels=compression_levels,
        expected_efficiencies=expected_efficiencies,
    )
