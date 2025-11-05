###########################################################
# Builder stage. Build dependencies.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

WORKDIR /app
COPY ./pyproject.toml ./uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev


###########################################################
# Production stage. Copy only runtime deps that were installed in the Builder stage.
FROM python:3.13-slim-bookworm AS production

ENV PYTHONUNBUFFERED=1

# Copy the applicant from the builder
COPY --from=builder /app /app

# Create user with the name uv
RUN groupadd -g 1500 uv && \
    useradd -m -u 1500 -g uv uv

USER uv
WORKDIR /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=uv:uv . /app

CMD [ "python3", "-m" , "src.bot" ]
