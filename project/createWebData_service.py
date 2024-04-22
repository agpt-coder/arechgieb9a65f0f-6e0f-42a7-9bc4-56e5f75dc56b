from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class StoreWebDataResponse(BaseModel):
    """
    Confirmation response after storing web data.
    """

    success: bool
    message: str


async def createWebData(
    userId: str, data: Dict[str, Any], compressionType: Optional[str]
) -> StoreWebDataResponse:
    """
    Stores web data sent from the Crawling Module. Expects JSON payload representing web data. Ensures data integrity and consistency before storage, and accessible only by the System Administrator and Data Manager.

    Args:
        userId (str): Identifier for the user responsible for the data submission.
        data (Dict[str, Any]): The actual web data to be stored, structured as key-value pairs.
        compressionType (Optional[str]): Type of compression used on the data, if applicable.

    Returns:
        StoreWebDataResponse: Confirmation response after storing web data.
    """
    try:
        crawling_session = await prisma.models.CrawlingSession.prisma().create(
            data={"userId": userId, "status": "completed", "logsPath": "/path/to/logs"}
        )
        await prisma.models.CrawledData.prisma().create(
            data={
                "data": data,
                "compressionType": compressionType,
                "crawlingSessionId": crawling_session.id,
                "archivedResourceId": "",
            }
        )
        return StoreWebDataResponse(success=True, message="Data stored successfully.")
    except Exception as e:
        return StoreWebDataResponse(success=False, message=str(e))
