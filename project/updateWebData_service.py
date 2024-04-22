from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UpdateWebDataResponse(BaseModel):
    """
    Responds with the updated web data object upon success or specifies the failure reason.
    """

    updatedData: Dict[str, Any]


async def updateWebData(
    dataId: str, new_content: Dict[str, Any], compressionType: Optional[str]
) -> UpdateWebDataResponse:
    """
    Updates existing web data by its ID with new content received from the Crawling Module. Validates changes and confirms update success. Returns the updated data object.

    Args:
        dataId (str): Identifier for the web data to be updated.
        new_content (Dict[str, Any]): New content to update the existing web data.
        compressionType (Optional[str]): Optional compression type of the new content.

    Returns:
        UpdateWebDataResponse: Responds with the updated web data object upon success or specifies the failure reason.
    """
    crawled_data = await prisma.models.CrawledData.prisma().find_unique(
        where={"id": dataId}
    )
    if crawled_data is None:
        return UpdateWebDataResponse(updatedData={"error": "Data not found"})
    updated_crawled_data = await prisma.models.CrawledData.prisma().update(
        where={"id": dataId},
        data={"data": new_content, "compressionType": compressionType},
    )
    response = UpdateWebDataResponse(updatedData=updated_crawled_data.data)
    return response
