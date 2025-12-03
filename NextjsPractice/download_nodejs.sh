#!/bin/bash

NODE_VERSION="v24.11.1"
BASE_URL="https://nodejs.org/dist/$NODE_VERSION"

OS=$(uname -s)
ARCH=$(uname -m)

if [[ "$OS" == "Linux" ]]; then
    NODE_TAR="node-$NODE_VERSION-linux-x64.tar.xz"
elif [[ "$OS" == "Darwin" ]]; then
    if [[ "$ARCH" == "arm64" ]]; then
        NODE_TAR="node-$NODE_VERSION-darwin-arm64.tar.gz"
    else
        NODE_TAR="node-$NODE_VERSION-darwin-x64.tar.gz"
    fi
else
    echo "Unsupported OS: $OS"
    exit 1
fi

NODE_URL="$BASE_URL/$NODE_TAR"

curl -# -C - -o $NODE_TAR $NODE_URL
mkdir -p .nodejs
tar -xvf $NODE_TAR -C .nodejs --strip-components 1
rm $NODE_TAR

