from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateBackupResponse(BaseModel):
    """
    Provides feedback on the backup creation attempt, including an identifier for the newly created backup for future reference.
    """

    success: bool
    backup_id: str
    message: str


async def createBackup(
    data_identifier: str, compression_type: Optional[str]
) -> CreateBackupResponse:
    """
    Creates a backup of the data. This route triggers the backup process in the Data Storage Module, storing the backup data possibly in a separate storage solution. The API should return a success status and a backup ID.

    Args:
        data_identifier (str): Identifies the specific data to be backed up, like a user ID or data block identifier.
        compression_type (Optional[str]): Specifies the type of compression to use for this backup, possibly improving storage efficiency.

    Returns:
        CreateBackupResponse: Provides feedback on the backup creation attempt, including an identifier for the newly created backup for future reference.
    """
    try:
        new_backup = await prisma.models.Backup.prisma().create(
            {
                "dataPath": data_identifier,
                "status": "success",
                "CompressionType": compression_type,
            }
        )
        _ = await prisma.models.BackupLog.prisma().create(
            {
                "log": "Backup created successfully for data identifier: {}".format(
                    data_identifier
                ),
                "backupId": new_backup.id,
            }
        )
        response = CreateBackupResponse(
            success=True,
            backup_id=new_backup.id,
            message="Backup successfully created.",
        )
    except Exception as e:
        response = CreateBackupResponse(success=False, backup_id="", message=str(e))
    return response
