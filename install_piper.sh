#!/bin/bash
# Automated workaround for piper-tts and piper-phonemize install
# TODO: Fix for windows

# Clone project
git clone git@github.com:rhasspy/piper-phonemize.git piper-phonemize
cd piper-phonemize
# Checkout (tag: 2023.11.14-4, Date:   Tue Nov 14 11:54:34 2023 -0600)
git checkout fccd4f335aa68ac0b72600822f34d84363daa2bf -b temp
# Build piper-phonemize
make clean; make

# Link piper-phonemize dependencies to avoid dyld[82606]: Library not loaded: @rpath/libpiper_phonemize.1.dylib
# TODO: Get OS version to use cd for Windows instead of pwd
export DYLD_LIBRARY_PATH=`pwd`/install/lib/

# Test command for lib linking
# echo "testing one two three" | ./install/bin/piper_phonemize -l en-us --espeak-data ./install/share/espeak-ng-data/

# Create ven in root of project
python3 -m venv ../venv
# Activate virtual env and update pip
source ../venv/bin/activate; pip install -U pip

# Tweak C++ headers to update __version__ for piper-phonemize
patch -p1 <<EOF
--- a/setup.py
+++ b/setup.py
@@ -9 +9 @@ _DIR = Path(__file__).parent
-_ESPEAK_DIR = _DIR / "espeak-ng" / "build"
+_ESPEAK_DIR = _DIR / "install"
@@ -13 +13 @@ _ONNXRUNTIME_DIR = _LIB_DIR / "onnxruntime"
-__version__ = "1.2.0"
+__version__ = "1.1.0"
EOF

# Install temp local version of piper-phonemize to virtual environment
pip install .
# Copy espeak-ng-data from build to virtual env
# TODO: Fix determining correct python major.minor
cp -rp ./install/share/espeak-ng-data ../venv/lib/python3.11/site-packages/piper_phonemize/espeak-ng-data

pip install piper-tts

# Example of testing piper-tts & play file!
# echo 'Welcome to the world of speech synthesis!' | piper --model en_US-lessac-medium --output_file welcome.wav
# afplay welcome.wav