from prompt_cycler import PromptCycler

if __name__ == "__main__":
    cycler = PromptCycler()

    prompt = "{red|green|blue} does {booo|baaah}"

    print(cycler.cycle_prompt(seed=0, append=prompt, cycle_mode="random", reset_cycle=False, seed_spintax=False))

