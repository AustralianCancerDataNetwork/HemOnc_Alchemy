#!/usr/bin/env bash
# Register the project environment as the `python3` Jupyter kernel.
#
# The VS Code Jupyter extension supplies its own kernel when it attaches, but
# `jupyter execute`, nbclient and papermill all resolve `python3` from the
# kernel spec directory. Without this, running the notebooks from the CLI
# fails with NoSuchKernel even though every dependency is installed.
#
# Run from postStartCommand, not just postCreateCommand: a container created
# before this script existed would otherwise never get the kernel.
# `ipykernel install` is idempotent, so re-running on every start is safe.
set -euo pipefail

if ! python -c "import ipykernel" 2>/dev/null; then
  echo "ipykernel not installed; skipping kernel registration (needs the exploration extra)"
  exit 0
fi

python -m ipykernel install --user --name python3 --display-name "hemonc-alchemy" >/dev/null
echo "Registered the python3 Jupyter kernel"
