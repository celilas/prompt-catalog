"""Shared fixtures for prompt-catalog tests."""

from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest
import yaml


@pytest.fixture
def catalog_root(tmp_path: Path) -> Path:
    """Create a minimal valid catalog structure in a temp directory."""

    # -- schema --
    schema_dir = tmp_path / "schema"
    schema_dir.mkdir()

    prompt_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Prompt",
        "type": "object",
        "required": ["id", "name", "category", "description", "prompt"],
        "properties": {
            "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
            "name": {"type": "string"},
            "category": {
                "type": "string",
                "enum": ["planning", "architecture", "development", "testing",
                         "security", "deployment", "operations", "domains"],
            },
            "description": {"type": "string"},
            "skill_level": {
                "type": "string",
                "enum": ["beginner", "intermediate", "advanced", "expert"],
            },
            "platforms": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": ["all", "web", "windows", "linux", "cloud"],
                },
            },
            "tags": {"type": "array", "items": {"type": "string"}},
            "prompt": {"type": "string"},
            "variables": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["name", "description"],
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": "string"},
                        "example": {"type": "string"},
                    },
                },
            },
            "related_prompts": {"type": "array", "items": {"type": "string"}},
        },
    }
    (schema_dir / "prompt.schema.json").write_text(json.dumps(prompt_schema, indent=2))

    # -- prompts --
    planning_dir = tmp_path / "prompts" / "planning"
    planning_dir.mkdir(parents=True)

    good_prompt = {
        "id": "test-prompt-1",
        "name": "Test Prompt",
        "title": "Test Prompt",
        "category": "planning",
        "description": "A test prompt for unit testing.",
        "skill_level": "beginner",
        "platforms": ["all"],
        "tags": ["test"],
        "prompt": "Generate a plan for {{project_name}} using {{methodology}}.",
        "variables": [
            {"name": "project_name", "description": "Name of the project", "example": "MyApp"},
            {"name": "methodology", "description": "Methodology to use", "example": "agile"},
        ],
        "related_prompts": [],
    }
    (planning_dir / "test-prompt-1.yaml").write_text(yaml.dump(good_prompt, default_flow_style=False))

    second_prompt = {
        "id": "test-prompt-2",
        "name": "Second Prompt",
        "title": "Second Prompt",
        "category": "planning",
        "description": "Another prompt.",
        "skill_level": "intermediate",
        "platforms": ["web", "linux"],
        "tags": ["test", "planning"],
        "prompt": "Review the architecture for {{project_name}}.",
        "variables": [
            {"name": "project_name", "description": "Name of the project"},
        ],
        "related_prompts": ["test-prompt-1"],
    }
    (planning_dir / "test-prompt-2.yaml").write_text(yaml.dump(second_prompt, default_flow_style=False))

    # -- instructions --
    guardrails_dir = tmp_path / "instructions" / "guardrails"
    guardrails_dir.mkdir(parents=True)

    instruction_md = textwrap.dedent("""\
        ---
        name: Test Guardrail
        description: A guardrail for testing
        ---

        # Test Guardrail

        This is the content of the test guardrail instruction.
        It has enough content to pass the length check in the validator.
    """)
    (guardrails_dir / "test-guard.instructions.md").write_text(instruction_md)

    # -- starter kit --
    kits_dir = tmp_path / "starter-kits"
    kits_dir.mkdir()

    kit = {
        "id": "test-kit",
        "name": "Test Kit",
        "description": "A starter kit for testing.",
        "target_audience": "testers",
        "prompts": ["test-prompt-1", "test-prompt-2"],
        "instructions": ["guardrails/test-guard"],
        "tags": ["test"],
    }
    (kits_dir / "test-kit.yaml").write_text(yaml.dump(kit, default_flow_style=False))

    # -- index.json --
    index = {
        "version": "1.0",
        "statistics": {"total_prompts": 2},
        "prompts": [
            {
                "id": "test-prompt-1",
                "name": "Test Prompt",
                "file": "prompts/planning/test-prompt-1.yaml",
                "category": "planning",
            },
            {
                "id": "test-prompt-2",
                "name": "Second Prompt",
                "file": "prompts/planning/test-prompt-2.yaml",
                "category": "planning",
            },
        ],
        "instructions": [
            {
                "id": "test-guard",
                "name": "Test Guardrail",
                "file": "instructions/guardrails/test-guard.instructions.md",
                "scope": "guardrails",
            },
        ],
        "chains": [],
        "starter_kits": [
            {
                "id": "test-kit",
                "name": "Test Kit",
                "file": "starter-kits/test-kit.yaml",
            },
        ],
    }
    (tmp_path / "prompts" / "index.json").write_text(json.dumps(index, indent=2))

    return tmp_path
