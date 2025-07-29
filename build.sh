#!/bin/bash
set -e

echo "Starting build process..."

# Upgrade pip, setuptools, and wheel first
echo "Upgrading build tools..."
python -m pip install --upgrade pip setuptools wheel

# Install dependencies with verbose output
echo "Installing dependencies..."
pip install -r requirements.txt --verbose

echo "Build completed successfully!" 