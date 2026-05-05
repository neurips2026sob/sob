#!/bin/bash
set -a
source ./.env
set +a

EXTRA='{"provider":{"only":["moonshotai"]},"reasoning":{"enabled":false}}'

.venv/bin/python -m sob.run --provider openrouter --modality text  --model-id moonshotai/kimi-k2.6 --openrouter-extra-body "$EXTRA" > logs/launch/kimi26_text.log  2>&1
.venv/bin/python -m sob.run --provider openrouter --modality image --model-id moonshotai/kimi-k2.6 --openrouter-extra-body "$EXTRA" > logs/launch/kimi26_image.log 2>&1
.venv/bin/python -m sob.run --provider openrouter --modality audio --model-id moonshotai/kimi-k2.6 --openrouter-extra-body "$EXTRA" > logs/launch/kimi26_audio.log 2>&1

echo "KIMI26_DONE $(date -Iseconds)" >> logs/launch/kimi26.done
