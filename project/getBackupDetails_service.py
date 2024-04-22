from datetime import datetime
from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class BackupLog(BaseModel):
    """
    A model describing log entries that are associated with a backup operation.
    """

    id: str
    log: str
    createdAt: datetime
    backupId: str


class BackupDetailsResponse(BaseModel):
    """
    API response model providing detailed information regarding a specific backup, including size, timestamp, and status.
    """

    id: str
    timestamp: datetime
    dataPath: str
    status: str
    size: int
    CompressionType: Optional[str] = None
    BackupLogs: List[BackupLog]


async def getBackupDetails(backupId: str) -> BackupDetailsResponse:
    """
    Fetches the details of a specific backup using the backup ID, including the data size, backup date, and any errors encountered. Essential for detailed diagnostics and backup verification.

    Args:
        backupId (str): The unique identifier for a backup from which details are to be retrieved.

    Returns:
        BackupDetailsResponse: API response model providing detailed information regarding a specific backup, including size, timestamp, and status.

    Example:
        backup_details = await getBackupDetails("123e4567-e89b-12d3-a456-426614174000")
        print(backup_details)
    """
    backup = await prisma.models.Backup.prisma().find_unique(
        where={"id": backupId}, include={"BackupLogs": True}
    )
    if not backup:
        raise ValueError("No backup found with provided backup ID.")
    details = BackupDetailsResponse(
        id=backup.id,
        timestamp=backup.timestamp,
        dataPath=backup.dataPath,
        status=backup.status,
        size=backup.size,
        CompressionType=backup.CompressionType,
        BackupLogs=[
            BackupLog(
                id=log.id, log=log.log, createdAt=log.createdAt, backupId=log.backupId
            )
            for log in backup.BackupLogs
        ],
    )
    return details
