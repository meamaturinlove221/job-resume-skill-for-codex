#!/usr/bin/env python3
"""
Gated BOSS MCP batch-apply orchestrator.

This script intentionally avoids browser automation, scraping, login bypass,
CAPTCHA bypass, and hidden platform writes. It only calls a user-configured MCP
server over stdio, displays each job detail, and then applies according to the
selected approval mode.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

JsonDict = Dict[str, Any]


class MCPError(RuntimeError):
    pass


class MCPStdioClient:
    """Minimal JSON-RPC 2.0 client for MCP stdio transport."""

    def __init__(self, command: str, args: List[str], env: Optional[JsonDict] = None) -> None:
        merged_env = os.environ.copy()
        if env:
            merged_env.update({str(k): str(v) for k, v in env.items()})
        self.proc = subprocess.Popen(
            [command, *args],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=merged_env,
            text=False,
        )
        self._next_id = 1

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def __enter__(self) -> "MCPStdioClient":
        self.initialize()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        self.close()

    def _send(self, payload: JsonDict) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(data)}\r\n\r\n".encode("ascii")
        if self.proc.stdin is None:
            raise MCPError("MCP stdin is closed")
        self.proc.stdin.write(header + data)
        self.proc.stdin.flush()

    def _read_message(self) -> JsonDict:
        if self.proc.stdout is None:
            raise MCPError("MCP stdout is closed")
        headers: Dict[str, str] = {}
        while True:
            line = self.proc.stdout.readline()
            if not line:
                stderr = self._read_stderr_tail()
                raise MCPError(f"MCP server closed stdout. stderr={stderr}")
            if line in (b"\r\n", b"\n"):
                break
            key, _, value = line.decode("ascii", errors="replace").partition(":")
            headers[key.strip().lower()] = value.strip()
        length = int(headers.get("content-length", "0"))
        if length <= 0:
            raise MCPError(f"Invalid MCP message headers: {headers}")
        body = self.proc.stdout.read(length)
        return json.loads(body.decode("utf-8"))

    def _read_stderr_tail(self) -> str:
        if self.proc.stderr is None:
            return ""
        try:
            return self.proc.stderr.read(4096).decode("utf-8", errors="replace")
        except Exception:
            return ""

    def request(self, method: str, params: Optional[JsonDict] = None) -> Any:
        req_id = self._next_id
        self._next_id += 1
        self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params or {}})
        while True:
            msg = self._read_message()
            if msg.get("id") != req_id:
                continue
            if "error" in msg:
                raise MCPError(json.dumps(msg["error"], ensure_ascii=False))
            return msg.get("result")

    def notify(self, method: str, params: Optional[JsonDict] = None) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def initialize(self) -> None:
        self.request(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "job-resume-codex-boss-apply", "version": "0.1.0"},
            },
        )
        self.notify("notifications/initialized")

    def call_tool(self, name: str, arguments: JsonDict) -> Any:
        result = self.request("tools/call", {"name": name, "arguments": arguments})
        return unwrap_mcp_tool_result(result)


def unwrap_mcp_tool_result(result: Any) -> Any:
    """Handle common MCP content envelopes while preserving unknown shapes."""
    if not isinstance(result, dict):
        return result
    if "structuredContent" in result:
        return result["structuredContent"]
    content = result.get("content")
    if isinstance(content, list) and content:
        text_parts = [item.get("text") for item in content if isinstance(item, dict) and "text" in item]
        if text_parts:
            text = "\n".join(str(x) for x in text_parts)
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return {"text": text}
    return result


def load_json(path: Path) -> JsonDict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def append_jsonl(path: Path, row: JsonDict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def as_list(payload: Any) -> List[JsonDict]:
    if isinstance(payload, list):
        return [x for x in payload if isinstance(x, dict)]
    if isinstance(payload, dict):
        for key in ("jobs", "data", "items", "results", "list"):
            if isinstance(payload.get(key), list):
                return [x for x in payload[key] if isinstance(x, dict)]
    return []


def pick(job: JsonDict, field_map: JsonDict, logical_name: str, default: str = "") -> str:
    key = field_map.get(logical_name, logical_name)
    value = job.get(key, job.get(logical_name, default))
    if value is None:
        return default
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def job_key(job: JsonDict, field_map: JsonDict) -> str:
    security_id = pick(job, field_map, "security_id")
    job_id = pick(job, field_map, "job_id")
    if security_id or job_id:
        return f"sid={security_id}|jid={job_id}"
    return f"title={pick(job, field_map, 'title')}|company={pick(job, field_map, 'company')}"


def trim(text: str, n: int = 500) -> str:
    text = " ".join(text.split())
    return text if len(text) <= n else text[: n - 1] + "…"


def render_job_card(index: int, job: JsonDict, field_map: JsonDict) -> None:
    title = pick(job, field_map, "title", "<no title>")
    company = pick(job, field_map, "company", "<no company>")
    print("=" * 88)
    print(f"[{index}] {title}  |  {company}")
    rows = [
        ("薪资", pick(job, field_map, "salary")),
        ("城市", pick(job, field_map, "city")),
        ("经验", pick(job, field_map, "experience")),
        ("学历", pick(job, field_map, "education")),
        ("招聘者", pick(job, field_map, "recruiter")),
        ("链接", pick(job, field_map, "url")),
        ("JobKey", job_key(job, field_map)),
    ]
    for label, value in rows:
        if value:
            print(f"{label}: {value}")
    desc = pick(job, field_map, "description")
    if desc:
        print("JD摘要:")
        print(trim(desc, 900))


def build_search_args(args: argparse.Namespace, config: JsonDict) -> JsonDict:
    defaults = config.get("search_defaults", {})
    payload: JsonDict = {
        "query": args.query or defaults.get("query"),
        "city": args.city or defaults.get("city"),
        "limit": args.limit or defaults.get("limit"),
    }
    return {k: v for k, v in payload.items() if v not in (None, "")}


def build_detail_args(job: JsonDict, field_map: JsonDict) -> JsonDict:
    payload = {
        "security_id": pick(job, field_map, "security_id"),
        "job_id": pick(job, field_map, "job_id"),
    }
    return {k: v for k, v in payload.items() if v}


def build_apply_args(job: JsonDict, field_map: JsonDict, config: JsonDict) -> JsonDict:
    payload = build_detail_args(job, field_map)
    extra = config.get("apply_payload", {})
    for key, value in extra.items():
        if value not in (None, ""):
            payload[key] = value
    return payload


def ask_approval() -> bool:
    answer = input("Apply this job? Type y to apply, s to skip: ").strip().lower()
    return answer == "y"


def ensure_auto_allowed(args: argparse.Namespace, config: JsonDict) -> None:
    if args.mode != "auto":
        return
    safety = config.get("safety", {})
    if not safety.get("allow_auto_apply", False):
        raise SystemExit("auto mode is disabled in config: set safety.allow_auto_apply=true in a local config file")
    if not args.i_understand_batch_apply:
        raise SystemExit("auto mode requires --i-understand-batch-apply")


def load_state(path: Path) -> JsonDict:
    if path.exists():
        return load_json(path)
    return {"applied_keys": []}


def main() -> int:
    parser = argparse.ArgumentParser(description="Gated BOSS MCP batch apply orchestrator")
    parser.add_argument("--config", required=True, help="Path to local config JSON")
    parser.add_argument("--jobs", help="Optional JSON file with jobs; skips MCP search when present")
    parser.add_argument("--query", help="Search keyword, for MCP search tool")
    parser.add_argument("--city", help="City, for MCP search tool")
    parser.add_argument("--limit", type=int, help="Max search results")
    parser.add_argument("--mode", choices=["dry-run", "manual", "auto"], default="manual")
    parser.add_argument("--i-understand-batch-apply", action="store_true")
    parser.add_argument("--no-detail", action="store_true", help="Skip detail tool call; only use search payload")
    parser.add_argument("--show-raw", action="store_true", help="Print raw job JSON after each card")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_json(config_path)
    ensure_auto_allowed(args, config)

    field_map = config.get("field_map", {})
    tool_names = config.get("tool_names", {})
    limits = config.get("limits", {})
    paths = config.get("paths", {})
    safety = config.get("safety", {})

    max_apply = int(limits.get("max_apply_count", 10))
    min_interval = float(limits.get("min_interval_seconds", 30))
    state_path = Path(paths.get("state_file", ".boss_apply_state.json"))
    audit_path = Path(paths.get("audit_log", ".boss_apply_audit.jsonl"))
    state = load_state(state_path)
    applied_keys = set(state.get("applied_keys", []))

    mcp_cfg = config.get("mcp_server", {})
    jobs: List[JsonDict]

    with MCPStdioClient(mcp_cfg["command"], list(mcp_cfg.get("args", [])), mcp_cfg.get("env", {})) as client:
        if args.jobs:
            jobs = as_list(load_json(Path(args.jobs)))
        else:
            search_tool = tool_names.get("search")
            if not search_tool:
                raise SystemExit("tool_names.search is required when --jobs is not provided")
            jobs = as_list(client.call_tool(search_tool, build_search_args(args, config)))

        if not jobs:
            print("No jobs found.")
            return 0

        applied_count = 0
        for idx, job in enumerate(jobs, start=1):
            if applied_count >= max_apply:
                print(f"Reached max_apply_count={max_apply}; stop.")
                break

            detail = job
            if not args.no_detail and safety.get("require_detail_before_apply", True):
                detail_tool = tool_names.get("detail")
                if detail_tool:
                    detail_payload = client.call_tool(detail_tool, build_detail_args(job, field_map))
                    if isinstance(detail_payload, dict):
                        detail = {**job, **detail_payload}

            key = job_key(detail, field_map)
            if safety.get("dedupe_by_job_key", True) and key in applied_keys:
                print(f"Skip duplicate job: {key}")
                continue

            render_job_card(idx, detail, field_map)
            if args.show_raw:
                print(json.dumps(detail, ensure_ascii=False, indent=2))

            should_apply = False
            if args.mode == "dry-run":
                print("DRY-RUN: no apply call will be made.")
            elif args.mode == "manual":
                should_apply = ask_approval()
            elif args.mode == "auto":
                should_apply = True
                print("AUTO mode: detail displayed; applying because explicit auto gates are enabled.")

            if not should_apply:
                append_jsonl(
                    audit_path,
                    {
                        "time": datetime.now(timezone.utc).isoformat(),
                        "mode": args.mode,
                        "action": "skip",
                        "job_key": key,
                        "title": pick(detail, field_map, "title"),
                        "company": pick(detail, field_map, "company"),
                    },
                )
                continue

            apply_tool = tool_names.get("apply")
            if not apply_tool:
                raise SystemExit("tool_names.apply is required for manual/auto apply mode")

            try:
                result = client.call_tool(apply_tool, build_apply_args(detail, field_map, config))
                ok = True
                error = ""
            except Exception as exc:  # keep audit on failed write attempts
                result = None
                ok = False
                error = str(exc)

            append_jsonl(
                audit_path,
                {
                    "time": datetime.now(timezone.utc).isoformat(),
                    "mode": args.mode,
                    "action": "apply",
                    "job_key": key,
                    "title": pick(detail, field_map, "title"),
                    "company": pick(detail, field_map, "company"),
                    "tool": apply_tool,
                    "ok": ok,
                    "error": error,
                    "result": result,
                },
            )
            if ok:
                print("Apply result: ok")
                applied_keys.add(key)
                applied_count += 1
                state["applied_keys"] = sorted(applied_keys)
                save_json(state_path, state)
            else:
                print(f"Apply result: failed: {error}")

            if applied_count < max_apply and min_interval > 0:
                time.sleep(min_interval)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
