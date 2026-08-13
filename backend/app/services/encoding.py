from charset_normalizer import from_bytes
from pydantic import BaseModel


class EncodingDetection(BaseModel):
    encoding: str
    confidence: float
    has_replacement_characters: bool


def detect_encoding(raw: bytes) -> EncodingDetection:
    result = from_bytes(raw).best()
    encoding = (result.encoding if result else None) or "utf-8"
    decoded = raw.decode(encoding, errors="replace")
    return EncodingDetection(
        encoding=encoding,
        confidence=float(result.percent_coherence / 100 if result else 0),
        has_replacement_characters="\ufffd" in decoded,
    )
