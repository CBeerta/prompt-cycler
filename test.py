from prompt_cycler import PromptCycler

if __name__ == "__main__":
    cycler = PromptCycler()

    prompt = "{red|green|blue} does {booo|baaah}"

    print(cycler.cycle_prompt(seed=0, append=prompt, trigger_words="", filename="doesnotexist.txt", prompt_index=4))
    print(cycler.cycle_prompt(seed=234823949237, append=prompt, trigger_words="lala", filename="doesnotexist.txt", prompt_index=0))
    print(cycler.cycle_prompt(seed=0, append=prompt, trigger_words="", filename="empty.txt", prompt_index=0))
