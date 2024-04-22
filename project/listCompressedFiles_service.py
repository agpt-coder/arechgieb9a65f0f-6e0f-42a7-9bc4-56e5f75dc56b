from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class GetCompressedFilesRequest(BaseModel):
    """
    Request model for retrieving details of compressed files. No specific input parameters required as this is a straightforward GET request.
    """

    pass


class CompressedFile(BaseModel):
    """
    Details of a single compressed file.
    """

    file_id: str
    original_size: int
    compressed_size: int
    compression_ratio: float


class GetCompressedFilesResponse(BaseModel):
    """
    Response model for listing compressed files which include identifiers, original and compressed sizes, and compression ratios.
    """

    files: List[CompressedFile]


async def listCompressedFiles(
    request: GetCompressedFilesRequest,
) -> GetCompressedFilesResponse:
    """
    Lists all the files that have been compressed. It provides details such as file identifiers,
    original sizes, compressed sizes, and compression ratios. This is useful for monitoring and
    auditing purposes. The response includes a list of files along with the mentioned data.

    Args:
        request (GetCompressedFilesRequest): Request model for retrieving details of compressed files.
                                             No specific input parameters required as this is a straightforward GET request.

    Returns:
        GetCompressedFilesResponse: Response model for listing compressed files which include identifiers,
                                    original and compressed sizes, and compression ratios.
    """
    compressed_data_records = await prisma.models.ArchivedResource.prisma().find_many(
        where={"CrawledData": {"some": {"compressionType": {"not": None}}}},
        include={"CrawledData": {"include": {"crawledSession": True}}},
    )
    compressed_files = []
    for resource in compressed_data_records:
        for data in resource.CrawledData:
            if data.compressionType:
                try:
                    original_size = data.data["original_size"]
                    compressed_size = data.data["compressed_size"]
                    compression_ratio = (
                        original_size / compressed_size if compressed_size > 0 else 0
                    )  # TODO(autogpt): Operator "/" not supported for types "Serializable" and "Serializable"
                    #     Operator "/" not supported for types "None" and "None"
                    #     Operator "/" not supported for types "None" and "bool"
                    #     Operator "/" not supported for types "None" and "float"
                    #     Operator "/" not supported for types "None" and "int"
                    #     Operator "/" not supported for types "None" and "str"
                    #     Operator "/" not supported for types "None" and "datetime"
                    #     Operator "/" not supported for types "None" and "List[Any]"
                    #     Operator "/" not supported for types "None" and "Dict[None, Any]"
                    #     .... reportOperatorIssue
                    compressed_file = CompressedFile(
                        file_id=data.id,
                        original_size=original_size,
                        compressed_size=compressed_size,
                        compression_ratio=compression_ratio,
                    )
                    compressed_files.append(compressed_file)
                except KeyError:
                    continue
    return GetCompressedFilesResponse(files=compressed_files)
