from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CrawlingSession(BaseModel):
    """
    Model representing a session of internet crawling activities started by a user.
    """

    id: str
    status: str
    startTime: datetime
    endTime: Optional[datetime] = None


class Search(BaseModel):
    """
    Model representing a search query performed by the user.
    """

    id: str
    query: str
    createdAt: datetime


class APIKey(BaseModel):
    """
    Model representing an API key owned by the user.
    """

    id: str
    key: str
    permissions: List[str]
    createdAt: datetime


class UserDetailsResponse(BaseModel):
    """
    A comprehensive user profile including contact information, roles and a summary of user activity across different modules.
    """

    id: str
    email: str
    role: str
    crawling_sessions: List[CrawlingSession]
    searches: List[Search]
    api_keys: List[APIKey]


async def getUserDetails(userId: str) -> UserDetailsResponse:
    """
    Fetches detailed information of a user identified by userId. This includes user contact information, roles, and activity logs. Makes use of the API Access Module to retrieve user data securely. The result is a detailed user profile.

    Args:
    userId (str): The unique identifier for the user. This will be used to fetch the specific user's details.

    Returns:
    UserDetailsResponse: A comprehensive user profile including contact information, roles and a summary of user activity across different modules.
    """
    user = await prisma.models.User.prisma().find_unique(
        where={"id": userId},
        include={"CrawlingSessions": True, "Searches": True, "APIKeys": True},
    )
    if user is None:
        raise ValueError("User with the given ID does not exist.")
    user_details_response = UserDetailsResponse(
        id=user.id,
        email=user.email,
        role=user.role.name,
        crawling_sessions=[
            CrawlingSession(
                id=session.id,
                status=session.status,
                startTime=session.startTime,
                endTime=session.endTime,
            )
            for session in user.CrawlingSessions
        ],
        searches=[
            Search(id=search.id, query=search.query, createdAt=search.createdAt)
            for search in user.Searches
        ],
        api_keys=[
            APIKey(
                id=apikey.id,
                key=apikey.key,
                permissions=apikey.permissions,
                createdAt=apikey.createdAt,
            )
            for apikey in user.APIKeys
        ],
    )
    return user_details_response
