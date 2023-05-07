#!/bin/sh

# Specify the name of the Systemd service
SERVICE_NAME="tgbot"
SERVICE_NAME2="server"

# Specify the path to the Git repository
REPO_PATH="/opt/p2p_orders_bot"

# Navigate to the Git repository
cd "$REPO_PATH"

# Start an infinite loop
while true; do
  # Fetch the latest changes from the remote repository
  git fetch

  # Check if there are any new changes
  if ! git diff --quiet HEAD origin/main; then
    # Pull the latest changes from the remote repository
    git pull

    # Restart the Systemd service
    systemctl restart "$SERVICE_NAME"
    systemctl restart "$SERVICE_NAME2"

    # Print a success message
    echo "Updated Git repository and restarted $SERVICE_NAME"
  fi

  # Wait for a few seconds before checking for new changes again
  sleep 10
done