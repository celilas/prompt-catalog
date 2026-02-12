# Real-World Case Studies

These case studies analyze well-known open-source projects through the lens of the Prompt Catalog. Each study shows:

1. **What the project is** and what domain it operates in
2. **Which prompts and instructions would apply** if you were building it with AI assistance
3. **What the prompts would have caught** — mistakes the project actually encountered (from public issues/post-mortems) that our prompts explicitly guard against
4. **Practical prompt usage** — how to fill in the variables for this specific project

## Case Studies

| Case Study | Domain | Project | Key Takeaways |
|-----------|--------|---------|---------------|
| [Sentry](sentry-error-tracking.md) | Cloud-native SaaS | [getsentry/sentry](https://github.com/getsentry/sentry) | Microservices architecture, multi-tenancy, observability |
| [Medplum](medplum-healthcare.md) | Healthcare | [medplum/medplum](https://github.com/medplum/medplum) | HIPAA, HL7 FHIR, clinical safety, PHI handling |
| [Maybe Finance](maybe-personal-finance.md) | FinTech | [maybe-finance/maybe](https://github.com/maybe-finance/maybe) | Financial data integrity, decimal arithmetic, multi-currency |
| [Cal.com](calcom-scheduling-saas.md) | SaaS Web App | [calcom/cal.com](https://github.com/calcom/cal.com) | Web app architecture, API design, multi-tenancy, testing |

## How to Read These

Each case study follows this structure:

1. **Project Overview** — What it does, tech stack, scale
2. **Prompt Mapping** — Which catalog prompts apply and why
3. **What Prompts Would Have Caught** — Real issues from the project's history
4. **Variable Fill-In** — Concrete example of filling in prompt variables for this project
5. **Instruction Stack** — Which instruction files to load and in what order
6. **Lessons Learned** — What we can learn from this project about AI-assisted development
