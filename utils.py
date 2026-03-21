import os
import sys
from pathlib import Path
from typing import Any, TextIO


class HiddenPrints:
    devnull = Path(os.devnull)

    def __enter__(self) -> None:
        self._original_stdout: TextIO = sys.stdout
        sys.stdout = self.devnull.open("w")

    def __exit__(self, *args: Any) -> None:
        sys.stdout.close()
        sys.stdout = self._original_stdout


hidden_prints = HiddenPrints
