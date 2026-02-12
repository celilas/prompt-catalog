# Case Study: Maybe Finance — Personal Finance Application

> **Project:** [maybe-finance/maybe](https://github.com/maybe-finance/maybe)
> **Domain:** FinTech, Personal Finance
> **Stack:** Ruby on Rails, Hotwire/Stimulus, PostgreSQL, Sidekiq
> **Scale:** Self-hosted personal finance management — net worth tracking, investment portfolios, budgeting

## Project Overview

Maybe is an open-source personal finance application that was originally a funded startup ($2M+), shut down, then open-sourced. It tracks net worth across bank accounts, investment portfolios, real estate, and other assets. It connects to financial institutions via Plaid to sync transactions.

Key technical challenges:
- **Financial data accuracy** — monetary calculations must be precise
- **Multi-currency support** — assets in different currencies with real-time conversion
- **Third-party financial integrations** — Plaid, Synth (market data), exchange rate APIs
- **Investment portfolio tracking** — positions, lots, cost basis, unrealized gains/losses

## Prompt Mapping

| Prompt | Why |
|--------|-----|
| `DOM-FINTECH-001` | **Primary domain prompt** — financial data integrity, decimal types, reconciliation |
| `PLAN-REQ-001` | Requirements: account aggregation, net worth, transaction categorization, budgeting |
| `ARCH-SYS-001` | Monolith architecture (Rails), background jobs, external API integrations |
| `ARCH-DATA-001` | Financial data schema: accounts, transactions, holdings, balances, historical snapshots |
| `DEV-WEB-001` | Rails + Hotwire frontend |
| `SEC-THREAT-001` | Financial credentials (Plaid tokens), PII, account balances |
| `TEST-UNIT-001` | Financial calculations require exhaustive boundary testing |

## What Prompts Would Have Caught

### 1. Floating-Point Money Arithmetic

**Issue:** This is the single most common error in financial software. Any use of `float` or `double` for monetary values introduces rounding errors. For example, `0.1 + 0.2 = 0.30000000000000004` in IEEE 754 floating point.

**What the prompt catches:**
> `DOM-FINTECH-001` Section 2 (Financial Data Integrity): "Use **decimal types** for monetary values — NEVER floating point." This is also listed as the #1 anti-pattern: "Using floating point for money."

**How the AI would apply it:** An AI agent with this prompt loaded would generate all monetary columns as `decimal(19,4)` in PostgreSQL, use `BigDecimal` in Ruby, and reject any PR that introduces `float` for money. The prompt is absolute — "NEVER" — giving the AI no room for ambiguity.

### 2. Missing Reconciliation Process

**Issue:** When syncing transactions from Plaid, discrepancies can arise — Plaid may update or remove transactions retroactively, timestamps may shift, and balance calculations may not match the institution's reported balance.

**What the prompt catches:**
> `DOM-FINTECH-001` Section 2: "Implement **double-entry bookkeeping** or equivalent reconciliation" and "Design for **eventual consistency** with reconciliation processes."
> Anti-pattern: "No reconciliation process."

An AI agent would have generated a reconciliation service that compares synced transaction totals against reported balances, flags discrepancies, and provides a resolution workflow.

### 3. Multi-Currency Rounding

**Issue:** Converting between currencies introduces rounding decisions. JPY has 0 decimal places, USD has 2, BTC has 8. Net worth aggregation across currencies requires consistent rounding rules and a clear "display currency" vs. "native currency" distinction.

**What the prompt catches:**
> `DOM-FINTECH-001` Section 6 (Testing): "**Currency tests** — multi-currency rounding, conversion, display." The prompt forces the developer to think about this during architecture, not after bugs appear.

### 4. Transaction Idempotency

**Issue:** Plaid webhooks can fire multiple times for the same transaction update. Without idempotency keys, duplicate transactions get created.

**What the prompt catches:**
> `DOM-FINTECH-001` Section 2: "All financial operations must be **idempotent** (handle retries safely)" and "Every transaction must have a unique, immutable **transaction ID**."

## Variable Fill-In Example

```yaml
# DOM-FINTECH-001 variables for Maybe
application_type: >
  Personal finance management platform — net worth tracking across
  bank accounts, investments, real estate, crypto, and vehicles with
  Plaid-based account aggregation and manual entry.

financial_operations: >
  Transaction syncing and categorization, balance calculation,
  investment portfolio tracking (positions, lots, cost basis),
  net worth computation across asset classes, budget tracking.

jurisdiction: >
  United States (primary), with multi-currency support for
  international accounts and investments.

compliance_frameworks: >
  Not PCI-DSS (no card processing). Plaid handles bank auth.
  Focus: data accuracy, user data privacy (CCPA if applicable),
  secure credential storage.

integration_partners: >
  Plaid (account aggregation, transactions), Synth (market data,
  stock prices), exchange rate APIs (currency conversion),
  manual CSV import/export.
```

## Instruction Stack

```
1. instructions/guardrails/accuracy.instructions.md     — Financial calculations must be exact
2. instructions/guardrails/security.instructions.md      — Protect financial credentials
3. instructions/platforms/web.instructions.md             — Rails web application
4. instructions/phases/implementation.instructions.md     — Code quality for financial logic
5. instructions/phases/testing.instructions.md            — Financial calculations need exhaustive tests
```

## Lessons for AI-Assisted Development

1. **"NEVER floating point for money" is a perfect AI instruction.** It's absolute, unambiguous, and prevents the most common financial software error. Prompts work best when they give AI agents clear, non-negotiable rules.

2. **Domain prompts surface requirements you'd forget to ask for.** Most developers wouldn't think to ask about "reconciliation processes" or "idempotent financial operations" when starting a personal finance app. The domain prompt makes these requirements explicit.

3. **Anti-patterns are as valuable as best practices.** The `DOM-FINTECH-001` anti-patterns list ("Using floating point for money", "Missing audit trail", "No reconciliation process") gives AI agents a checklist of what NOT to do — which is often more actionable than what to do.

4. **Testing prompts for financial software need specific guidance.** Generic "write unit tests" isn't sufficient. `DOM-FINTECH-001`'s testing section specifies reconciliation tests, boundary tests with min/max amounts, and multi-currency rounding tests — exactly the tests that catch financial bugs.
