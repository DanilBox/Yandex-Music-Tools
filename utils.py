import os
import sys
from typing import Any, TextIO


class HiddenPrints:
    def __enter__(self) -> None:
        self._original_stdout: TextIO = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, *args: Any) -> None:
        sys.stdout.close()
        sys.stdout = self._original_stdout


hidden_prints = HiddenPrints
