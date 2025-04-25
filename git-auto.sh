#!/bin/bash
msg=${1:-"Update code"}
git add .
git commit -m "$msg"
git push
