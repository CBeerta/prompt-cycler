from prompt_cycler import PromptCycler, StyleCycler

if __name__ == "__main__":
    cycler = PromptCycler()

    prompt = "{red|green|blue} does {booo|baaah}"
    print("\n\nPromptCycler:\n")

    print(
        cycler.cycle_prompt(
            seed=0,
            append=prompt,
            trigger_words="lala",
            filename="doesnotexist.txt",
            prompt_index=4,
        )
    )
    print(
        cycler.cycle_prompt(
            seed=234823949237,
            append=prompt,
            trigger_words="lala",
            filename="doesnotexist.txt",
            prompt_index=0,
        )
    )

    print(
        cycler.cycle_prompt(
            seed=0,
            append=prompt,
            trigger_words="lala",
            filename="empty.txt",
            prompt_index=0,
        )
    )

    print(
        cycler.cycle_prompt(
            seed=0,
            append=prompt,
            trigger_words="lala",
            filename="testfile.txt",
            prompt_index=0,
        )
    )
    print(
        cycler.cycle_prompt(
            seed=0,
            append=prompt,
            trigger_words="",
            filename="testfile.txt",
            prompt_index=0,
        )
    )

    print("\n\nStyleCycler:\n")

    # --- StyleCycler tests ---
    style_cycler = StyleCycler()

    # Test specific style
    print(style_cycler.cycle_style(style="Plain", seed=0, switch_every=1))
    print(style_cycler.cycle_style(style="Plain", seed=0, switch_every=1, prompt="abcdgeheim", negative_prompt="defgnicht"))

    # Test random with seed for reproducibility
    r1 = style_cycler.cycle_style(style="random", seed=42, switch_every=1)
    r2 = style_cycler.cycle_style(style="random", seed=42, switch_every=1)
    print(r1)
    assert r1 == r2, "Same seed should produce same random style"

    # Test switch_every cycling
    style_cycler2 = StyleCycler()
    s1 = style_cycler2.cycle_style(style="random", seed=123, switch_every=3)
    s2 = style_cycler2.cycle_style(style="random", seed=123, switch_every=3)
    s3 = style_cycler2.cycle_style(style="random", seed=123, switch_every=3)
    s4 = style_cycler2.cycle_style(style="random", seed=123, switch_every=3)
    print(f"\nswitch_every=3: {s1[2]}, {s2[2]}, {s3[2]}, {s4[2]}")
    assert s1 == s2 == s3, "First 3 calls should return same style"
    # s4 may or may not differ depending on counter state

