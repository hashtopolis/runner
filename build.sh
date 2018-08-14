#!/usr/bin/env bash

rm runner.zip
zip -r runner.zip __main__.py htpserver -x "*__pycache__*"
