"""BƯỚC 3a — PII gate TRƯỚC KHI vào context/store (12').

Đọc CHECKPOINTS.md (§3a) trước khi bắt đầu: Presidio không có tiếng Việt
sẵn (AnalyzerEngine() mặc định chỉ hỗ trợ "en"). Đường an toàn cho 2h là
regex recognizer + deny-list cho PERSON — coi spaCy/transformers NER là
stretch goal, KHÔNG bắt buộc.

Interface bắt buộc (tests/test_pii.py gọi trực tiếp 2 hàm này):

    detect(text: str) -> list[dict]
        Mỗi entity: {"type": str, "start": int, "end": int}
        `type` là một trong: "VN_CCCD", "VN_PHONE", "VN_BANK_ACCOUNT", "EMAIL"
        `start`/`end` là offset ký tự trong `text` (offset đầu bao gồm,
        offset cuối KHÔNG bao gồm — giống slice Python text[start:end]).
        Format này khớp với tests/vn_pii_testset.jsonl.

    redact(text: str) -> str
        Trả về `text` sau khi mọi entity từ detect() bị thay bằng
        "[REDACTED_<TYPE>]". Phải xử lý overlap/thứ tự đúng khi có nhiều
        entity (gợi ý: thay từ cuối văn bản về đầu để offset không bị lệch).

Gợi ý định dạng (không bắt buộc đúng regex này, miễn đạt ngưỡng trên test
set ở tests/vn_pii_testset.jsonl):
    VN_CCCD          12 chữ số liên tiếp
    VN_PHONE         0 + 9-10 chữ số, có thể có dấu cách/gạch ngang
    VN_BANK_ACCOUNT  8-16 chữ số liên tiếp, thường đi kèm "STK"/"số tài khoản"
    EMAIL            dạng chuẩn local@domain.tld

Đo bằng: pytest tests/test_pii.py -v -s   (in ra precision/recall)
"""
from __future__ import annotations

import re


EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
CCCD_RE = re.compile(r"(?<!\d)\d{12}(?!\d)")
PHONE_RE = re.compile(r"(?<!\d)0(?:[ -]?\d){9,10}(?!\d)")
BANK_RE = re.compile(
    r"(?:\bSTK\b|\bsố\s+tài\s+khoản\b)\s*:?\s*(\d{8,16})(?!\d)",
    re.IGNORECASE,
)


def detect(text: str) -> list[dict]:
    entities: list[dict] = []
    bank_spans: list[tuple[int, int]] = []

    # Nhận diện STK tránh phân loại nhầm STK 12 thành CCCD
    for match in BANK_RE.finditer(text):
        start, end = match.span(1)
        bank_spans.append((start, end))
        entities.append({"type": "VN_BANK_ACCOUNT", "start": start, "end": end})

    for pattern, entity_type in (
        (CCCD_RE, "VN_CCCD"),
        (PHONE_RE, "VN_PHONE"),
        (EMAIL_RE, "EMAIL"),
    ):
        for match in pattern.finditer(text):
            start, end = match.span()
            overlaps_bank = any(
                start < bank_end and bank_start < end
                for bank_start, bank_end in bank_spans
            )
            if entity_type != "EMAIL" and overlaps_bank:
                continue

            entities.append({"type": entity_type, "start": start, "end": end})

    return sorted(entities, key=lambda item: (item["start"], item["end"]))


def redact(text: str) -> str:
    entities = detect(text)

    for entity in sorted(entities, key=lambda item: item["start"], reverse=True):
        start = entity["start"]
        end = entity["end"]
        replacement = f"[REDACTED_{entity['type']}]"
        text = text[:start] + replacement + text[end:]

    return text
