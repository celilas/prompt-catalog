"""
Prompt Catalog MCP Server.

Run with:
    prompt-catalog serve
    # or
    python -m prompt_catalog_mcp.server
"""

from __future__ import annotations

import os

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    Resource,
    TextContent,
)

from .catalog import Catalog

CATALOG_ROOT = os.environ.get("CATALOG_ROOT", os.getcwd())

app = Server("prompt-catalog")
_catalog: Catalog | None = None


def _get_catalog() -> Catalog:
    global _catalog
    if _catalog is None:
        _catalog = Catalog.load(CATALOG_ROOT)
    return _catalog


# ── Resources ────────────────────────────────────────────────────────


@app.list_resources()
async def list_resources() -> list[Resource]:
    catalog = _get_catalog()
    resources: list[Resource] = []

    for p in catalog.prompts.values():
        resources.append(
            Resource(
                uri=f"prompt-catalog://prompts/{p.category}/{p.id}",
                name=p.title,
                description=p.description,
                mimeType="text/yaml",
            )
        )

    for inst in catalog.instructions.values():
        resources.append(
            Resource(
                uri=f"prompt-catalog://instructions/{inst.scope}/{inst.stem}",
                name=inst.name,
                description=inst.description,
                mimeType="text/markdown",
            )
        )

    return resources


@app.read_resource()
async def read_resource(uri: str) -> str:
    catalog = _get_catalog()

    if uri.startswith("prompt-catalog://prompts/"):
        parts = uri.replace("prompt-catalog://prompts/", "").split("/")
        prompt_id = parts[-1] if parts else ""
        entry = catalog.prompts.get(prompt_id)
        if entry:
            return entry.file_path.read_text(encoding="utf-8")
        raise ValueError(f"Prompt not found: {prompt_id}")

    if uri.startswith("prompt-catalog://instructions/"):
        parts = uri.replace("prompt-catalog://instructions/", "").split("/")
        stem = parts[-1] if parts else ""
        entry = catalog.instructions.get(stem)
        if entry:
            return entry.file_path.read_text(encoding="utf-8")
        raise ValueError(f"Instruction not found: {stem}")

    raise ValueError(f"Unknown URI: {uri}")


# ── Prompt Templates ────────────────────────────────────────────────


@app.list_prompts()
async def list_prompts() -> list[Prompt]:
    catalog = _get_catalog()
    prompts: list[Prompt] = []

    for p in catalog.prompts.values():
        arguments = [
            PromptArgument(
                name=v["name"],
                description=v.get("description", ""),
                required=v.get("required", False),
            )
            for v in p.variables
        ]
        prompts.append(
            Prompt(
                name=p.id.lower(),
                description=p.description or p.title,
                arguments=arguments,
            )
        )

    return prompts


@app.get_prompt()
async def get_prompt(
    name: str, arguments: dict[str, str] | None = None
) -> GetPromptResult:
    catalog = _get_catalog()

    # Match by lowercase ID
    entry = None
    for p in catalog.prompts.values():
        if p.id.lower() == name.lower():
            entry = p
            break

    if not entry:
        raise ValueError(f"Prompt not found: {name}")

    rendered = entry.render(arguments)

    return GetPromptResult(
        description=entry.description or entry.title,
        messages=[
            PromptMessage(
                role="user",
                content=TextContent(type="text", text=rendered),
            )
        ],
    )


# ── Entry point ──────────────────────────────────────────────────────


async def run():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options(),
        )


def main():
    import asyncio

    asyncio.run(run())


if __name__ == "__main__":
    main()
