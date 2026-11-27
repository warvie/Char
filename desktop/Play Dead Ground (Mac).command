#!/bin/bash
# Dead Ground desktop launcher (Mac): Chrome in its own window, frame-rate cap off
DIR="$(cd "$(dirname "$0")" && pwd)"
open -n -a "Google Chrome" --args --user-data-dir="$HOME/Library/Application Support/DeadGroundBrowser" --disable-gpu-vsync --disable-frame-rate-limit --disable-background-timer-throttling --app="file://$DIR/index.html" \
  || open "file://$DIR/index.html"
