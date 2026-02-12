# Opinionated Starter Kits

Starter kits are curated bundles of prompts and instructions designed for specific project types. Instead of choosing from 32 prompts and 18 instruction files, pick a kit and get a ready-to-use stack.

## Available Kits

| Kit | Target | Prompts | Instructions |
|-----|--------|---------|--------------|
| [SaaS Web App](saas-web-app.yaml) | Full-stack SaaS applications (Next.js, Rails, Django) | 12 | 6 |
| [API Backend](api-backend.yaml) | REST/GraphQL API services | 9 | 5 |
| [Mobile App](mobile-app.yaml) | iOS, Android, or cross-platform mobile | 10 | 5 |
| [Cloud Native](cloud-native.yaml) | Microservices on Kubernetes/serverless | 11 | 6 |
| [FinTech Platform](fintech-platform.yaml) | Financial services with compliance | 13 | 8 |
| [Healthcare App](healthcare-app.yaml) | HIPAA-compliant clinical applications | 13 | 8 |

## Using a Kit

### With the CLI

```bash
# List all available kits
prompt-catalog kit list

# View a kit's contents
prompt-catalog kit show saas-web-app

# Export a kit's prompts and instructions to a directory
prompt-catalog kit export saas-web-app --output ./my-project/.prompts

# Interactive mode — recommends a kit based on your answers
prompt-catalog start
```

### Manual Setup

1. Open the kit YAML file
2. Copy the listed instruction files into your project's `.github/instructions/` or `.vscode/` directory
3. Reference the prompt IDs when working with your AI coding agent

## Kit Philosophy

Each kit is **opinionated** — it makes choices so you don't have to:

- **Order matters.** Instructions are listed in the order they should be loaded. Guardrails come first, then platform specifics, then phase guidance.
- **Less is more.** Kits don't include every prompt — they include the right prompts for the project type.
- **Domain prompts are optional.** Base kits cover the engineering fundamentals. Add domain prompts when your project has regulatory or industry-specific needs.
- **Guardrails are non-negotiable.** Every kit includes accuracy and security guardrails. These are the baseline.

## Creating Custom Kits

Kit files are YAML with a simple schema:

```yaml
id: my-custom-kit
name: My Custom Kit
description: What this kit is for
target_audience: Who should use it

prompts:
  - PLAN-REQ-001
  - ARCH-SYS-001
  # ... prompt IDs from the catalog

instructions:
  - guardrails/accuracy
  - guardrails/security
  - platforms/web
  # ... instruction file stems (without .instructions.md)

tags:
  - custom
  - my-domain
```
