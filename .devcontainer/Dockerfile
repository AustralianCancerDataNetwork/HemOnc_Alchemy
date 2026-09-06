FROM python:3.12-slim-bookworm

# Copy uv from the official image while keeping the application image Python slim.
COPY --from=ghcr.io/astral-sh/uv:0.8.17 /uv /uvx /bin/

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:/home/${USERNAME}/.local/bin:${PATH}"

RUN groupadd --gid "${USER_GID}" "${USERNAME}" \
    && useradd --uid "${USER_UID}" --gid "${USER_GID}" -m -s /bin/bash "${USERNAME}"

WORKDIR /workspace/hemonc-alchemy

# The source is mounted by Compose. The project and its extras are installed by
# the Compose command/post-create hook when the mounted Git checkout is
# available to hatch-vcs; installing here would omit the mounted source tree.
RUN apt-get update \
    && apt-get install --yes --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir --parents /opt/venv \
    && chown -R "${USERNAME}:${USERNAME}" /opt/venv

USER ${USERNAME}
