#!/usr/bin/env bash

cat << EOF > .env
ENVIRONMENT=prod
TESTING=0
EMB_DIR="/code/NLP_resources/embeddings"
TRANSFORMERS_CACHE="/code/NLP_resources/huggingface"
HF_HOME="/code/NLP_resources/huggingface"
TORCH_HOME="/code/NLP_resources/torch"
EOF
