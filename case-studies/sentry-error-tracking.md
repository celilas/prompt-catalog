# Case Study: Sentry — Error Tracking Platform

> **Project:** [getsentry/sentry](https://github.com/getsentry/sentry)
> **Domain:** Cloud-native SaaS, Observability
> **Stack:** Python (Django), React, PostgreSQL, ClickHouse, Kafka, Redis, Snuba
> **Scale:** Processes billions of events/day, multi-region, self-hosted + SaaS

## Project Overview

Sentry is an open-source application monitoring and error-tracking platform. It ingests error events, stack traces, and performance data from client SDKs across dozens of languages, processes them in near-real-time, and presents actionable dashboards to developers.

Key technical challenges:
- **High-throughput event ingestion** (millions of events per second)
- **Multi-tenant architecture** with per-organization rate limiting and quotas
- **Complex data pipeline** (Kafka → processing → ClickHouse/PostgreSQL)
- **Self-hosted and SaaS** deployment models from the same codebase

## Prompt Mapping

If you were building Sentry from scratch with AI assistance, here's the prompt stack you'd use:

### Phase 1: Planning & Architecture

| Prompt | Why |
|--------|-----|
| `PLAN-REQ-001` | Elicit requirements: SDKs, event ingestion, alerting, integrations |
| `PLAN-REQ-002` | Non-functional requirements are critical: throughput (billions/day), latency (< 1s to dashboard), availability (99.9%+) |
| `ARCH-SYS-001` | Overall system architecture — this is a complex distributed system |
| `ARCH-MICRO-001` | Sentry is microservices-oriented: relay (Rust ingestion), snuba (query), symbolicator, etc. |
| `ARCH-CLOUD-001` | Multi-region deployment, hybrid cloud (self-hosted + SaaS) |
| `ARCH-DATA-001` | Dual storage: PostgreSQL for metadata, ClickHouse for time-series event data |

### Phase 2: Implementation

| Prompt | Why |
|--------|-----|
| `DEV-WEB-001` | React frontend (dashboard) |
| `DEV-API-001` | REST API for SDKs, integrations, and the web UI |
| `SEC-THREAT-001` | Threat model: multi-tenant data isolation, API key security, PII in error events |
| `SEC-CODE-001` | SDK ingestion is an attack surface — untrusted input from the internet |

### Phase 3: Operations

| Prompt | Why |
|--------|-----|
| `DEPLOY-IAC-001` | ClickHouse clusters, Kafka, PostgreSQL — all require IaC |
| `DEPLOY-CICD-001` | Complex CI/CD with SDK matrix testing across languages |
| `OPS-MON-001` | "Who monitors the monitor?" — Sentry needs its own observability stack |

## What Prompts Would Have Caught

These are real issues from Sentry's public history that catalog prompts explicitly address:

### 1. ClickHouse Query Performance (ARCH-DATA-001)

**Issue:** Sentry's migration from PostgreSQL to ClickHouse for event data required careful schema design. Early ClickHouse schemas led to expensive `ORDER BY` operations on high-cardinality columns.

**What the prompt catches:**
> `ARCH-DATA-001` Section 3 (Data Modeling): "Define **indexing strategy** aligned with query patterns — not just write patterns" and "Consider write vs. read optimization trade-offs for your storage engine"

A developer using this prompt would have been directed to design the ClickHouse schema around query patterns (filter by project → time range → error type) from the start.

### 2. Multi-Tenant Data Leakage Risk (SEC-THREAT-001)

**Issue:** In any multi-tenant system, the #1 security concern is data leaking between tenants. Sentry has handled multiple reports around tenant isolation in their self-hosted and SaaS offerings.

**What the prompt catches:**
> `SEC-THREAT-001` requires modeling "authorization boundaries" and "data isolation between tenants." It explicitly calls out: "For multi-tenant systems, verify that every data access path includes tenant context filtering."

### 3. PII in Error Events (SEC-CODE-001 + DOM-COMPLIANCE-001)

**Issue:** Error events frequently contain PII (usernames, emails, IP addresses, file paths with usernames) that users don't intend to send. Sentry had to build extensive data scrubbing.

**What the prompt catches:**
> `SEC-CODE-001` Section on input handling: "Sanitize and validate ALL external input" and "Implement data classification for sensitive fields."
> `DOM-COMPLIANCE-001` Section 2: "Data classification engine — automatically classify data by sensitivity level" and "Data minimization — collect only what is necessary."

### 4. Self-Hosted Deployment Complexity (DEPLOY-IAC-001)

**Issue:** Sentry's self-hosted deployment involves 20+ Docker containers (PostgreSQL, ClickHouse, Kafka, Redis, Snuba, multiple Sentry workers) and has been a persistent source of community support burden.

**What the prompt catches:**
> `DEPLOY-IAC-001` Section 5 (Deployment Patterns): Requires documenting "deployment topology" and "environment parity." The prompt explicitly asks for "self-hosted installation documentation and validated deployment configurations."

## Variable Fill-In Example

Here's how you'd fill in `ARCH-MICRO-001` for Sentry:

```yaml
# ARCH-MICRO-001 variables for Sentry
system_description: >
  Application monitoring platform that ingests error events and performance
  data from client SDKs, processes them through a data pipeline, stores them
  in time-series and relational databases, and presents dashboards with
  alerting capabilities.

current_architecture: >
  Monolithic Django application evolving toward microservices. Current services:
  Relay (Rust, event ingestion/filtering), Snuba (Python, ClickHouse query layer),
  Symbolicator (Rust, stack trace symbolication), web UI (React SPA).

scalability_requirements: >
  Must handle 1M+ events/second at peak. Individual tenants can burst to
  100K events/minute. Storage: 90-day retention for events, 1-year for
  aggregated metrics. Multi-region with data residency requirements.

team_structure: >
  ~150 engineers across 20+ teams. Teams own vertical product areas
  (Issues, Performance, Replays, Crons) and horizontal platform teams
  (Infrastructure, SDK, Pipeline, Storage).
```

## Instruction Stack

For building a Sentry-like system, load these instructions in order:

```
1. instructions/guardrails/accuracy.instructions.md    — Prevent hallucination
2. instructions/guardrails/security.instructions.md     — Security baseline
3. instructions/guardrails/performance.instructions.md  — Performance-critical system
4. instructions/platforms/cloud.instructions.md          — Cloud deployment
5. instructions/platforms/web.instructions.md            — Web dashboard
6. instructions/phases/design.instructions.md            — Architecture phase
7. instructions/guardrails/adversarial-evaluation.instructions.md — Stress-test designs
```

## Lessons for AI-Assisted Development

1. **Start with non-functional requirements.** Sentry's architecture is driven almost entirely by throughput and latency requirements. `PLAN-REQ-002` forces you to specify these before writing code.

2. **Data architecture is the hardest decision.** The PostgreSQL → ClickHouse migration was years of work. `ARCH-DATA-001` pushes early consideration of storage engines, query patterns, and migration paths.

3. **Multi-tenancy isn't an afterthought.** Every query, every cache key, every background job must be tenant-scoped. `SEC-THREAT-001` forces threat modeling of tenant isolation before implementation.

4. **Observability for observability tools is non-trivial.** `OPS-MON-001` applied to itself — who monitors the monitoring system? This requires careful dependency analysis.
