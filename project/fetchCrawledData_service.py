from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class FetchCrawledDataRequest(BaseModel):
    """
    This model represents the input required to fetch crawled data. Currently, no specific input parameters are needed as the endpoint retrieves all available crawled data.
    """

    pass


class CrawledData(BaseModel):
    """
    Model representing data collected during a crawling session.
    """

    id: str
    data: Dict
    compressionType: Optional[str] = None
    crawlingSessionId: str
    archivedResourceId: Optional[str] = None


class FetchCrawledDataResponse(BaseModel):
    """
    This model represents the output after fetching crawled data, providing an array of CrawledData objects.
    """

    data: List[CrawledData]


async def fetchCrawledData(
    request: FetchCrawledDataRequest,
) -> FetchCrawledDataResponse:
    """
    Retrieves crawled data stored by the module. It interacts with the Data Storage Module for fetching the data. Response should include the fetched data.

    Args:
    request (FetchCrawledDataRequest): This model represents the input required to fetch crawled data.
    Currently, no specific input parameters are needed as the endpoint retrieves all available crawled data.

    Returns:
    FetchCrawledDataResponse: This model represents the output after fetching crawled data, providing an array of CrawledData objects.

    Implementation fetches all CrawledData entries from the database, using Prisma ORM.
    """
    crawled_data_entries = await prisma.models.CrawledData.prisma().find_many(
        include={"crawledSession": True, "ArchivedResource": True}
    )
    response_data = [
        CrawledData(
            id=entry.id,
            data=entry.data,
            compressionType=entry.compressionType,
            crawlingSessionId=entry.crawledSession.id,
            archivedResourceId=entry.ArchivedResource.id
            if entry.ArchivedResource
            else None,
        )
        for entry in crawled_data_entries
    ]
    return FetchCrawledDataResponse(data=response_data)
