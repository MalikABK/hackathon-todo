"""Entry point for the Todo App CLI."""

import sys
from pathlib import Path

# Allow running as `python src/main.py` (not just `python -m src.main`)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models import TaskList
from src.cli import dispatch_command


def main() -> None:
    """Create a TaskList, parse arguments, dispatch command, exit."""
    task_list = TaskList()
    exit_code = dispatch_command(sys.argv[1:], task_list)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
