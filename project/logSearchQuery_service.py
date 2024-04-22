from datetime import datetime
from typing import Dict

import prisma
import prisma.models
from pydantic import BaseModel


class SearchLogResponse(BaseModel):
    """
    Confirms the logging of the user's search query along with any additional relevant information.
    """

    success: bool
    message: str


async def logSearchQuery(
    search_query: str, filters: Dict[str, str], user_id: str, timestamp: datetime
) -> SearchLogResponse:
    """
    Logs each user's search query for analysis and improvement of the search engine. It captures detailed information about the search query, including the search terms, filters applied, and timestamp of the search. This data is essential for understanding user behavior and enhancing search functionality.

    Args:
        search_query (str): The main search terms entered by the user.
        filters (Dict[str, str]): Any filters applied during the search, such as date ranges or categories.
        user_id (str): The ID of the user making the search. Automatically captured from the user's session.
        timestamp (datetime): The exact time when the search was made. Automatically captured at the time of request.

    Returns:
        SearchLogResponse: Confirms the logging of the user's search query along with any additional relevant information.
    """
    try:
        await prisma.models.Search.prisma().create(
            data={
                "userId": user_id,
                "query": search_query,
                "createdAt": timestamp,
                "results": {"filters": filters},
            }
        )
        return SearchLogResponse(
            success=True, message="Search has been logged successfully."
        )
    except Exception as e:
        return SearchLogResponse(success=False, message=str(e))
