# Case Study: Cal.com — Scheduling SaaS Platform

> **Project:** [calcom/cal.com](https://github.com/calcom/cal.com)
> **Domain:** SaaS Web Application, Scheduling
> **Stack:** Next.js, TypeScript, tRPC, Prisma, PostgreSQL, Tailwind CSS
> **Scale:** Open-source Calendly alternative — team scheduling, booking pages, calendar integrations

## Project Overview

Cal.com is an open-source scheduling platform (the "Calendly alternative"). It provides individual and team booking pages, calendar integrations (Google, Outlook, Apple), video conferencing integrations (Zoom, Meet, Teams), payment collection (Stripe), and workflow automations.

Key technical challenges:
- **Calendar complexity** — timezone handling, recurring events, availability algorithms, multi-calendar conflict detection
- **Multi-tenancy** — SaaS with per-organization settings, plus self-hosted option
- **Integration density** — 100+ third-party integrations (calendars, video, payments, CRMs)
- **Real-time availability** — must check availability across multiple calendars in real-time

This case study is particularly useful because Cal.com represents the **most common project type** — a SaaS web application — and maps directly to the `saas-web-app` starter kit.

## Prompt Mapping

### The SaaS Web App Stack

| Prompt | Why |
|--------|-----|
| `PLAN-REQ-001` | Requirements from end users (bookers), admins (team managers), and developers (self-hosted) |
| `PLAN-REQ-003` | User stories: "As a busy professional, I want to share my booking link so that clients can book time without email back-and-forth" |
| `ARCH-SYS-001` | Monorepo architecture with apps/web, packages/lib, packages/prisma, packages/trpc |
| `DEV-WEB-001` | Next.js with App Router, React Server Components, tRPC for type-safe APIs |
| `DEV-API-001` | tRPC API layer + REST webhooks for integrations |
| `SEC-THREAT-001` | OAuth tokens for calendar access, multi-tenant data isolation |
| `TEST-UNIT-001` | Timezone logic, availability algorithms, recurring event expansion |
| `TEST-INT-001` | Calendar API integration tests, booking flow end-to-end |
| `DEPLOY-CICD-001` | Turborepo monorepo CI/CD, Docker for self-hosted, Vercel for SaaS |

## What Prompts Would Have Caught

### 1. Timezone Bugs

**Issue:** Timezone handling is notoriously difficult. Cal.com has had numerous timezone-related bugs: bookings showing at wrong times, DST transitions creating phantom availability or double-bookings, and timezone display inconsistencies between booker and host.

**What the prompt catches:**
> `DEV-WEB-001` Section on state management: "Handle **timezone and locale** correctly — store timestamps in UTC, display in user's local timezone."
> `TEST-UNIT-001` would generate boundary tests: "Test DST transitions, UTC+13/UTC-12 edge cases, half-hour timezone offsets (India, Nepal)."

**Concrete impact:** An AI agent with these prompts would store all times as UTC in the database, perform availability calculations in UTC, and convert to local timezone only at the display layer. It would also generate test cases for DST transitions and unusual timezone offsets.

### 2. OAuth Token Management

**Issue:** Cal.com connects to Google Calendar, Outlook, Zoom, and others via OAuth. Token refresh failures, token expiry during long-running operations, and secure token storage are persistent challenges.

**What the prompt catches:**
> `SEC-THREAT-001` would model "third-party credential storage" as a high-value asset and require encrypted storage, automatic refresh before expiry, and graceful degradation when refresh fails.
> `SEC-CODE-001` specifies: "Implement credential rotation and detect leaked credentials."

### 3. Race Conditions in Booking

**Issue:** When multiple people try to book the same slot simultaneously, without proper concurrency control, double bookings occur. This is a classic race condition.

**What the prompt catches:**
> `ARCH-SYS-001` covers concurrency: "Implement **optimistic or pessimistic locking** for resources with contention."
> `DOM-FINTECH-001` (the financial parallel): "Implement **optimistic locking** for concurrent financial operations" — the same pattern applies to booking slot contention.
> `TEST-INT-001` with adversarial tests: the `adversarial_tests` field would include `{ scenario: "Concurrent booking of the same slot by 10 users", expected_behavior: "Exactly one booking succeeds, others receive conflict error" }`.

### 4. API Rate Limiting for Calendar Sync

**Issue:** Google Calendar API has rate limits (typically 100 queries per 100 seconds per user). Bulk operations (initial calendar sync, large team booking) can hit these limits, causing sync failures.

**What the prompt catches:**
> `DEV-API-001` Section on API design: "Implement **rate limiting** — per-user, per-IP, per-operation limits" and "Design for third-party API rate limits with **backoff and retry**."
> `ARCH-SYS-001` Section on resilience: "Implement **circuit breakers** for external service calls."

## Variable Fill-In Example

```yaml
# ARCH-SYS-001 variables for Cal.com
project_name: "Cal.com — Open Source Scheduling Platform"

system_description: >
  Scheduling SaaS that provides booking pages for individuals and teams.
  Users connect their calendars (Google, Outlook, Apple), set availability
  rules, and share booking links. The system checks real-time availability
  across connected calendars, handles timezone conversion, collects payments
  via Stripe, and triggers video conferencing links on booking.

stakeholders: >
  End users (hosts setting up booking pages), bookers (external people
  booking time), team admins (managing organization settings), self-hosted
  deployers, integration partners, open-source contributors.

constraints: >
  Must work as both SaaS (Vercel) and self-hosted (Docker). Real-time
  availability checks must complete in under 2 seconds. Must support
  100+ integrations with graceful degradation. GDPR compliance for EU
  users. Monorepo architecture with Turborepo.

technology_preferences: >
  Next.js 14+ (App Router), TypeScript (strict mode), tRPC for API layer,
  Prisma ORM with PostgreSQL, Tailwind CSS, Turborepo for monorepo.
```

## Starter Kit Mapping

Cal.com maps directly to the **`saas-web-app`** starter kit:

```bash
prompt-catalog kit show saas-web-app
```

This kit includes exactly the prompts listed above, plus the instruction files for web development, security, and testing — the complete stack for AI-assisted SaaS development.

## Instruction Stack

```
1. instructions/guardrails/accuracy.instructions.md      — Prevent hallucinated APIs
2. instructions/guardrails/security.instructions.md       — OAuth token handling
3. instructions/platforms/web.instructions.md              — Next.js, React patterns
4. instructions/phases/design.instructions.md              — Architecture decisions
5. instructions/phases/testing.instructions.md             — Timezone and concurrency tests
6. instructions/guardrails/adversarial-evaluation.instructions.md — Race conditions, edge cases
```

## Lessons for AI-Assisted Development

1. **The `saas-web-app` starter kit fits most projects.** Cal.com is a SaaS web app, but so are most of the projects developers are building. This case study validates the starter kit's prompt selection.

2. **Timezone handling is where AI agents hallucinate most.** Without explicit instructions to "store UTC, display local," AI agents often generate code that stores local times, leading to bugs that only appear across timezones. The web platform instruction file prevents this.

3. **Concurrency testing is undertested by default.** AI agents rarely generate race condition tests unless explicitly prompted. The adversarial evaluation guardrail and `TEST-INT-001`'s adversarial_tests field catch this gap.

4. **Integration density requires resilience patterns.** Cal.com's 100+ integrations mean any external service can fail at any time. The prompts' emphasis on circuit breakers, retry with backoff, and graceful degradation prevents cascading failures.
