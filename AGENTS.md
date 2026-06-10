# AGENTS.md

## What this is

ComfyUI custom node package with 3 nodes: `PromptCycler`, `CheckpointCycler`, `StyleCycler`. Exposed via `NODE_CLASS_MAPPINGS` dict. Installed as a custom_nodes/ subfolder in ComfyUI.

## Commands

- **Install deps**: `uv sync` (or `uv sync --group dev` for dev extras)
- **Run tests**: `uv run python test.py` (raw script, not pytest — no test framework)
- **Format**: `uv run black .` (line-length 88)
- **Lint**: `uv run flake8`
- **Typecheck**: `uv run mypy .` (strict: `disallow_untyped_defs = true`)
- **Build**: `uv build`

## Architecture

- `prompt_cycler.py` — all 3 node classes + the ComfyUI registration dicts
- `__init__.py` — re-exports `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
- Single package, no monorepo, no generated code, no migrations.

## Quirks & gotchas

- **`prompt_index=0` / `prompt_index=-1`** = random mode (not sequential). Positive index = 1-based selection.
- **Prompts loaded from file on every execution** — the `filename` input is re-read each cycle_prompt call.
- **`test.py` StyleCycler tests** depend on a style JSON file at a hardcoded path (`/data/claus/src/comfy/easy-my-styles.json`). Will fail without it.
- **`folder_paths` import** is wrapped in try/except — `CheckpointCycler` and `StyleCycler` silently no-op outside ComfyUI.
- **Hardcoded local paths**: `glob.glob("/data/claus/src/comfy/*.txt")` in `INPUT_TYPES` and the style JSON path above. These are machine-specific and won't resolve elsewhere.
- **Spintax** (`{opt1|opt2}` syntax) is processed on every returned prompt via `spintax.spin()`.
- **Prompt file format**: lines can contain `;` to separate description from prompt (e.g. `"sunset;A sunset scene"` → description=`"sunset"`, prompt=`"A sunset scene"`).
- **`seed=0`** means no seeding — results are truly random each call.
- **`uv.lock` is gitignored** — the project uses pip/requirements.txt, not uv lockfiles.

## No existing AGENTS.md or .cursorrules was present before this file.
