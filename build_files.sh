#!/bin/bash
# Static build is handled by WhiteNoise at runtime — no collectstatic needed.

set -e

pip install -r requirements.txt
python3 -m pip install --upgrade pip --break-system-packages
python3 -m pip install -r requirements.txt --break-system-packages
python3 manage.py collectstatic --noinput
echo "Build complete."