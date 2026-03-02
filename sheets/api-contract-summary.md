# API Contract Summary

> Source: vKernel PRD Section 4.1

## Core Platform APIs

| # | API Name | Method | Endpoint | Auth | SyR Mapping | Description |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Install App | POST | `/api/v1/apps/install` | Bearer `<admin_token>` + `X-Request-ID` | SyR-PLAT-00 | Install a new Business App; triggers dependency check |
| 2 | Inject Permissions | POST | `/api/v1/iam/permissions/inject` | `X-App-ID` + `X-App-Secret` | SyR-PLAT-01 | App injects new permissions into AuthZ system on install |
| 3 | Extend Data Entity | PATCH | `/api/v1/data/entities/company/{id}/extend` | `X-App-ID` + `X-User-ID` | SyR-PLAT-02 | Extend a Core Entity with custom JSONB fields |
| 4 | Publish Event | POST | `/api/v1/events/publish` | `X-App-ID` + `X-Correlation-ID` | SyR-PLAT-03 | Publish an event to the Event Bus (Pub/Sub) |

## Response Code Summary

| API | Success | Error Codes |
| --- | --- | --- |
| Install App | `202 Accepted` (job_id, status: pending) | `400 MISSING_DEPENDENCY` |
| Inject Permissions | `201 Created` (injected_count, warning) | `409 PERMISSION_EXISTS` |
| Extend Data Entity | `200 OK` (entity_id, version, custom_fields) | — |
| Publish Event | `202 Accepted` (event_id, subscribers_notified) | — |

## Required Headers (All APIs)

| Header | Required By | Purpose |
| --- | --- | --- |
| `X-Request-ID` | Install App | Distributed tracing |
| `X-App-ID` | Permission Injection, Data Extension, Event Publish | Identifies calling App |
| `X-App-Secret` | Permission Injection | App-level authentication |
| `X-User-ID` | Data Extension | Audit trail attribution |
| `X-Correlation-ID` | Event Publish | End-to-end request tracing |
| `Authorization: Bearer` | Install App | Admin-level access token |

## Error Response Standard (§4.3.2)

All error responses follow this schema:

| Field | Type | Description |
| --- | --- | --- |
| `error` | string | `ERROR_CODE_IN_CAPS` |
| `message` | string | Human-readable message |
| `details` | object | Additional context (optional) |
| `correlation_id` | string | Request trace ID |
