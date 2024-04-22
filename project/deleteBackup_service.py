import prisma
import prisma.models
from pydantic import BaseModel


class DeleteBackupResponse(BaseModel):
    """
    Response model indicating the result of the delete operation, including messages for success or failure.
    """

    success: bool
    message: str


async def deleteBackup(backupId: str) -> DeleteBackupResponse:
    """
    Deletes a specific backup by its backup ID, removing it from the storage. Used to manage storage and delete old or unnecessary backups, ensuring efficient use of resources.

    Args:
    backupId (str): Unique identifier for the backup to be deleted.

    Returns:
    DeleteBackupResponse: Response model indicating the result of the delete operation, including messages for success or failure.

    Example:
        deleteBackup("some_unique_backup_id")
        > DeleteBackupResponse(success=True, message="prisma.models.Backup successfully deleted.")
    """
    backup = await prisma.models.Backup.prisma().find_unique(where={"id": backupId})
    if not backup:
        return DeleteBackupResponse(
            success=False, message=f"No backup found with ID: {backupId}"
        )
    await prisma.models.Backup.prisma().delete(where={"id": backupId})
    return DeleteBackupResponse(
        success=True, message="prisma.models.Backup successfully deleted."
    )
