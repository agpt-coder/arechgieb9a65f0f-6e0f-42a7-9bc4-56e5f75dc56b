from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class SearchResult(BaseModel):
    """
    A model that represents a single search result, which includes identifiers and metadata.
    """

    id: str
    title: str
    summary: str
    date: str
    content_type: str


class SearchResponseModel(BaseModel):
    """
    Model that defines the structure of the paginated search results returned from the server.
    """

    results: List[SearchResult]
    total_results: int
    current_page: int
    total_pages: int


async def searchArchivedContent(
    keywords: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    content_type: Optional[str],
    page: Optional[int],
    page_size: Optional[int],
) -> SearchResponseModel:
    """
    Allows users to search the archived content using various criteria such as keywords, date ranges, and content types.
    This route fetches data using the Data Storage Module. The response includes a paginated list of search results tailored to the query parameters provided by the user.

    Args:
        keywords (Optional[str]): Keywords used for searching in archived content.
        start_date (Optional[str]): The starting date of the date range for which to include the search results.
        end_date (Optional[str]): The end date of the date range for which to include the search results.
        content_type (Optional[str]): The types of content to include in the search, such as text, images, etc.
        page (Optional[int]): The pagination index for the search results.
        page_size (Optional[int]): The number of results per page.

    Returns:
        SearchResponseModel: Model that defines the structure of the paginated search results returned from the server.
    """
    page = page or 1
    page_size = page_size or 10
    where_conditions = {}
    if keywords:
        where_conditions["ArchivedResource"] = {"resourceUrl": {"contains": keywords}}
    if start_date and end_date:
        where_conditions["createdAt"] = {
            "gte": datetime.strptime(start_date, "%Y-%m-%d"),
            "lte": datetime.strptime(end_date, "%Y-%m-%d"),
        }
    if content_type:
        where_conditions["compressionType"] = {"equals": content_type}
    crawled_data = await prisma.models.CrawledData.prisma().find_many(
        skip=(page - 1) * page_size,
        take=page_size,
        where=where_conditions,
        include={"ArchivedResource": True},
    )
    search_results = []
    for data in crawled_data:
        arch_res = data.ArchivedResource
        search_results.append(
            SearchResult(
                id=arch_res.id,
                title=arch_res.resourceUrl,
                summary=arch_res.data.get("summary", "No summary available"),
                date=arch_res.createdAt.strftime("%Y-%m-%d"),
                content_type=data.compressionType or "unknown",
            )
        )  # TODO(autogpt): Cannot access member "get" for type "Json"
    #     Member "get" is unknown. reportAttributeAccessIssue
    total_results = await prisma.models.CrawledData.prisma().count(
        where=where_conditions
    )
    total_pages = (total_results + page_size - 1) // page_size
    return SearchResponseModel(
        results=search_results,
        total_results=total_results,
        current_page=page,
        total_pages=total_pages,
    )
