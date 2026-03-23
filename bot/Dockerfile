# Bot Dockerfile - uses uv for dependency management
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy pyproject.toml and uv.lock for dependency installation
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy bot source code
COPY bot.py ./
COPY handlers/ ./handlers/
COPY services/ ./services/
COPY config.py ./
COPY utils.py ./

# Run the bot
CMD ["uv", "run", "bot.py"]
