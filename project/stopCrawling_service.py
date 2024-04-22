from datetime import datetime
from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CrawlingSessionDetails(BaseModel):
    """
    Detailed information about the crawling session being stopped, including status and end time.
    """

    status: str
    endTime: Optional[datetime] = None


class CrawlingStopResponse(BaseModel):
    """
    Provides confirmation and details about stopping a crawling session, including the final state if the request was successful.
    """

    success: bool
    message: str
    crawlingSessionDetails: Optional[CrawlingSessionDetails] = None


async def stopCrawling(crawlingSessionId: Optional[str]) -> CrawlingStopResponse:
    """
    Stops the currently running crawling process. Should confirm whether the stop was successful and the state of the last crawl.

    Args:
        crawlingSessionId (Optional[str]): Optional identifier of the crawling session to be stopped. If omitted, it attempts to stop the currently active session.

    Returns:
        CrawlingStopResponse: Provides confirmation and details about stopping a crawling session, including the final state if the request was successful.
    """
    if crawlingSessionId:
        session = await prisma.models.CrawlingSession.prisma().find_unique(
            where={"id": crawlingSessionId, "status": "active"}
        )
    else:
        session = await prisma.models.CrawlingSession.prisma().find_first(
            where={"status": "active"}, order={"startTime": "desc"}
        )
    if not session:
        return CrawlingStopResponse(
            success=False, message="No active crawling session found."
        )
    updated_session = await prisma.models.CrawlingSession.prisma().update(
        where={"id": session.id}, data={"status": "stopped", "endTime": datetime.now()}
    )
    if updated_session:
        return CrawlingStopResponse(
            success=True,
            message="Crawling session stopped successfully.",
            crawlingSessionDetails=CrawlingSessionDetails(
                status=updated_session.status, endTime=updated_session.endTime
            ),
        )
    else:
        return CrawlingStopResponse(
            success=False, message="Failed to stop the crawling session."
        )
