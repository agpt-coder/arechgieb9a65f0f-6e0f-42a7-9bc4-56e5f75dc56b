from datetime import datetime
from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetBackupsRequest(BaseModel):
    """
    Request model for fetching all backups. This endpoint does not require any specific input parameters as it retrieves a list of all backups.
    """

    pass


class BackupDetails(BaseModel):
    """
    Detailed model representing individual backups.
    """

    id: str
    date: datetime
    status: str


class BackupListingResponse(BaseModel):
    """
    Response model representing a list of all backups. Provides essential details like ID, date, and status to monitor the backup situations efficiently.
    """

    backups: List[BackupDetails]


async def listBackups(request: GetBackupsRequest) -> BackupListingResponse:
    """
    Retrieves a list of all backup records. Each record provides the backup ID, date, and status. This allows system administrators and backup operators to monitor the backup states.

    Args:
    request (GetBackupsRequest): Request model for fetching all backups. This endpoint does not require any specific input parameters as it retrieves a list of all backups.

    Returns:
    BackupListingResponse: Response model representing a list of all backups. Provides essential details like ID, date, and status to monitor the backup situations efficiently.
    """
    backup_records = await prisma.models.Backup.prisma().find_many(
        order={"timestamp": "desc"}
    )
    backup_details_list = [
        BackupDetails(id=record.id, date=record.timestamp, status=record.status)
        for record in backup_records
    ]
    response = BackupListingResponse(backups=backup_details_list)
    return response
