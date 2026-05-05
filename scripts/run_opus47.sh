#!/bin/bash
set -a
source ./.env
set +a

.venv/bin/python -m sob.run --provider anthropic --modality text  --model-id claude-opus-4-7 > logs/launch/opus47_text.log  2>&1
.venv/bin/python -m sob.run --provider anthropic --modality image --model-id claude-opus-4-7 > logs/launch/opus47_image.log 2>&1
.venv/bin/python -m sob.run --provider anthropic --modality audio --model-id claude-opus-4-7 > logs/launch/opus47_audio.log 2>&1

echo "OPUS47_DONE $(date -Iseconds)" >> logs/launch/opus47.done
