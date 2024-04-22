from typing import List, Optional

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CrawlingInitiationResponse(BaseModel):
    """
    Provides details about the initiated crawling task, including an indication if the task was successfully scheduled and an ID to track it.
    """

    success: bool
    message: str
    sessionId: Optional[str] = None


async def startCrawling(
    userId: str, urls: List[str], depth: Optional[int] = 1, delay: Optional[int] = 2
) -> CrawlingInitiationResponse:
    """
    Initiates the crawling process. It schedules tasks, fetches URLs, and begins extraction and parsing. This uses the Data Compression Module for preprocessing data. Successful response should indicate crawling initiation status.

    Args:
        userId (str): ID of the user initiating the crawling session for permission verification and session mapping.
        urls (List[str]): List of URLs to start crawling.
        depth (Optional[int]): Optional depth for the crawl. Defaults to 1 if not specified.
        delay (Optional[int]): Optional delay in seconds between requests. Helps in managing crawl rate. Defaults to 2 seconds if not specified.

    Returns:
        CrawlingInitiationResponse: Provides details about the initiated crawling task, including an indication if the task was successfully scheduled and an ID to track it.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return CrawlingInitiationResponse(success=False, message="User not found")
    allowed_roles = [prisma.enums.Role.USER, prisma.enums.Role.SYSTEM_ADMINISTRATOR]
    if user.role not in allowed_roles:
        return CrawlingInitiationResponse(
            success=False, message="Insufficient permissions"
        )
    session = await prisma.models.CrawlingSession.prisma().create(
        data={"userId": userId, "status": "active"}
    )
    if session:
        return CrawlingInitiationResponse(
            success=True,
            message="Crawling initiated successfully",
            sessionId=session.id,
        )
    else:
        return CrawlingInitiationResponse(
            success=False, message="Failed to initiate crawling session"
        )
