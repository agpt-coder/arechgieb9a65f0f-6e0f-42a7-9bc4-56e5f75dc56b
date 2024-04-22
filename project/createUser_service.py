import prisma
import prisma.models
from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    """
    Response model for the user creation endpoint. Contains the user ID of the newly created user and a success message.
    """

    user_id: str
    message: str


class Role(BaseModel):
    """
    Role enum model that defines different role types in the system.
    """

    SYSTEM_ADMINISTRATOR: str = "SYSTEM_ADMINISTRATOR"
    DATA_MANAGER: str = "DATA_MANAGER"
    USER: str = "USER"
    DEVELOPER: str = "DEVELOPER"
    BACKUP_OPERATOR: str = "BACKUP_OPERATOR"


async def createUser(username: str, email: str, role: Role) -> CreateUserResponse:
    """
    This endpoint creates a new user within the system. It expects details like username, email, and roles in the body of the request. Upon successful creation, it returns the user ID along with a success message. This interaction uses the API Access Module for user data validation and storage.

    Args:
        username (str): Desired username for the new user account. Must be unique across the system.
        email (str): Email address for the new user. Must be valid and unique.
        role (Role): Assigned role from predefined roles in the system. Must include SYSTEM_ADMINISTRATOR, DATA_MANAGER, USER, DEVELOPER, or BACKUP_OPERATOR.

    Returns:
        CreateUserResponse: Response model for the user creation endpoint. Contains the user ID of the newly created user and a success message.
    """
    user = await prisma.models.User.prisma().create(
        data={"email": email, "hashedPassword": username, "role": role}
    )
    return CreateUserResponse(
        user_id=user.id,
        message=f"prisma.models.User {username} with email {email} and role {role} created successfully.",
    )
