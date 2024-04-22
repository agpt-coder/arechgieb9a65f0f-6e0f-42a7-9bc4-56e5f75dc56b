from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CrawlingConfigUpdateResponse(BaseModel):
    """
    This model provides confirmation that the crawling configuration has been updated with the new settings.
    """

    success: bool
    message: str


async def updateCrawlingConfig(
    crawl_depth: Optional[int],
    pause_duration: Optional[float],
    target_domains: Optional[List[str]],
) -> CrawlingConfigUpdateResponse:
    """
    Updates configurations used for the crawling process, such as crawl depth, pause duration, and target domains. Response confirms the application of new settings.

    Args:
        crawl_depth (Optional[int]): The maximal depth the crawler should go relative to the start page. If not specified, it defaults to its current setting.
        pause_duration (Optional[float]): Specifies the length of the pause between processing two consecutive URLs in seconds. Used to prevent high server load.
        target_domains (Optional[List[str]]): List of domains targeted for crawling. This overrides any previously set domains.

    Returns:
        CrawlingConfigUpdateResponse: This model provides confirmation that the crawling configuration has been updated with the new settings.
    """
    try:
        active_session = await prisma.models.CrawlingSession.prisma().find_first(
            where={"status": "active"}
        )
        if not active_session:
            return CrawlingConfigUpdateResponse(
                success=False, message="No active crawling session found."
            )
        updated_fields = {}
        if crawl_depth is not None:
            updated_fields["crawlingDepth"] = crawl_depth
        if pause_duration is not None:
            updated_fields["pauseDuration"] = pause_duration
        if target_domains is not None:
            updated_fields["targetDomains"] = target_domains
        await prisma.models.CrawlingSession.prisma().update(
            where={"id": active_session.id}, data=updated_fields
        )
        return CrawlingConfigUpdateResponse(
            success=True, message="Crawling settings successfully updated."
        )
    except Exception as e:
        return CrawlingConfigUpdateResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )
