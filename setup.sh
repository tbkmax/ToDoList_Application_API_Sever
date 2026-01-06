#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

echo "==> Running setup for ToDoList_Application in $ROOT_DIR"

# Create a default .env file if one does not already exist
ENV_FILE="$ROOT_DIR/.env"
if [ ! -f "$ENV_FILE" ]; then
  echo "No .env found — creating default $ENV_FILE"
  cat > "$ENV_FILE" <<'EOF'
POSTGRES_USER=todo_user
POSTGRES_PASSWORD=supersecret
POSTGRES_DB=todo_db
EOF
  echo "Created $ENV_FILE with default credentials. Review/update before use."
else
  echo ".env already exists at $ENV_FILE — leaving it unchanged."
fi

has_cmd() { command -v "$1" >/dev/null 2>&1; }

install_docker_via_getscript() {
  echo "Docker not found — attempting automated install via get.docker.com (requires sudo)."
  curl -fsSL https://get.docker.com | sudo sh
}

if has_cmd docker; then
  echo "Docker is already installed: $(docker --version)"
else
  install_docker_via_getscript
  if has_cmd docker; then
    echo "Docker installed successfully: $(docker --version)"
  else
    echo "ERROR: Docker installation failed. Please install Docker manually:" >&2
    echo "  https://docs.docker.com/get-docker/" >&2
    exit 1
  fi
fi

# Ensure Docker service is running
if systemctl >/dev/null 2>&1; then
  echo "Ensuring docker service is enabled and running (may prompt for sudo)..."
  sudo systemctl enable --now docker || true
fi

# Check for docker compose availability (either plugin or legacy binary)
if docker compose version >/dev/null 2>&1; then
  echo "docker compose plugin available: $(docker compose version 2>/dev/null | head -n1 || true)"
elif has_cmd docker-compose; then
  echo "docker-compose binary available: $(docker-compose --version)"
else
  echo "docker compose not found — attempting to install compose plugin/binary."
  # Try to install docker compose plugin via package manager script (get.docker.com usually installs it)
  if has_cmd apt-get; then
    sudo apt-get update
    sudo apt-get install -y docker-compose-plugin || true
  fi
  if ! docker compose version >/dev/null 2>&1 && ! has_cmd docker-compose; then
    echo "Could not install docker compose automatically. You can install it from:" >&2
    echo "  https://docs.docker.com/compose/install/" >&2
    echo "Proceeding may fail if compose is required." >&2
  fi
fi

echo "Bringing up project with: sudo docker compose up -d --build"
sudo docker compose up -d --build

echo "Done. Use 'sudo docker compose ps' to inspect running containers." 
