#!/bin/bash
# Step 1: Pull the latest changes from the repository
echo "Pulling the latest changes from the repository..."
git pull

# Step 2: Install dependencies
echo "Installing dependencies..."
npm ci

# Step 3: Build the Vue application
echo "Building the app..."
npm run build

# Step 4: Copy the build files to the deployment directory
TARGET_DIR="/var/www/pimoo-1rz.fab.hs-rm.de/html/"
echo "Copying files to $TARGET_DIR"
sudo cp -rf dist/* "$TARGET_DIR"

echo "Deployment complete!"