from typing import Dict, List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CrawledDataModel(BaseModel):
    """
    Model representing the structured data of a crawled web session.
    """

    id: str
    data: Dict
    compressionType: Optional[str] = None
    crawlingSessionId: str
    archivedResourceId: str


class GetWebDataOutput(BaseModel):
    """
    Output model containing a list of web data entries for the specified page, along with pagination details.
    """

    data: List[CrawledDataModel]
    totalPages: int
    currentPage: int
    totalEntries: int


async def getAllWebData(page: int, pageSize: int) -> GetWebDataOutput:
    """
    Retrieves all stored web data in a paginated response. Primarily used for oversight and backup purposes.
    Returns a list of web data entries.

    Args:
        page (int): Specifies the page number in the pagination sequence.
        pageSize (int): Specifies the number of items per page.

    Returns:
        GetWebDataOutput: Output model containing a list of web data entries for the specified page, along with pagination details.
    """
    skip = (page - 1) * pageSize
    crawled_data_records = await prisma.models.CrawledData.prisma().find_many(
        skip=skip,
        take=pageSize,
        include={"crawledSession": True, "ArchivedResource": True},
    )
    crawled_data_models = [
        CrawledDataModel(
            id=data.id,
            data=data.data,
            compressionType=data.compressionType,
            crawlingSessionId=data.crawledSession.id if data.crawledSession else None,
            archivedResourceId=data.ArchivedResource.id
            if data.ArchivedResource
            else None,
        )
        for data in crawled_data_records
    ]
    total_entries = await prisma.models.CrawledData.prisma().count()
    total_pages = (total_entries + pageSize - 1) // pageSize
    output = GetWebDataOutput(
        data=crawled_data_models,
        totalPages=total_pages,
        currentPage=page,
        totalEntries=total_entries,
    )
    return output
