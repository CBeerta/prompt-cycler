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
    print(
        style_cycler.cycle_style(
            style="Plain",
            seed=0,
            switch_every=1,
            prompt="abcdgeheim",
            negative_prompt="defgnicht",
        )
    )

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

    # --- append_random tests ---
    print("\n\nappend_random:\n")

    # Test append_random with a specific style
    sc = StyleCycler()
    a = sc.cycle_style(style="Plain", seed=42, switch_every=1)
    b = sc.cycle_style(style="Plain", seed=42, switch_every=1, append_random=True)
    print(f"without append_random: {a}")
    print(f"with append_random:    {b}")
    # append_random should produce a longer prompt with "+" in style_name
    assert ", " in b[2], "append_random should join two style names"
    assert b[0] != a[0], "append_random should produce a different prompt"

    # Test dedup: same token should not appear twice
    assert len(b[0].split(", ")) == len(
        set(b[0].split(", "))
    ), "append_random should dedupe prompt tokens"

    # Test append_random with style="random" produces two random styles
    sc2 = StyleCycler()
    c = sc2.cycle_style(style="random", seed=99, switch_every=1)
    d = sc2.cycle_style(style="random", seed=99, switch_every=1, append_random=True)
    print(f"random without append_random: {c}")
    print(f"random with append_random:    {d}")
    assert ", " in d[2], "append_random with random style should join two random styles"
    assert len(d[0]) > len(c[0]), "append_random should produce a longer prompt"
    assert len(d[0].split(", ")) == len(
        set(d[0].split(", "))
    ), "append_random should dedupe prompt tokens"

    # --- append_random with switch_every ---
    print("\n\nappend_random + switch_every:\n")

    # Fixed style: appended should persist for switch_every calls
    sc3 = StyleCycler()
    results = []
    for i in range(6):
        r = sc3.cycle_style(style="Plain", seed=42, switch_every=3, append_random=True)
        results.append(r)
        print(f"  call {i+1}: {r[2]}")

    # Calls 0-2 should have same style_name, calls 3-5 may or may not
    # (They should differ because the 4th call at counter>=3 advances)
    assert results[0][2] == results[1][2] == results[2][2], (
        f"First 3 calls (switch_every=3, fixed style) should have same "
        f"style_name: {results[0][2]}, {results[1][2]}, {results[2][2]}"
    )
    # The appended style should change after switch_every
    assert results[2][2] != results[3][2], (
        f"4th call should have a different appended style: "
        f"{results[2][2]} vs {results[3][2]}"
    )
    # And then persist again
    assert results[3][2] == results[4][2] == results[5][2], (
        f"Calls 4-6 (switch_every=3, fixed style) should have same "
        f"style_name: {results[3][2]}, {results[4][2]}, {results[5][2]}"
    )

    # Random style: both main and appended should persist for switch_every
    sc4 = StyleCycler()
    results2 = []
    for i in range(6):
        r = sc4.cycle_style(style="random", seed=77, switch_every=3, append_random=True)
        results2.append(r)
        print(f"  call {i+1}: {r[2]}")

    assert results2[0][2] == results2[1][2] == results2[2][2], (
        f"First 3 calls (switch_every=3, random style) should have same "
        f"style_name: {results2[0][2]}, {results2[1][2]}, {results2[2][2]}"
    )
    assert results2[2][2] != results2[3][2], (
        f"4th call should have a different style pair: "
        f"{results2[2][2]} vs {results2[3][2]}"
    )
    assert results2[3][2] == results2[4][2] == results2[5][2], (
        f"Calls 4-6 (switch_every=3, random style) should have same "
        f"style_name: {results2[3][2]}, {results2[4][2]}, {results2[5][2]}"
    )

    # The two names in the pair should be different (main != appended)
    names = results2[0][2].split(", ")
    assert len(names) == 2, f"Should have two style names: {names}"
    assert (
        names[0] != names[1]
    ), f"Main and appended styles should be different: {names}"

    print("\n\nAll tests passed!")
