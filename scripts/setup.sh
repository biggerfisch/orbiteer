#!/bin/bash

if [[ -z "$(command -v poetry)" ]]; then
    echo "Failed to find Poetry"
    exit 1
fi

poetry install --remove-untracked
