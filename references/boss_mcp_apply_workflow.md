# BOSS MCP Apply Workflow

This workflow adds a gated BOSS Zhipin job-application orchestrator to the Codex job-resume skill.

## Positioning

The repository already focuses on JD routing, resume tailoring, outreach text, interview prep, risky-claim audits, and job-table screening. The BOSS MCP layer should extend that workflow as a controlled execution bridge:

```text
BOSS MCP / local job table
        │
        ▼
search / detail tools
        │
        ▼
job detail cards
        │
        ▼
resume route + claim safety gate
        │
        ▼
apply gate
  ├─ dry-run: detail display only
  ├─ manual: approve each job before apply
  └─ auto: explicit opt-in + capped + logged
        │
        ▼
audit log + local state
```

## Safety model

Default mode is `manual`. `auto` requires all of the following:

1. `safety.allow_auto_apply` is set to `true` in a local config file.
2. CLI mode is set to `--mode auto`.
3. CLI flag `--i-understand-batch-apply` is present.
4. The batch is capped by `limits.max_apply_count`.
5. Each job detail is fetched and printed before the write action.
6. Every attempt is written to the audit log when enabled.
7. Previously attempted jobs are skipped when local dedupe is enabled.

The implementation must not contain code for CAPTCHA bypass, login bypass, rate-limit bypass, hidden scraping, cookie theft, or background mass outreach. It only calls a user-configured MCP server using the user's own authenticated session.

## MCP tool contract

The script is configurable because public BOSS MCP projects use different tool names and payload shapes.

Required logical tools:

| Logical tool | Config key | Purpose |
|---|---|---|
| Search jobs | `tool_names.search` | Return candidate job list. |
| Read detail | `tool_names.detail` | Return one full JD/detail object. |
| Apply | `tool_names.apply` | Submit application or greeting through the configured MCP server. |

Recommended normalized job fields:

```json
{
  "job_id": "...",
  "security_id": "...",
  "title": "算法实习生",
  "company": "...",
  "salary": "...",
  "city": "杭州",
  "experience": "不限",
  "education": "本科",
  "recruiter": "...",
  "url": "...",
  "description": "..."
}
```

If the MCP server does not expose an apply/write tool, keep the workflow in `dry-run` or `manual-open` style: print the job details, export the shortlist, and let the user finish on the official BOSS page.

## Recommended local run flow

1. Copy `boss_apply_config.example.json` to a local ignored config file.
2. Set the MCP server command and real tool names.
3. Run dry-run first and confirm field extraction.
4. Run manual mode to approve each job.
5. Use auto mode only after the dry-run and manual mode reports are correct.

## Output expectations

Every job must be rendered before any apply call:

- title
- company
- salary
- city/location
- experience and education
- recruiter if present
- URL if present
- JD/description excerpt
- local route hint if later integrated with the resume router

Every write attempt must record:

- timestamp
- mode
- job key
- title and company
- tool name
- result status
- error text if any
