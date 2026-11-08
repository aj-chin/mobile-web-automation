
#!/usr/bin/env bash
set -euo pipefail

DISPLAY_NUMBER=99
DISPLAY_ID=":${DISPLAY_NUMBER}"
RECORDING_DIR="recordings"
VIDEO_FILE="${RECORDING_DIR}/twitch_test.mp4"

mkdir -p "$RECORDING_DIR"

XVFB_PID=""
FFMPEG_PID=""

cleanup() {
    if [[ -n "$FFMPEG_PID" ]]; then
        kill -INT "$FFMPEG_PID" 2>/dev/null || true
        wait "$FFMPEG_PID" 2>/dev/null || true
    fi

    if [[ -n "$XVFB_PID" ]]; then
        kill "$XVFB_PID" 2>/dev/null || trueclear
        
        wait "$XVFB_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT

echo "Starting virtual display..."
Xvfb "$DISPLAY_ID" -screen 0 1280x900x24 -ac &
XVFB_PID=$!

export DISPLAY="$DISPLAY_ID"
export RECORD_TEST=1

sleep 2

echo "Starting screen recording..."
ffmpeg \
    -y \
    -f x11grab \
    -framerate 15 \
    -video_size 1280x900 \
    -i "$DISPLAY_ID" \
    -c:v libx264 \
    -pix_fmt yuv420p \
    "$VIDEO_FILE" \
    > /tmp/twitch_ffmpeg.log 2>&1 &
FFMPEG_PID=$!

sleep 2

echo "Running Twitch automation..."
python -m pytest tests/twitch/test_twitch_search.py -v -s

echo "Test execution finished."
echo "Recording will be saved to: $VIDEO_FILE"
