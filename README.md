# ComfyUI Prompt Cycler Node

A custom ComfyUI node pack that provides 3 nodes for cycling prompts, checkpoints, and styles during batch generation.

## Nodes

### Prompt Cycler
Cycles through prompts loaded from a text file. Supports random and index-based selection.

### Parameters

| Param | Type | Description |
|-------|------|-------------|
| `seed` | INT | Random seed (0 = no seed, results are random each call) |
| `filename` | STRING | Path to a text file with prompts (one per line) |
| `prompt_index` | INT | `0` or `-1` = random mode, positive value = 1-based selection |
| `append` | STRING | Spintax text to append after the chosen prompt |
| `trigger_words` | STRING | Comma-separated words appended after `append` |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| `prompt` | STRING | Selected prompt with spintax processed and append/trigger_words applied |
| `cycle_index` | INT | The prompt index used (0-based) |
| `description` | STRING | Text before `;` in the prompt line, or `"n/a"` if no separator |

### Prompt file format

- One prompt per line.
- Lines can use `;` to separate a description from the prompt text: `"sunset;A sunset scene"` → description=`"sunset"`, prompt=`"A sunset scene"`.
- **Spintax** (`{opt1|opt2}`) is processed on every returned prompt.

### Can't I select prompts sequentially?

No — use the index input with a counter node if you need sequential selection.

---

### Checkpoint Cycler
Cycles through ComfyUI checkpoint files matching a pattern.

| Param | Type | Description |
|-------|------|-------------|
| `pattern` | STRING | Regex to filter checkpoint filenames (default: `.`) |
| `seed` | INT | Random seed (0 = no seed) |
| `switch_every` | INT | Stay on each checkpoint for N calls (1 = random every time) |

Outputs a single STRING with the checkpoint filename. Empty string if no checkpoints match.

---

### Style Cycler
Cycles through styles loaded from a JSON file.

| Param | Type | Description |
|-------|------|-------------|
| `style` | STRING | Style name from the JSON, or `"random"` |
| `seed` | INT | Random seed (0 = no seed) |
| `switch_every` | INT | Stay on each style for N calls (1 = random every time) |
| `prompt` | STRING | Base prompt to prepend the style prompt to |
| `negative_prompt` | STRING | Base negative prompt to prepend the style's negative prompt to |
| `append_random` | BOOLEAN | When `True`, append a second random style (deduped). Works with any `style` value including `"random"`. |

Outputs `(prompt, negative_prompt, style_name)`.

---

## Installation

```bash
cd ComfyUI/custom_nodes
git clone ssh://git@forgejo.svc.beerta.net:30022/claus/prompt-cycler.git
cd prompt-cycler
pip install -r requirements.txt
```

Restart ComfyUI afterwards. All 3 nodes appear in the `"text/prompt"` category.

Originally created by **Anton Tenitsky**. This fork maintains the project at [forgejo.svc.beerta.net](https://forgejo.svc.beerta.net/claus/prompt-cycler).

## Development

```bash
uv sync --group dev
uv run python test.py    # run tests
uv run black .           # format
uv run flake8            # lint
uv run mypy .            # typecheck
```

## License

MIT
