import prisma
import prisma.models
from pydantic import BaseModel


class DeleteUserResponse(BaseModel):
    """
    This response model confirms whether the user was successfully removed or not. It provides feedback in the form of a message.
    """

    success: bool
    message: str


async def deleteUser(userId: str) -> DeleteUserResponse:
    """
    Removes a user from the system using the specified userId. A successful operation will confirm the user's removal. The API Access Module handles this to maintain data integrity and log the action for security compliance.

    Args:
        userId (str): The unique identifier of the user to be removed.

    Returns:
        DeleteUserResponse: This response model confirms whether the user was successfully removed or not. It provides feedback in the form of a message.
    """
    user = await prisma.models.User.prisma().find_unique(where={"id": userId})
    if user is None:
        return DeleteUserResponse(
            success=False, message="No user found with the provided userId."
        )
    await prisma.models.User.prisma().delete(where={"id": userId})
    return DeleteUserResponse(success=True, message="User successfully deleted.")
