from enum import Enum

import prisma
import prisma.models
from pydantic import BaseModel


class DeleteWebDataResponse(BaseModel):
    """
    Confirmation of successful deletion of web data.
    """

    success: bool
    message: str


class Role(Enum):
    SYSTEM_ADMINISTRATOR: str = "SYSTEM_ADMINISTRATOR"
    DATA_MANAGER: str = "DATA_MANAGER"
    USER: str = "USER"
    DEVELOPER: str = "DEVELOPER"
    BACKUP_OPERATOR: str = "BACKUP_OPERATOR"


async def deleteWebData(dataId: str, role: Role) -> DeleteWebDataResponse:
    """
    Deletes specific web data by its ID. Necessary for maintaining data relevance and storage management. A success response is returned if the operation is successful.

    Args:
        dataId (str): Unique identifier for the web data to be deleted.
        role (Role): Role of the user to confirm permission for operation.

    Returns:
        DeleteWebDataResponse: Confirmation of successful deletion of web data.
    """
    if role in [Role.SYSTEM_ADMINISTRATOR, Role.DATA_MANAGER]:
        crawled_data = await prisma.models.CrawledData.prisma().find_unique(
            where={"id": dataId}
        )
        if crawled_data:
            await prisma.models.CrawledData.prisma().delete(where={"id": dataId})
            return DeleteWebDataResponse(
                success=True, message="Web data successfully deleted."
            )
        else:
            return DeleteWebDataResponse(success=False, message="Web data not found.")
    else:
        return DeleteWebDataResponse(
            success=False,
            message="Permission denied. Only administrators and data managers can delete web data.",
        )
