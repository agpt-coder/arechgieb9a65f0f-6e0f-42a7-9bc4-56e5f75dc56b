from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserDetail(BaseModel):
    """
    Detailed information of a user, suitable for listing purposes.
    """

    id: str
    username: str
    role: str
    created_at: datetime


class GetUsersResponse(BaseModel):
    """
    The response model returning a list of users with their basic data, designed for administrative purposes.
    """

    users: List[UserDetail]
    total_count: int
    page: int
    limit: int


async def listUsers(
    page: Optional[int] = None, limit: Optional[int] = None, sort: Optional[str] = None
) -> GetUsersResponse:
    """
    Retrieves a list of all users. User data is fetched from the Data Storage Module, and this route is commonly used to manage users or retrieve a complete user listing. Response includes an array of user data.

    Args:
        page (Optional[int]): The page number for pagination, starting from 1.
        limit (Optional[int]): The number of user entries per page. Defaults to a sensible value if not specified.
        sort (Optional[str]): The sorting parameter which could be any of the user attributes like 'createdAt' or 'email', optionally prefixed with +/- for ascending/descending order.

    Returns:
        GetUsersResponse: The response model returning a list of users with their basic data, designed for administrative purposes.
    """
    if page is None:
        page = 1
    if limit is None:
        limit = 10
    order_query = None
    if sort:
        sort_direction = "asc" if not sort.startswith("-") else "desc"
        attribute = sort[1:] if sort.startswith("-") else sort
        order_query = {attribute: sort_direction}
    users = await prisma.models.User.prisma().find_many(
        skip=(page - 1) * limit, take=limit, order=order_query
    )
    count = await prisma.models.User.prisma().count()
    user_details = [
        UserDetail(
            id=user.id, username=user.email, role=user.role, created_at=user.createdAt
        )
        for user in users
    ]
    return GetUsersResponse(
        users=user_details, total_count=count, page=page, limit=limit
    )
