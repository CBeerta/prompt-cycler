import torch
import random
from pathlib import Path
import spintax
import glob

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
            "A battlefield in the morning dusk littered with corpses"
        ]

        self.current_index = 0
        self.execution_count = 0
        self.seed = 0


    @classmethod
    def INPUT_TYPES(cls):
        filenames = glob.glob("/data/claus/src/comfy/*.txt")
        if len(filenames) == 0:
            filenames = ["prompts.txt"]
        
        return {
            "required": {
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                    "step": 1,
                    "display": "number"
                }),
                "filename": (filenames, {
                    "default": filenames[0]
                }),
                "cycle_mode": (["sequential", "random"], {
                    "default": "random"
                }),
                "reset_cycle": ("BOOLEAN", {
                    "default": False,
                    "display": "checkbox"
                })
            },
            "optional": {
                "append": ("STRING", {
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("STRING", "INT")
    RETURN_NAMES = ("prompt", "cycle_index")
    FUNCTION = "cycle_prompt"
    CATEGORY = "text/prompt"

    seed = 0

    def cycle_prompt(self, seed: int, append: str, cycle_mode: str, reset_cycle: bool, filename: str = ""):
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
        # FIXME: this should probably be customizable
        if Path(filename).exists():
            self.example_prompts = Path(filename).read_text().splitlines()

        # Use custom prompts if provided, otherwise use example prompts
        prompts_to_use = self.example_prompts

        # Reset cycle if requested
        if reset_cycle:
            self.current_index = 0
            self.execution_count = 0
        
        # Set random seed for reproducible results
        self.seed = seed
        if seed != 0:
            random.seed(seed)
            torch.manual_seed(seed)
        
        # Choose prompt based on cycle mode
        if cycle_mode == "sequential":
            prompt = prompts_to_use[self.current_index % len(prompts_to_use)]
            cycle_index = self.current_index % len(prompts_to_use)
            self.current_index += 1
        else:  # random mode
            cycle_index = random.randint(0, len(prompts_to_use) - 1)
            prompt = prompts_to_use[cycle_index]

        prompt = prompt + ", " + append

        self.execution_count += 1
       
        return (spintax.spin(prompt, seed=seed), cycle_index)


# Node class mapping for ComfyUI
NODE_CLASS_MAPPINGS = {
    "PromptCycler": PromptCycler
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PromptCycler": "Prompt Cycler"
}
