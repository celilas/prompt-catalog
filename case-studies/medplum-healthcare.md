# Case Study: Medplum — Healthcare Infrastructure Platform

> **Project:** [medplum/medplum](https://github.com/medplum/medplum)
> **Domain:** Healthcare, HL7 FHIR, Clinical Applications
> **Stack:** TypeScript, React, Node.js, PostgreSQL, Redis, AWS
> **Scale:** FHIR-native healthcare API serving clinical applications, EHR integrations, patient portals

## Project Overview

Medplum is an open-source healthcare development platform that provides a FHIR-native API server, React component library, and deployment infrastructure for building clinical applications. It's the healthcare equivalent of Firebase — a backend-as-a-service specifically designed for healthcare data.

Key technical challenges:
- **FHIR R4 compliance** — full conformance with the HL7 FHIR specification (hundreds of resource types)
- **HIPAA Security Rule** — technical safeguards for Protected Health Information (PHI)
- **Clinical safety** — software used in healthcare contexts where errors can harm patients
- **Interoperability** — SMART on FHIR, FHIR Bulk Data, HL7v2 integration

## Prompt Mapping

### Core Architecture

| Prompt | Why |
|--------|-----|
| `DOM-HEALTHCARE-001` | **Primary domain prompt** — covers FHIR, HIPAA, clinical safety, PHI handling |
| `PLAN-REQ-001` | Requirements from clinicians, administrators, compliance officers |
| `PLAN-REQ-002` | Non-functional: HIPAA audit requirements, availability for clinical systems (99.99%), data integrity (RPO=0) |
| `ARCH-SYS-001` | Overall platform architecture (API server, auth, storage, subscriptions) |
| `ARCH-DATA-001` | FHIR resource storage in PostgreSQL — complex schema with versioning, compartments, search parameters |

### Security & Compliance

| Prompt | Why |
|--------|-----|
| `SEC-THREAT-001` | PHI is the highest-value target. Threat model: unauthorized PHI access, insider threats, API abuse |
| `SEC-CODE-001` | Every API endpoint handles PHI — input validation, output filtering, audit logging |
| `DOM-COMPLIANCE-001` | HIPAA, HITECH, SOC 2 Type II, state privacy laws |

### Operations

| Prompt | Why |
|--------|-----|
| `DEPLOY-IAC-001` | AWS infrastructure with HIPAA-eligible services only |
| `OPS-MON-001` | Monitoring that never logs PHI — operational visibility without data exposure |

## What Prompts Would Have Caught

### 1. PHI in Logs (DOM-HEALTHCARE-001)

**Issue:** Healthcare applications commonly leak PHI into application logs, error messages, and monitoring systems. This is a HIPAA violation. Log aggregation services (Datadog, Splunk) then become PHI processors requiring BAAs.

**What the prompt catches:**
> `DOM-HEALTHCARE-001` Section 4 (PHI Handling): "**NEVER** log PHI; use opaque identifiers in all logging" and "Error messages must not leak PHI to end users or logs."

An AI agent given this instruction would generate logging code that uses resource IDs instead of patient names, redacts PHI from error messages, and avoids including query parameters in access logs.

### 2. FHIR Search Parameter Complexity (ARCH-DATA-001)

**Issue:** FHIR defines hundreds of search parameters across resource types, including chained searches (`Patient?general-practitioner.name=Smith`), reverse includes, and composite parameters. Naive implementations either miss search parameters or implement them with N+1 queries.

**What the prompt catches:**
> `ARCH-DATA-001` Section 4 (Query Design): "Design query patterns before schema" and "Consider **search indexing strategy** aligned with actual query patterns."
> `DOM-HEALTHCARE-001` Section 1: "HL7 FHIR R4+ — Use FHIR resources as the primary data model for clinical data" and "FHIR resource mapping — map application entities to appropriate FHIR resources."

### 3. Audit Trail Requirements (DOM-COMPLIANCE-001)

**Issue:** HIPAA § 164.312(b) requires audit controls that "record and examine activity in information systems that contain or use ePHI." This means every read, write, update, and delete of any PHI-containing resource must be logged immutably.

**What the prompt catches:**
> `DOM-COMPLIANCE-001` Section 4 (Audit Trail): "Immutable audit logs — append-only logs that cannot be modified or deleted" and "What to log: Who, what, when, where, outcome for every regulated action."
> `DOM-HEALTHCARE-001` Section 2 (HIPAA Technical Safeguards) provides a specific mapping table: `164.312(b) | Audit controls | Immutable audit log of all PHI access`

### 4. Consent and Data Access Granularity (DOM-HEALTHCARE-001)

**Issue:** Patient consent in healthcare isn't binary. A patient may consent to sharing data with their primary care physician but not with a researcher. FHIR Consent resources and compartment-based access control are required.

**What the prompt catches:**
> `DOM-HEALTHCARE-001` Section 5: "Consent granularity — per-purpose consent (treatment, payment, operations, research)" and "Consent revocation — patients can revoke consent with downstream enforcement."

## Variable Fill-In Example

Here's how you'd fill in `DOM-HEALTHCARE-001` for Medplum:

```yaml
# DOM-HEALTHCARE-001 variables for Medplum
application_type: >
  FHIR-native healthcare development platform providing API server,
  React component library, and backend-as-a-service for building
  clinical applications (EHR, patient portals, care coordination).

data_standards: >
  HL7 FHIR R4 (full spec conformance), SMART on FHIR for app authorization,
  FHIR Bulk Data Access ($export), HL7v2 inbound integration, US Core
  Implementation Guide, USCDI v3.

regulatory_framework: >
  HIPAA Security Rule and Privacy Rule, HITECH Act, 21st Century Cures Act
  (information blocking provisions), ONC Health IT Certification criteria,
  SOC 2 Type II.

integration_requirements: >
  EHR integration (Epic FHIR APIs, Cerner), lab interfaces (HL7v2 ORU),
  pharmacy (NCPDP SCRIPT), payer APIs (Da Vinci), public health
  reporting (electronic case reporting).

user_types: >
  Healthcare developers (primary), clinicians (end-users of built apps),
  patients (portal access), administrators (access control, compliance),
  integration engineers (HL7v2/FHIR interface setup).
```

## Instruction Stack

```
1. instructions/guardrails/accuracy.instructions.md      — Critical: clinical context
2. instructions/guardrails/security.instructions.md       — PHI protection
3. instructions/guardrails/compliance.instructions.md     — HIPAA regulatory compliance
4. instructions/guardrails/adversarial-evaluation.instructions.md — Test against security threats
5. instructions/platforms/cloud.instructions.md            — AWS HIPAA-eligible deployment
6. instructions/platforms/web.instructions.md              — React component library
7. instructions/phases/design.instructions.md              — Architecture decisions
```

## Lessons for AI-Assisted Development

1. **Domain knowledge prevents dangerous errors.** Without `DOM-HEALTHCARE-001`, an AI agent would likely generate code that logs patient names, uses floating-point for dosage calculations, or stores PHI without encryption. These aren't just bugs — they're compliance violations and patient safety risks.

2. **Standards compliance requires specificity.** "Implement FHIR" is too vague — the prompt's specificity about FHIR R4, US Core, SMART on FHIR, and Bulk Data guides the AI toward the right implementation choices.

3. **Audit logging in healthcare is not optional.** Every prompt in the healthcare stack reinforces immutable audit trails. An AI agent that sees this instruction in the guardrails, the domain prompt, AND the compliance prompt will not skip it.

4. **The "never log PHI" instruction prevents the most common HIPAA violation.** Simple, clear, repeated across multiple instruction files — this is how you prevent AI-generated code from creating compliance exposure.
