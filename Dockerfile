# Slim base image — smaller attack surface and faster pulls than the full python image
FROM python:3.11-slim

WORKDIR /app

# Dependencies copied and installed BEFORE the app code.
# Docker caches layers — if only app.py changes, this layer is reused
# instead of reinstalling every dependency on every build.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code copied last, since it changes most often
COPY app.py .

# Run as a non-root user — never run application containers as root
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]