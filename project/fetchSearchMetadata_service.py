from datetime import datetime
from typing import Dict, List

import prisma
import prisma.models
from pydantic import BaseModel


class GetSearchMetadataRequest(BaseModel):
    """
    Request model for fetching search-related metadata. No direct inputs required as the data is extracted directly from the database based on available content and user permissions.
    """

    pass


class FilterOption(BaseModel):
    """
    Defines a single filter option available for the search functionality.
    """

    filter_name: str
    options: List[str]


class DateRange(BaseModel):
    """
    Date range from minimum to maximum with inclusive boundaries.
    """

    min_date: datetime
    max_date: datetime


class GetSearchMetadataResponse(BaseModel):
    """
    Provides dynamically generated metadata for search interfaces based on the existing archived content and user roles.
    """

    filters: List[FilterOption]
    role_based_access: Dict[str, List[str]]
    date_range: DateRange


async def fetchSearchMetadata(
    request: GetSearchMetadataRequest,
) -> GetSearchMetadataResponse:
    """
    Provides metadata necessary for front-end components to render search interfaces effectively, such as available filters and search criteria options. This endpoint directly interacts with the Data Storage Module to ensure up-to-date metadata is always provided. It helps in providing dynamic search options based on the data available.

    Args:
        request (GetSearchMetadataRequest): Request model for fetching search-related metadata. No direct inputs required as the data is extracted directly from the database based on available content and user permissions.

    Returns:
        GetSearchMetadataResponse: Provides dynamically generated metadata for search interfaces based on the existing archived content and user roles.
    """
    crawled_data_items = await prisma.models.CrawledData.prisma().find_many(
        include={"ArchivedResource": True}
    )
    resource_types = set()
    compression_types = set()
    min_date = datetime.max
    max_date = datetime.min
    for item in crawled_data_items:
        if "type" in item.ArchivedResource.data:
            resource_types.add(item.ArchivedResource.data["type"])
        if item.compressionType:
            compression_types.add(item.compressionType)
        resource_date = item.ArchivedResource.createdAt
        min_date = min(min_date, resource_date)
        max_date = max(max_date, resource_date)
    filters = [
        FilterOption(filter_name="Resource Type", options=list(resource_types)),
        FilterOption(filter_name="Compression Type", options=list(compression_types)),
    ]
    date_range = DateRange(min_date=min_date, max_date=max_date)
    role_based_access = {
        "SYSTEM_ADMINISTRATOR": ["create", "delete", "modify"],
        "DATA_MANAGER": ["view", "archive"],
        "USER": ["view"],
        "DEVELOPER": ["debug"],
        "BACKUP_OPERATOR": ["backup", "restore"],
    }
    return GetSearchMetadataResponse(
        filters=filters, role_based_access=role_based_access, date_range=date_range
    )
