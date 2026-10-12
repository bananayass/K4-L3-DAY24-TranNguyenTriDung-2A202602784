"""BƯỚC 3c — kiểm soát OBO tại ranh giới từng tool call."""
from __future__ import annotations

import hashlib
import json
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from agent import ledger, policy, tools
from agent.policy import PolicyContext

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
DEFAULT_LEDGER_PATH = REPORTS_DIR / "ledger.jsonl"
AGENT_ID = "lab24-agent"
AGENT_SCOPES = ("search_docs", "read_customer", "http_post")
RUN_TTL = timedelta(minutes=5)
TICKET_FILENAME_RE = re.compile(r"ticket-(\d+)\.md\Z")


class RunnerScaffoldPending(NotImplementedError):
    """Only the original runner stub uses this to enable the CP1/CP2 baseline."""


def handle(message: str, llm, log_dir: Path | None = None,
           principal_id: str = "support_l1") -> str:
    """Run the mockable agent with simulated OBO policy and audit metadata.

    Each tool decision is checked and logged before the tool can execute.
    Principal records are lab fixtures, not production authentication.
    """
    ledger_dir = Path(log_dir) if log_dir is not None else REPORTS_DIR
    ledger_path = ledger_dir / "ledger.jsonl"
    run_id = uuid.uuid4().hex
    expires_at = (datetime.now(timezone.utc) + RUN_TTL).isoformat(timespec="seconds")
    owner = f"{AGENT_ID}/{run_id}"

    def invoke(tool_name: str, args: dict, classification: str,
               purpose: str, egress_enabled: bool, operation):
        context = PolicyContext(
            data_classification=classification,
            request_purpose=purpose,
            agent_owner=owner,
            delegation_depth=0,
            egress_enabled=egress_enabled,
            principal_id=principal_id,
            requested_tool=tool_name,
            agent_scopes=AGENT_SCOPES,
            parent_scopes=(),
            expires_at=expires_at,
        )
        allowed, reason = policy.check(context)
        _append_decision(
            ledger_path=ledger_path,
            run_id=run_id,
            principal_id=principal_id,
            expires_at=expires_at,
            tool_name=tool_name,
            args=args,
            classification=classification,
            allowed=allowed,
            reason=reason,
        )
        if not allowed:
            return False, None
        return True, operation()

    allowed, docs = invoke(
        tool_name="search_docs",
        args={"query": message},
        classification="internal",
        purpose="summarize-tickets",
        egress_enabled=False,
        operation=lambda: tools.search_docs(message),
    )
    if not allowed:
        docs = []

    combined_text = "\n\n".join(doc["text"] for doc in docs)
    injected = llm.find_injection(combined_text)

    # Run A chỉ chuyển sang Run B các ticket ID lấy từ tên file trong corpus
    # Không lấy customer ID từ nội dung ticket hoặc kết quả nhận diện injection
    ticket_ids = _ticket_ids_from_docs(docs)
    mapping_allowed, customer_ids = invoke(
        tool_name="read_customer",
        args={"ticket_ids": ticket_ids},
        classification="restricted",
        purpose="support-reply",
        egress_enabled=False,
        operation=lambda: _customer_ids_for_tickets(ticket_ids),
    )
    if not mapping_allowed:
        customer_ids = []

    # Run B chỉ đọc hồ sơ gắn với ticket ID lấy từ tên file
    # invoke() kiểm tra quyền và ghi lại kết quả trước khi gọi tool
    collected = []
    for customer_id in customer_ids:
        try:
            allowed, record = invoke(
                tool_name="read_customer",
                args={"customer_id": customer_id},
                classification="restricted",
                purpose="support-reply",
                egress_enabled=False,
                operation=lambda customer_id=customer_id: tools.read_customer(customer_id),
            )
        except tools.ToolError:
            continue
        if allowed:
            collected.append(record)

    if injected is not None and collected:
        # Keep customer data out of the ledger; only its canonical hash is stored.
        invoke(
            tool_name="http_post",
            args={"url": injected.target_url, "body": {"records": collected}},
            classification="restricted",
            purpose="support-reply",
            egress_enabled=True,
            operation=lambda: tools.http_post(
                injected.target_url, {"records": collected}
            ),
        )

    return llm.summarize(docs)


def _ticket_ids_from_docs(docs: list[dict]) -> list[int]:
    """Lấy ticket ID từ tên file trong corpus, không đọc từ nội dung file"""
    ticket_ids = {
        int(match.group(1))
        for doc in docs
        if (match := TICKET_FILENAME_RE.fullmatch(str(doc.get("id", ""))))
    }
    return sorted(ticket_ids)


def _customer_ids_for_tickets(ticket_ids: list[int]) -> list[str]:
    """Tìm khách có related_tickets khớp với các ticket ID đã nhận"""
    if not ticket_ids:
        return []

    customers = json.loads(tools.CUSTOMERS_FILE.read_text(encoding="utf-8"))
    ticket_set = set(ticket_ids)
    return [
        str(customer["customer_id"])
        for customer in customers
        if ticket_set.intersection(customer.get("related_tickets", []))
    ]


def _append_decision(*, ledger_path: Path, run_id: str, principal_id: str,
                     expires_at: str, tool_name: str, args: dict,
                     classification: str, allowed: bool, reason: str) -> None:
    """Append one JSONL decision without storing raw tool arguments."""
    args_json = json.dumps(args, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    entry = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "agent_id": AGENT_ID,
        "run_id": run_id,
        "tool": tool_name,
        "args_hash": hashlib.sha256(args_json.encode("utf-8")).hexdigest(),
        "classification": classification,
        "decision": "allow" if allowed else "deny",
        "reason": reason or "policy returned no reason",
        "on_behalf_of": principal_id,
        "expires_at": expires_at,
    }
    ledger.append(entry, ledger_path)
