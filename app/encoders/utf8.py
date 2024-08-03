class Utf8Encoder:
    def __call__(self, data: str) -> bytes:
        return data.encode()