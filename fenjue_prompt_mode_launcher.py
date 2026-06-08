import sys

import chatgpt_batch_pyautogui as batch


def choose_prompt_mode() -> str:
    for argument in sys.argv[1:]:
        normalized = argument.strip().upper()
        if normalized in {"A", "--MODE=A", "--PROMPT-MODE=A"}:
            return "A"
        if normalized in {"B", "--MODE=B", "--PROMPT-MODE=B"}:
            return "B"

    while True:
        print("")
        print("Choose prompt mode:")
        print("  A = original stable compact style")
        print("  B = photographer four-block style")
        choice = input("Prompt mode [A/B, default A]: ").strip().upper() or "A"
        if choice in {"A", "B"}:
            return choice
        print("Please enter A or B.")


def activate_prompt_mode(mode: str) -> None:
    if mode == "A":
        print("Prompt mode A active: original stable compact style.", flush=True)
        return

    import photographer_prompt_templates as photographer

    batch.prompt_for_art_direction = photographer.prompt_for_art_direction
    batch.prompt_template_name = photographer.prompt_template_name
    print("Prompt mode B active: photographer four-block style.", flush=True)


if __name__ == "__main__":
    activate_prompt_mode(choose_prompt_mode())
    batch.main()
