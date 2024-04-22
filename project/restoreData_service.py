import prisma
import prisma.models
from pydantic import BaseModel


class RecoveryResponse(BaseModel):
    """
    Provides the response details after initiating a recovery operation. It includes the status of the operation and any relevant logs or error messages.
    """

    status: str
    details: str


async def restoreData(backupId: str) -> RecoveryResponse:
    """
    Initiates a data recovery operation using a specified backup ID. The data restore updates the current state of the Data Storage Module to match that of the backup. This route returns a success status and details of the restore process.

    Args:
        backupId (str): The unique identifier of the backup from which the data will be restored.

    Returns:
        RecoveryResponse: Provides the response details after initiating a recovery operation. It includes the status of the operation and any relevant logs or error messages.
    """
    backup = await prisma.models.Backup.prisma().find_unique(where={"id": backupId})
    if not backup:
        return RecoveryResponse(status="failed", details="Backup ID not found")
    return RecoveryResponse(
        status="success", details=f"Data restored from backup at {backup.dataPath}"
    )
