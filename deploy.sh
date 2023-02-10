#!/bin/bash

set -ex

./check.sh

kubectl apply -f service.yaml
kubectl apply -f podsa.yaml

docker buildx build . --platform=linux/arm64,linux/amd64 -t holdenk/cal-email-backend:0.1a --push

# If the cluster is running update it otherwise start it
# Note: this (in practice) does not work (for updating) currently.
(ray exec raycluster.yaml ls && ray rsync-up raycluster.yaml ./backend /apps/) ||
  (ray exec --start raycluster.yaml ls)
# Run the command
ray exec --screen raycluster.yaml  "cd /apps/; python ./backend/main.py"
