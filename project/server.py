import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

import prisma
import prisma.enums
import project.compressData_service
import project.createBackup_service
import project.createUser_service
import project.createWebData_service
import project.deleteBackup_service
import project.deleteUser_service
import project.deleteWebData_service
import project.fetchCrawledData_service
import project.fetchSearchMetadata_service
import project.getAllWebData_service
import project.getBackupDetails_service
import project.getCompressionSettings_service
import project.getCrawlingStatus_service
import project.getUserDetails_service
import project.getWebData_service
import project.listBackups_service
import project.listCompressedFiles_service
import project.listUsers_service
import project.logSearchQuery_service
import project.restoreData_service
import project.searchArchivedContent_service
import project.startCrawling_service
import project.stopCrawling_service
import project.updateCompressionSettings_service
import project.updateCrawlingConfig_service
import project.updateUser_service
import project.updateWebData_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(title="arechgie", lifespan=lifespan, description="archive the internet")


@app.put(
    "/compress/settings",
    response_model=project.updateCompressionSettings_service.CompressionSettingsUpdateResponse,
)
async def api_put_updateCompressionSettings(
    algorithm: str, level: int, optimize_for: str
) -> project.updateCompressionSettings_service.CompressionSettingsUpdateResponse | Response:
    """
    Updates the compression settings based on input parameters. This route is crucial for tailoring the compression process to specific needs, such as optimizing for speed or compression ratio. The expectations are to provide the new settings in the request, and the response confirms the successful update.
    """
    try:
        res = await project.updateCompressionSettings_service.updateCompressionSettings(
            algorithm, level, optimize_for
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/search/logs", response_model=project.logSearchQuery_service.SearchLogResponse
)
async def api_post_logSearchQuery(
    search_query: str, filters: Dict[str, str], user_id: str, timestamp: datetime
) -> project.logSearchQuery_service.SearchLogResponse | Response:
    """
    Logs each user's search query for analysis and improvement of the search engine. It captures detailed information about the search query, including the search terms, filters applied, and timestamp of the search. This data is essential for understanding user behavior and enhancing search functionality.
    """
    try:
        res = await project.logSearchQuery_service.logSearchQuery(
            search_query, filters, user_id, timestamp
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/users/{userId}", response_model=project.deleteUser_service.DeleteUserResponse
)
async def api_delete_deleteUser(
    userId: str,
) -> project.deleteUser_service.DeleteUserResponse | Response:
    """
    Removes a user from the system using the specified userId. A successful operation will confirm the user's removal. The API Access Module handles this to maintain data integrity and log the action for security compliance.
    """
    try:
        res = await project.deleteUser_service.deleteUser(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/users/{userId}", response_model=project.updateUser_service.UpdateUserResponse
)
async def api_put_updateUser(
    userId: str, email: str, password: str, role: prisma.enums.Role
) -> project.updateUser_service.UpdateUserResponse | Response:
    """
    Updates details for a specific user. It securely updates user data in the Data Storage Module based on the provided userId and input data. Returns the updated user information upon successful update.
    """
    try:
        res = await project.updateUser_service.updateUser(userId, email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/backups", response_model=project.listBackups_service.BackupListingResponse)
async def api_get_listBackups(
    request: project.listBackups_service.GetBackupsRequest,
) -> project.listBackups_service.BackupListingResponse | Response:
    """
    Retrieves a list of all backup records. Each record provides the backup ID, date, and status. This allows system administrators and backup operators to monitor the backup states.
    """
    try:
        res = await project.listBackups_service.listBackups(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/users", response_model=project.listUsers_service.GetUsersResponse)
async def api_get_listUsers(
    page: Optional[int], limit: Optional[int], sort: Optional[str]
) -> project.listUsers_service.GetUsersResponse | Response:
    """
    Retrieves a list of all users. User data is fetched from the Data Storage Module, and this route is commonly used to manage users or retrieve a complete user listing. Response includes an array of user data.
    """
    try:
        res = await project.listUsers_service.listUsers(page, limit, sort)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/search", response_model=project.searchArchivedContent_service.SearchResponseModel
)
async def api_get_searchArchivedContent(
    keywords: Optional[str],
    start_date: Optional[str],
    end_date: Optional[str],
    content_type: Optional[str],
    page: Optional[int],
    page_size: Optional[int],
) -> project.searchArchivedContent_service.SearchResponseModel | Response:
    """
    Allows users to search the archived content using various criteria such as keywords, date ranges, and content types. This route fetches data using the Data Storage Module. The response includes a paginated list of search results tailored to the query parameters provided by the user.
    """
    try:
        res = await project.searchArchivedContent_service.searchArchivedContent(
            keywords, start_date, end_date, content_type, page, page_size
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/compress", response_model=project.compressData_service.CompressDataResponse)
async def api_post_compressData(
    data: str, compressionAlgorithm: Optional[str]
) -> project.compressData_service.CompressDataResponse | Response:
    """
    Accepts raw data from the Crawling Module, compresses it using specified algorithms, and forwards the compressed data to the Data Storage Module. The response includes a confirmation of the data receipt and a summary of the compression results, such as the compression ratio achieved.
    """
    try:
        res = project.compressData_service.compressData(data, compressionAlgorithm)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/web-data/{dataId}",
    response_model=project.getWebData_service.GetWebDataByIdResponse,
)
async def api_get_getWebData(
    dataId: str,
) -> project.getWebData_service.GetWebDataByIdResponse | Response:
    """
    Retrieves specific web data by its ID. Used to fetch data for the Search Engine Module or for administrative purposes. Returns JSON object of the web data if found or a not found error if no such data exists.
    """
    try:
        res = await project.getWebData_service.getWebData(dataId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/backups/{backupId}",
    response_model=project.deleteBackup_service.DeleteBackupResponse,
)
async def api_delete_deleteBackup(
    backupId: str,
) -> project.deleteBackup_service.DeleteBackupResponse | Response:
    """
    Deletes a specific backup by its backup ID, removing it from the storage. Used to manage storage and delete old or unnecessary backups, ensuring efficient use of resources.
    """
    try:
        res = await project.deleteBackup_service.deleteBackup(backupId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/web-data/{dataId}",
    response_model=project.deleteWebData_service.DeleteWebDataResponse,
)
async def api_delete_deleteWebData(
    dataId: str, role: prisma.enums.Role
) -> project.deleteWebData_service.DeleteWebDataResponse | Response:
    """
    Deletes specific web data by its ID. Necessary for maintaining data relevance and storage management. A success response is returned if the operation is successful.
    """
    try:
        res = await project.deleteWebData_service.deleteWebData(dataId, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/backups/{backupId}",
    response_model=project.getBackupDetails_service.BackupDetailsResponse,
)
async def api_get_getBackupDetails(
    backupId: str,
) -> project.getBackupDetails_service.BackupDetailsResponse | Response:
    """
    Fetches the details of a specific backup using the backup ID, including the data size, backup date, and any errors encountered. Essential for detailed diagnostics and backup verification.
    """
    try:
        res = await project.getBackupDetails_service.getBackupDetails(backupId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/backups", response_model=project.createBackup_service.CreateBackupResponse)
async def api_post_createBackup(
    data_identifier: str, compression_type: Optional[str]
) -> project.createBackup_service.CreateBackupResponse | Response:
    """
    Creates a backup of the data. This route triggers the backup process in the Data Storage Module, storing the backup data possibly in a separate storage solution. The API should return a success status and a backup ID.
    """
    try:
        res = await project.createBackup_service.createBackup(
            data_identifier, compression_type
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/compress/settings",
    response_model=project.getCompressionSettings_service.CompressionSettingsResponse,
)
async def api_get_getCompressionSettings(
    request: project.getCompressionSettings_service.GetCompressionSettingsRequest,
) -> project.getCompressionSettings_service.CompressionSettingsResponse | Response:
    """
    Retrieves the current compression settings and algorithms in use. This information helps in understanding the compression process and adjusting parameters if necessary. The response includes details such as algorithm names, compression levels, and expected efficiencies.
    """
    try:
        res = await project.getCompressionSettings_service.getCompressionSettings(
            request
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/recoveries", response_model=project.restoreData_service.RecoveryResponse)
async def api_post_restoreData(
    backupId: str,
) -> project.restoreData_service.RecoveryResponse | Response:
    """
    Initiates a data recovery operation using a specified backup ID. The data restore updates the current state of the Data Storage Module to match that of the backup. This route returns a success status and details of the restore process.
    """
    try:
        res = await project.restoreData_service.restoreData(backupId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/web-data/{dataId}",
    response_model=project.updateWebData_service.UpdateWebDataResponse,
)
async def api_put_updateWebData(
    dataId: str, new_content: Dict[str, Any], compressionType: Optional[str]
) -> project.updateWebData_service.UpdateWebDataResponse | Response:
    """
    Updates existing web data by its ID with new content received from the Crawling Module. Validates changes and confirms update success. Returns the updated data object.
    """
    try:
        res = await project.updateWebData_service.updateWebData(
            dataId, new_content, compressionType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/crawling/stop", response_model=project.stopCrawling_service.CrawlingStopResponse
)
async def api_post_stopCrawling(
    crawlingSessionId: Optional[str],
) -> project.stopCrawling_service.CrawlingStopResponse | Response:
    """
    Stops the currently running crawling process. Should confirm whether the stop was successful and the state of the last crawl.
    """
    try:
        res = await project.stopCrawling_service.stopCrawling(crawlingSessionId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/web-data", response_model=project.createWebData_service.StoreWebDataResponse
)
async def api_post_createWebData(
    userId: str, data: Dict[str, Any], compressionType: Optional[str]
) -> project.createWebData_service.StoreWebDataResponse | Response:
    """
    Stores web data sent from the Crawling Module. Expects JSON payload representing web data. Ensures data integrity and consistency before storage. Accessible only by the System Administrator and Data Manager.
    """
    try:
        res = await project.createWebData_service.createWebData(
            userId, data, compressionType
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/users/{userId}", response_model=project.getUserDetails_service.UserDetailsResponse
)
async def api_get_getUserDetails(
    userId: str,
) -> project.getUserDetails_service.UserDetailsResponse | Response:
    """
    Fetches detailed information of a user identified by userId. This includes user contact information, roles, and activity logs. Makes use of the API Access Module to retrieve user data securely. The result is a detailed user profile.
    """
    try:
        res = await project.getUserDetails_service.getUserDetails(userId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post("/users", response_model=project.createUser_service.CreateUserResponse)
async def api_post_createUser(
    username: str, email: str, role: prisma.enums.Role
) -> project.createUser_service.CreateUserResponse | Response:
    """
    This endpoint creates a new user within the system. It expects details like username, email, and roles in the body of the request. Upon successful creation, it returns the user ID along with a success message. This interaction uses the API Access Module for user data validation and storage.
    """
    try:
        res = await project.createUser_service.createUser(username, email, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/crawling/data",
    response_model=project.fetchCrawledData_service.FetchCrawledDataResponse,
)
async def api_get_fetchCrawledData(
    request: project.fetchCrawledData_service.FetchCrawledDataRequest,
) -> project.fetchCrawledData_service.FetchCrawledDataResponse | Response:
    """
    Retrieves crawled data stored by the module. It interacts with the Data Storage Module for fetching the data. Response should include the fetched data.
    """
    try:
        res = await project.fetchCrawledData_service.fetchCrawledData(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.patch(
    "/crawling/config",
    response_model=project.updateCrawlingConfig_service.CrawlingConfigUpdateResponse,
)
async def api_patch_updateCrawlingConfig(
    crawl_depth: Optional[int],
    pause_duration: Optional[float],
    target_domains: Optional[List[str]],
) -> project.updateCrawlingConfig_service.CrawlingConfigUpdateResponse | Response:
    """
    Updates configurations used for the crawling process, such as crawl depth, pause duration, and target domains. Response confirms the application of new settings.
    """
    try:
        res = await project.updateCrawlingConfig_service.updateCrawlingConfig(
            crawl_depth, pause_duration, target_domains
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/crawling/start",
    response_model=project.startCrawling_service.CrawlingInitiationResponse,
)
async def api_post_startCrawling(
    urls: List[str], userId: str, depth: Optional[int], delay: Optional[int]
) -> project.startCrawling_service.CrawlingInitiationResponse | Response:
    """
    Initiates the crawling process. It schedules tasks, fetches URLs, and begins extraction and parsing. This uses the Data Compression Module for preprocessing data. Successful response should indicate crawling initiation status.
    """
    try:
        res = await project.startCrawling_service.startCrawling(
            urls, userId, depth, delay
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/compress/files",
    response_model=project.listCompressedFiles_service.GetCompressedFilesResponse,
)
async def api_get_listCompressedFiles(
    request: project.listCompressedFiles_service.GetCompressedFilesRequest,
) -> project.listCompressedFiles_service.GetCompressedFilesResponse | Response:
    """
    Lists all the files that have been compressed. It provides details such as file identifiers, original sizes, compressed sizes, and compression ratios. This is useful for monitoring and auditing purposes. The response includes a list of files along with the mentioned data.
    """
    try:
        res = await project.listCompressedFiles_service.listCompressedFiles(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get("/web-data", response_model=project.getAllWebData_service.GetWebDataOutput)
async def api_get_getAllWebData(
    page: int, pageSize: int
) -> project.getAllWebData_service.GetWebDataOutput | Response:
    """
    Retrieves all stored web data in a paginated response. Primarily used for oversight and backup purposes. Returns a list of web data entries.
    """
    try:
        res = await project.getAllWebData_service.getAllWebData(page, pageSize)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/crawling/status",
    response_model=project.getCrawlingStatus_service.GetCrawlingStatusResponse,
)
async def api_get_getCrawlingStatus(
    request: project.getCrawlingStatus_service.GetCrawlingStatusRequest,
) -> project.getCrawlingStatus_service.GetCrawlingStatusResponse | Response:
    """
    Provides current status of the crawling process, including the number of pages processed, current URLs being crawled, and any errors. Expected response includes status details.
    """
    try:
        res = await project.getCrawlingStatus_service.getCrawlingStatus(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/search/metadata",
    response_model=project.fetchSearchMetadata_service.GetSearchMetadataResponse,
)
async def api_get_fetchSearchMetadata(
    request: project.fetchSearchMetadata_service.GetSearchMetadataRequest,
) -> project.fetchSearchMetadata_service.GetSearchMetadataResponse | Response:
    """
    Provides metadata necessary for front-end components to render search interfaces effectively, such as available filters and search criteria options. This endpoint directly interacts with the Data Storage Module to ensure up-to-date metadata is always provided. It helps in providing dynamic search options based on the data available.
    """
    try:
        res = await project.fetchSearchMetadata_service.fetchSearchMetadata(request)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
