from __future__ import annotations

import sys

from fenjue.modes.registry import activate_prompt_mode
from fenjue.modes.selection import choose_prompt_mode
from fenjue.runtime import batch

def main() -> None:
    selected_mode = choose_prompt_mode(sys.argv[1:])
    activate_prompt_mode(selected_mode, batch, args=sys.argv[1:])
    if selected_mode == "D":
        from fenjue.runtime import target_batch
        target_batch.main()
    else:
        batch.main()

if __name__ == "__main__":
    main()
