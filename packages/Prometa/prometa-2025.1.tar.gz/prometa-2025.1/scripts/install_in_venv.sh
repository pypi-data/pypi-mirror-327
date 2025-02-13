#!/usr/bin/env bash
set -euo pipefail

SELF=$(readlink -f "${BASH_SOURCE[@]}")
cd -- "${SELF%/*/*}"

if command -v uv
then
  echo "Using uv to create virtual environment."
  uv venv venv
  source venv/bin/activate
  pip_cmd=(uv pip)
else
  echo "Using venv and pip to create virtual environment."
  python3 -m venv venv
  source venv/bin/activate
  pip install -U pip
  pip_cmd=(pip)
fi

"${pip_cmd[@]}" install -U -e .
