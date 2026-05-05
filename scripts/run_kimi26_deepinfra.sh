#!/bin/bash
set -a
source ./.env
set +a

EXTRA='{"provider":{"only":["deepinfra"]},"reasoning":{"enabled":false}}'

.venv/bin/python -m sob.run --provider openrouter --modality text --model-id moonshotai/kimi-k2.6 --openrouter-extra-body "$EXTRA" > logs/launch/kimi26_deepinfra_text.log 2>&1

echo "KIMI26_DEEPINFRA_DONE $(date -Iseconds)" >> logs/launch/kimi26_deepinfra.done
