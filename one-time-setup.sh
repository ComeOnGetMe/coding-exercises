#!/bin/bash
# install just depending on the OS
ensure_just() {
    if command -v just >/dev/null 2>&1; then
        echo "✅ just is already installed."
    else
        echo "🔄 Installing just..."
        install_just
    fi
}

install_just() {
    if [ "$(uname)" == "Darwin" ]; then
        brew install just
    elif [ "$(uname)" == "Linux" ]; then
        curl -fsSL https://just.systems/install.sh | bash -s -- --to ~/.local/bin
    fi
}

ensure_uv() {
    if command -v uv >/dev/null 2>&1; then
        echo "✅ uv is already installed."
    else
        echo "🔄 Installing uv..."
        curl -fsSL https://astral.sh/uv/install.sh | bash
    fi
}

ensure_docker() {
    if command -v docker >/dev/null 2>&1; then
        echo "✅ docker is already installed."
    else
        echo "🔄 Installing docker..."
        install_docker
    fi
}

install_docker() {
    if [ "$(uname)" == "Darwin" ]; then
        brew install docker
    elif [ "$(uname)" == "Linux" ]; then
        # Install Docker using the official convenience script
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        rm get-docker.sh
        # Add current user to docker group (requires logout/login to take effect)
        sudo usermod -aG docker $USER
        echo "⚠️  Note: You may need to log out and back in for Docker group changes to take effect."
    fi
}

ensure_docker_compose() {
    if command -v docker-compose >/dev/null 2>&1 || docker compose version >/dev/null 2>&1; then
        echo "✅ docker-compose is already installed."
    else
        echo "🔄 Installing docker-compose..."
        install_docker_compose
    fi
}

install_docker_compose() {
    if [ "$(uname)" == "Darwin" ]; then
        brew install docker-compose
    elif [ "$(uname)" == "Linux" ]; then
        # Docker Compose v2 comes with Docker, but install standalone v1 for compatibility
        sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
}

ensure_just
ensure_uv
ensure_docker
ensure_docker_compose
echo "✅ One-time setup complete."
echo "🚀 You can now run 'just setup' to create the virtual environment and install the dependencies."