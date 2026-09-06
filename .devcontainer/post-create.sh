#!/usr/bin/env bash
# Devcontainer create-time setup: install the project, then seed the
# oa-configurator stack config pointing at the compose `postgres` service.
set -euo pipefail

cd "$(dirname "$0")/.."

uv sync --frozen --extra dev --extra author --extra exploration --extra postgres --extra omop

bash "$(dirname "$0")/register-kernel.sh"

config_path="${OA_CONFIG_PATH:-${HOME}/.config/omop/config.toml}"
mkdir -p "$(dirname "${config_path}")"

if [ -e "${config_path}" ]; then
  echo "Keeping the existing stack config at ${config_path}"
else
  # Mode 600 because the file holds database passwords; oa-configurator warns
  # about anything more permissive. Copied rather than mounted so that
  # `omop-config configure hemonc_alchemy` can rewrite it in place, without
  # the edit landing back in the checked-in seed.
  install -m 600 .devcontainer/config.toml "${config_path}"
  echo "Installed the devcontainer stack config at ${config_path}"
fi
