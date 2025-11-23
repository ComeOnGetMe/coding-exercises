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


ensure_just
ensure_uv
echo "✅ One-time setup complete."
echo "🚀 You can now run 'just setup' to create the virtual environment and install the dependencies."