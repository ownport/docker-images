#!/bin/bash

echo "[INFO] Publishing package"
python3 setup.py sdist bdist_wheel
twine upload -r internal dist/*
