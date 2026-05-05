#!/bin/bash
set -a
source ./.env
set +a

EXTRA='{"provider":{"only":["z-ai"]},"reasoning":{"enabled":false}}'

.venv/bin/python -m sob.run --provider openrouter --modality text  --model-id z-ai/glm-5.1 --openrouter-extra-body "$EXTRA" > logs/launch/glm51_text.log  2>&1
.venv/bin/python -m sob.run --provider openrouter --modality image --model-id z-ai/glm-5.1 --openrouter-extra-body "$EXTRA" > logs/launch/glm51_image.log 2>&1
.venv/bin/python -m sob.run --provider openrouter --modality audio --model-id z-ai/glm-5.1 --openrouter-extra-body "$EXTRA" > logs/launch/glm51_audio.log 2>&1

echo "GLM51_DONE $(date -Iseconds)" >> logs/launch/glm51.done
