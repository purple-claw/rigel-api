#!/bin/bash

echo "Downloading spaCy model: en_core_web_sm..."
python -m spacy download en_core_web_sm

# Copy the installed model into project folder
model_dir=$(python -c "import en_core_web_sm; print(en_core_web_sm.__path__[0])")
cp -r $model_dir ./en_core_web_sm
