
import gzip


class GzipEncoder:
    def __call__(self, data: str) -> bytes:
        return gzip.compress(data.encode())