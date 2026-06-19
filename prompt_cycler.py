import torch
import random
import re
from pathlib import Path
import spintax
import json
import glob

try:
    import folder_paths
except ModuleNotFoundError:
    pass


class PromptCycler:
    """
    A ComfyUI custom node that cycles through an infinite number of prompts.
    Supports both built-in example prompts and custom user-defined prompts.
    Each time the node is executed, it returns the next prompt in sequence or randomly.
    """

    def __init__(self):
        # Example prompts - users can provide their own via custom_prompts
        self.example_prompts = [
            "A majestic mountain landscape at sunset with golden light",
            "A futuristic city with flying cars and neon lights",
            "A peaceful forest with sunlight filtering through trees",
            "An underwater scene with colorful coral reefs and fish",
            "A cozy cabin in the woods during winter snowfall",
            "A space station orbiting a distant planet",
            "A bustling marketplace in an ancient city",
            "A serene lake with mountains reflected in the water",
            "A steampunk laboratory with brass gears and steam",
            "A magical garden with glowing flowers and butterflies",
            "A battlefield in the morning dusk littered with corpses",
        ]

        self.current_index = 0
        self.seed = 0

    @classmethod
    def INPUT_TYPES(cls):
        filenames = glob.glob("/data/claus/src/comfy/*.txt")
        if len(filenames) == 0:
            filenames = ["prompts.txt"]

        return {
            "required": {
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "step": 1,
                        "display": "number",
                    },
                ),
                "filename": (filenames, {"default": filenames[0]}),
                "prompt_index": ("INT", {"default": 0, "min": -1, "display": "number"}),
            },
            "optional": {
                "append": ("STRING", {"default": ""}),
                "trigger_words": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "INT", "STRING")
    RETURN_NAMES = ("prompt", "cycle_index", "description")
    FUNCTION = "cycle_prompt"
    CATEGORY = "text/prompt"

    seed = 0

    def cycle_prompt(
        self,
        seed: int,
        append: str,
        trigger_words: str,
        prompt_index: int,
        filename: str = "",
    ):
        """
        Cycle through prompts and return the current one.
        Supports infinite number of prompts via custom_prompts input.

        Args:
            seed: Random seed for reproducible results
            append: A Text (Spintax) to append to the randomly chosen prompt
            cycle_mode: "sequential" or "random" cycling
            reset_cycle: Whether to reset the cycle counter

        Returns:
            Tuple of (current_prompt, cycle_index)
        """

        # load file on every effin run please
        if Path(filename).exists():
            self.example_prompts = Path(filename).read_text().splitlines()

        # Use custom prompts if provided, otherwise use example prompts
        prompts_to_use = self.example_prompts

        # Set random seed for reproducible results
        self.seed = seed
        if seed != 0:
            random.seed(seed)
            torch.manual_seed(seed)

        cycle_index = prompt_index

        appends = append + (f", {trigger_words}, " if trigger_words else ", ")

        if prompt_index > 0 and prompt_index < len(prompts_to_use):  # index mode
            if prompt_index > len(prompts_to_use):
                prompt = appends
            else:
                prompt = prompts_to_use[prompt_index - 1] + ", " + appends
        elif len(prompts_to_use) == 0:  # no prompts in file, just append
            prompt = appends
        else:  # random mode
            cycle_index = random.randint(0, len(prompts_to_use) - 1)
            prompt = prompts_to_use[cycle_index] + ", " + appends

        if ";" in prompt:
            description = prompt.split(";")[0].strip()
            prompt = prompt.split(";")[1]
        else:
            description = "n/a"

        return (spintax.spin(prompt, seed=seed), cycle_index, description)


class CheckpointCycler:
    def __init__(self):
        self._counter = 0
        self._current_idx = 0

    @classmethod
    def INPUT_TYPES(cls):

        return {
            "required": {
                "pattern": (
                    "STRING",
                    {
                        "default": ".",
                        "multiline": False,
                    },
                ),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "step": 1,
                        "display": "number",
                    },
                ),
                "switch_every": ("INT", {"default": 1, "min": 1, "display": "number"}),
            },
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "cycle_checkpoint"
    CATEGORY = "text/prompt"

    def _get_all_checkpoints(self):
        """Get all checkpoint filenames from ComfyUI's checkpoint directory."""
        return folder_paths.get_filename_list("checkpoints")

    def _get_checkpoint_path(self, ckpt_name):
        """Get the full path to a checkpoint by name."""
        return folder_paths.get_full_path("checkpoints", ckpt_name) or ""

    def cycle_checkpoint(self, pattern: str, seed: int, switch_every: int = 1):
        all_ckpts = self._get_all_checkpoints()
        matched = [c for c in all_ckpts if re.search(pattern, c)]
        matched.sort()

        if not matched:
            return ("",)

        if seed != 0:
            random.seed(seed)

        if switch_every == 1:
            # Original behavior: random every time
            idx = random.randint(0, len(matched) - 1)
        else:
            # Cycling mode: stay on each checkpoint for switch_every calls
            if self._counter == 0:
                self._current_idx = random.randint(0, len(matched) - 1)
            elif self._counter >= switch_every:
                self._current_idx = (self._current_idx + 1) % len(matched)
                self._counter = 0
            idx = self._current_idx

        self._counter += 1
        ckpt = matched[idx]
        return (ckpt,)


def _load_styles():
    # style_file = Path(__file__).parent / "test-styles.json.json"
    # FIXME
    style_file = Path("/data/claus/src/comfy/easy-my-styles.json")
    if style_file.exists():
        with open(style_file) as f:
            return json.load(f)
    return []


class StyleCycler:
    def __init__(self):
        self._counter = 0
        self._current_idx = 0
        self._append_idx = 0

    @classmethod
    def INPUT_TYPES(cls):
        styles = _load_styles()
        style_names = sorted([s["name"] for s in styles])
        return {
            "required": {
                "style": (["random"] + style_names, {"default": "random"}),
                "seed": (
                    "INT",
                    {
                        "default": 0,
                        "min": 0,
                        "max": 0xFFFFFFFFFFFFFFFF,
                        "step": 1,
                        "display": "number",
                    },
                ),
                "switch_every": ("INT", {"default": 5, "min": 1, "display": "number"}),
                "append_random": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "prompt": ("STRING", {"default": ""}),
                "negative_prompt": ("STRING", {"default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("prompt", "negative_prompt", "style_name")
    FUNCTION = "cycle_style"
    CATEGORY = "text/prompt"

    @staticmethod
    def _dedupe_join(*parts: str) -> str:
        items: list[str] = []
        for part in parts:
            for s in part.split(", "):
                s = s.strip()
                if s and s not in items:
                    items.append(s)
        return ", ".join(items)

    def _next_cycled_index(self, switch_every, max_val, attr, exclude=None):
        should_init = self._counter == 0
        should_advance = self._counter >= switch_every

        val = getattr(self, attr)
        if switch_every == 1 or should_init:
            val = random.randint(0, max_val - 1)
        elif should_advance:
            val = (val + 1) % max_val

        if exclude is not None:
            while val == exclude:
                val = (val + 1) % max_val

        setattr(self, attr, val)
        return val

    def cycle_style(
        self,
        style: str,
        seed: int,
        switch_every: int = 1,
        prompt: str = "",
        negative_prompt: str = "",
        append_random: bool = False,
    ):
        styles = _load_styles()
        if not styles:
            return ("", "", "none")

        if seed != 0:
            random.seed(seed)

        if style == "random":
            idx = self._next_cycled_index(switch_every, len(styles), "_current_idx")
        else:
            idx = next((i for i, s in enumerate(styles) if s["name"] == style), 0)

        if append_random and len(styles) > 1:
            rnd_idx = self._next_cycled_index(
                switch_every, len(styles), "_append_idx", exclude=idx
            )

        if switch_every > 1 and (style == "random" or append_random):
            if self._counter >= switch_every:
                self._counter = 0
            self._counter += 1

        chosen = styles[idx]
        result_prompt = "{}, {} ".format(prompt, chosen["prompt"]).lstrip(", ")
        result_neg = "{}, {} ".format(
            negative_prompt, chosen["negative_prompt"]
        ).lstrip(", ")
        style_name = chosen["name"]

        if append_random:
            if len(styles) > 1:
                rnd = styles[rnd_idx]
                result_prompt = self._dedupe_join(
                    prompt, chosen["prompt"], rnd["prompt"]
                )
                result_neg = self._dedupe_join(
                    negative_prompt,
                    chosen["negative_prompt"],
                    rnd["negative_prompt"],
                )
                style_name = f"{chosen['name']}, {rnd['name']}"
            else:
                result_prompt = self._dedupe_join(prompt, chosen["prompt"])
                result_neg = self._dedupe_join(
                    negative_prompt, chosen["negative_prompt"]
                )
                style_name = chosen["name"]

        return (result_prompt, result_neg, style_name)


# Node class mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptCycler": PromptCycler,
    "CheckpointCycler": CheckpointCycler,
    "StyleCycler": StyleCycler,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCycler": "Prompt Cycler",
    "CheckpointCycler": "Checkpoint Cycler",
    "StyleCycler": "Style Cycler",
}
