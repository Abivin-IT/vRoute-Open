# Naming Conventions

> Source: vKernel PRD Section 4.3

## 4.3.1 Naming Patterns

| # | Element | Pattern | Example | Notes |
| --- | --- | --- | --- | --- |
| 1 | App ID | `com.[company].[appname]` | `com.vcorp.vhr` | Reverse-domain style, lowercase |
| 2 | Permission Code | `[domain].[resource].[action]` | `sales.lead.delete` | Dot-separated, lowercase |
| 3 | Event Type | `[DOMAIN]_[ENTITY]_[ACTION]` | `HR_EMPLOYEE_ONBOARDED` | UPPER_SNAKE_CASE |
| 4 | API Versioning | `api/v[major]` in URL | `/api/v1/...` | Major version only in URL |

## 4.3.2 Error Response Format

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `error` | string | Yes | `ERROR_CODE_IN_CAPS` (UPPER_SNAKE_CASE) |
| `message` | string | Yes | Human-readable description |
| `details` | object | No | Additional context / nested info |
| `correlation_id` | string | Yes | Maps to `X-Correlation-ID` header |

## 4.3.3 Logging & Observability Fields

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `timestamp` | ISO 8601 | Yes | UTC timestamp |
| `level` | string | Yes | `INFO`, `WARN`, `ERROR`, `DEBUG` |
| `service` | string | Yes | App/service name (e.g., `vfinance`) |
| `correlation_id` | string | Yes | End-to-end trace ID |
| `user_id` | string | Yes | Acting user ID |
| `event` | string | Yes | Event category (e.g., `API_CALL`) |
| `duration_ms` | integer | Yes | Request duration in milliseconds |

## Required HTTP Headers

| Header | Format | Purpose |
| --- | --- | --- |
| `X-Correlation-ID` | `req_[uuid]` | Mandatory on every request for tracing |
| `X-Request-ID` | string | Install API tracing |
| `X-App-ID` | string | Identifies calling App |
| `X-App-Secret` | string | App-level auth (permission injection) |
| `X-User-ID` | string | Audit trail attribution |
