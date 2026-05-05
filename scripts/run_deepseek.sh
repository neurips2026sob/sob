#!/bin/bash
set -a
source ./.env
set +a

EXTRA='{"provider":{"only":["novita"]},"reasoning":{"enabled":false}}'

.venv/bin/python -m sob.run --provider openrouter --modality text  --model-id deepseek/deepseek-v4-pro --openrouter-extra-body "$EXTRA" > logs/launch/deepseek_text.log  2>&1
.venv/bin/python -m sob.run --provider openrouter --modality image --model-id deepseek/deepseek-v4-pro --openrouter-extra-body "$EXTRA" > logs/launch/deepseek_image.log 2>&1
.venv/bin/python -m sob.run --provider openrouter --modality audio --model-id deepseek/deepseek-v4-pro --openrouter-extra-body "$EXTRA" > logs/launch/deepseek_audio.log 2>&1

echo "DEEPSEEK_DONE $(date -Iseconds)" >> logs/launch/deepseek.done