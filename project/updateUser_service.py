from datetime import datetime

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class UpdateUserResponse(BaseModel):
    """
    Response model indicating the result of the update operation or potential errors.
    """

    success: bool
    userId: str
    message: str


async def updateUser(
    userId: str, email: str, password: str, role: prisma.enums.Role
) -> UpdateUserResponse:
    """
    Updates details for a specific user. It securely updates user data in the Data Storage Module based on the provided userId and input data. Returns the updated user information upon successful update.

    Args:
        userId (str): The unique identifier of the user to be updated.
        email (str): New email address for the user, must be unique across the system.
        password (str): New hashed password for secure authentication.
        role (prisma.enums.Role): New role of the user, constrained to specified enums for role.

    Returns:
        UpdateUserResponse: Response model indicating the result of the update operation or potential errors.
    """
    try:
        exist_user = await prisma.models.User.prisma().find_many(
            where={"email": email, "NOT": {"id": userId}}
        )
        if exist_user:
            return UpdateUserResponse(
                success=False,
                userId=userId,
                message="Another user with the same email already exists.",
            )
        updated_user = await prisma.models.User.prisma().update(
            where={"id": userId},
            data={
                "email": email,
                "hashedPassword": password,
                "role": role,
                "updatedAt": datetime.now(),
            },
        )
        if updated_user:
            return UpdateUserResponse(
                success=True,
                userId=userId,
                message="User details successfully updated.",
            )
        else:
            return UpdateUserResponse(
                success=False, userId=userId, message="Failed to update user details."
            )
    except Exception as error:
        return UpdateUserResponse(success=False, userId=userId, message=str(error))
