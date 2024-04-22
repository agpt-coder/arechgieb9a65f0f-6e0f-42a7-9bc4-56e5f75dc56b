import gzip
import zlib
from typing import Optional

from pydantic import BaseModel


class CompressDataResponse(BaseModel):
    """
    This model provides a summary of the compression operation, including the efficiency and size of the compressed data.
    """

    message: str
    originalSize: int
    compressedSize: int
    compressionRatio: float


def compressData(
    data: str, compressionAlgorithm: Optional[str] = None
) -> CompressDataResponse:
    """
    Accepts raw data from the Crawling Module, compresses it using specified algorithms, and forwards the compressed data to the Data Storage Module. The response includes a confirmation of the data receipt and a summary of the compression results, such as the compression ratio achieved.

    Args:
        data (str): The raw data extracted during a web crawling session.
        compressionAlgorithm (Optional[str]): The type of compression algorithm to apply to the data. It defaults to 'gzip' if not specified.

    Returns:
        CompressDataResponse: This model provides a summary of the compression operation, including the efficiency and size of the compressed data.
    """
    original_size = len(data.encode("utf-8"))
    if compressionAlgorithm is None or compressionAlgorithm == "gzip":
        compressed_data = gzip.compress(data.encode("utf-8"))
        algorithm_used = "gzip"
    elif compressionAlgorithm == "deflate":
        compressed_data = zlib.compress(data.encode("utf-8"))
        algorithm_used = "deflate"
    else:
        raise ValueError(f"Unsupported compression algorithm {compressionAlgorithm}")
    compressed_size = len(compressed_data)
    compression_ratio = original_size / compressed_size if compressed_size > 0 else 0
    response = CompressDataResponse(
        message=f"Data compressed successfully using {algorithm_used}.",
        originalSize=original_size,
        compressedSize=compressed_size,
        compressionRatio=compression_ratio,
    )
    return response
