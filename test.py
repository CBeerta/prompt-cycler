from prompt_cycler import PromptCycler

if __name__ == "__main__":
    cycler = PromptCycler()

    append = "{red|green|blue} does {booo|baaah}"
    appendlist = ["{red|green|blue} does {booo|baaah}", "{red|green|blue} does {booo|baaah}", "{red|green|blue} does {booo|baaah}"]

    print(cycler.cycle_prompt(seed=0, append=append, trigger_words="lala", filename="doesnotexist.txt", prompt_index=4))
    print(cycler.cycle_prompt(seed=234823949237, append=append, trigger_words="lala", filename="doesnotexist.txt", prompt_index=0))
    print(cycler.cycle_prompt(seed=0, append=append, trigger_words="lala", filename="doesnotexist.txt", prompt_index=20))
    print(cycler.cycle_prompt(seed=0, append=appendlist, trigger_words="lala", filename="doesnotexist.txt", prompt_index=4))

    print(cycler.cycle_prompt(seed=0, append=append, trigger_words="lala", filename="empty.txt", prompt_index=0))

