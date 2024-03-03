#!/bin/bash
# run in root of git repo


# Define directories to ensure they exist
directories=("llms" "voices")

# Create directories if they don't exist
for dir in "${directories[@]}"; do
  if [[ ! -d "$dir" ]]; then
    echo "Creating directory: $dir"
    mkdir "$dir"
  fi
done

echo "Directories ready for downloads."

# Initialize and update git submodules
echo "Initializing git submodules..."
git submodule init
git submodule update
echo "Pulled submodules, building..."

# Prompt the user
echo "Do you want to download default models? (y/n)"
read answer

# Check the answer
if [[ $answer = y* ]] || [[ $answer = Y* ]]; then
  echo "Downloading default models..."
  ./defaultModels.sh
else
  echo "Skipping download of default models."
fi


# Run build script
./build.sh

# Setup Python virtual environment and install dependencies
echo "Setting up Python virtual environment..."
python3 -m venv venv
source ./venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
cd piper/src/python_run || exit
pip install -r requirements.txt
pip install -r requirements_http.txt



echo "Setup complete."
