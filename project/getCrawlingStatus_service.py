from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetCrawlingStatusRequest(BaseModel):
    """
    Request model for getting the current or recent crawling session status. This operation does not require specific input parameters as it retrieves the general current status.
    """

    pass


class GetCrawlingStatusResponse(BaseModel):
    """
    This model details the response for the crawling status, providing metrics and error messages alongside identifiers for further querying if needed.
    """

    currentSessionId: str
    numPagesProcessed: int
    currentURLs: List[str]
    errors: List[str]
    status: str


async def getCrawlingStatus(
    request: GetCrawlingStatusRequest,
) -> GetCrawlingStatusResponse:
    """
    Provides current status of the crawling process, including the number of pages processed, current URLs being crawled, and any errors. Expected response includes status details.

    This function queries the most recent or currently active CrawlingSession from the database and constructs a response based on the session data and related crawled data.

    Args:
        request (GetCrawlingStatusRequest): Request model for getting the current or recent crawling session status. This operation does not require specific input parameters as it retrieves the general current status.

    Returns:
        GetCrawlingStatusResponse: This model details the response for the crawling status, providing metrics and error messages alongside identifiers for further querying if needed.
    """
    sessions = await prisma.models.CrawlingSession.prisma().find_many(
        take=1,
        order={"startTime": "desc"},
        include={"CrawledData": {"include": {"ArchivedResource": True}}},
    )
    if not sessions:
        return GetCrawlingStatusResponse(
            currentSessionId="",
            numPagesProcessed=0,
            currentURLs=[],
            errors=[],
            status="no active session",
        )
    session = sessions[0]
    num_pages_processed = len(session.CrawledData)
    current_urls = [
        cdata.ArchivedResource.resourceUrl
        for cdata in session.CrawledData
        if cdata.ArchivedResource
    ]
    errors = [
        log
        for cdata in session.CrawledData
        for log in cdata.ArchivedResource.CrawledData
        if log
    ]
    return GetCrawlingStatusResponse(
        currentSessionId=session.id,
        numPagesProcessed=num_pages_processed,
        currentURLs=current_urls,
        errors=errors,
        status=session.status,
    )
