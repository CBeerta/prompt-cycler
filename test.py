from prompt_cycler import PromptCycler

if __name__ == "__main__":
    cycler = PromptCycler()

    prompt = "{red|green|blue} does {booo|baaah}"

    print(cycler.cycle_prompt(seed=0, append=prompt, filename="doesnotexist.txt", cycle_mode="random", reset_cycle=False))
    print(cycler.cycle_prompt(seed=0, append=prompt, filename="empty.txt", cycle_mode="random", reset_cycle=False))
