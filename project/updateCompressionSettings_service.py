import prisma
import prisma.models
from pydantic import BaseModel


class CompressionSettingsUpdateResponse(BaseModel):
    """
    Response model confirming the updates made to the compression settings.
    """

    success: bool
    message: str


async def updateCompressionSettings(
    algorithm: str, level: int, optimize_for: str
) -> CompressionSettingsUpdateResponse:
    """
    Updates the compression settings based on input parameters. This route is crucial for tailoring the
    compression process to specific needs, such as optimizing for speed or compression ratio. The
    expectations are to provide the new settings in the request, and the response confirms the successful
    update.

    Args:
        algorithm (str): Specifies the compression algorithm to be used.
        level (int): Determines the compression level, where a higher level gives better compression at
                     the cost of speed.
        optimize_for (str): Indicates whether the settings should optimize for speed or compression ratio.

    Returns:
        CompressionSettingsUpdateResponse: Response model confirming the updates made to the compression settings.
    """
    try:
        backup_setting = await prisma.models.Backup.prisma().update(
            where={"CompressionType": "DEFAULT"}, data={"CompressionType": algorithm}
        )
        if backup_setting:
            response = CompressionSettingsUpdateResponse(
                success=True,
                message=f"Compression settings updated to use {algorithm} with level {level} and optimized for {optimize_for}.",
            )
        else:
            response = CompressionSettingsUpdateResponse(
                success=False, message="Failed to update compression settings."
            )
    except Exception as e:
        response = CompressionSettingsUpdateResponse(
            success=False, message=f"An error occurred: {str(e)}"
        )
    return response
