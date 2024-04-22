from typing import Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CrawledData(BaseModel):
    """
    Model representing data collected during a crawling session.
    """

    id: str
    data: Dict
    compressionType: Optional[str] = None
    crawlingSessionId: str
    archivedResourceId: Optional[str] = None


class GetWebDataByIdResponse(BaseModel):
    """
    Response model that returns details of the web data if found, otherwise returns a not found error.
    """

    data: CrawledData


async def getWebData(dataId: str) -> GetWebDataByIdResponse:
    """
    Retrieves specific web data by its ID. Used to fetch data for the Search Engine Module or for administrative purposes. Returns JSON object of the web data if found or a not found error if no such data exists.

    Args:
    dataId (str): The unique identifier for the web data to be retrieved.

    Returns:
    GetWebDataByIdResponse: Response model that returns details of the web data if found, otherwise returns a not found error.

    This actual implementation will try to find the data from "CrawledData" in the database using the passed 'dataId'.
    If the data exists, it returns it packed into a GetWebDataByIdResponse object. If data does not exist, it returns
    an empty GetWebDataByIdResponse object.
    """
    crawled_data = await prisma.models.CrawledData.prisma().find_unique(
        where={"id": dataId}
    )
    if crawled_data:
        crawled_data_dict = CrawledData(
            id=crawled_data.id,
            data=crawled_data.data,
            compressionType=crawled_data.compressionType,
            crawlingSessionId=crawled_data.crawlingSessionId,
            archivedResourceId=crawled_data.archivedResourceId,
        )
        return GetWebDataByIdResponse(data=crawled_data_dict)
    else:
        return GetWebDataByIdResponse(data=None)
