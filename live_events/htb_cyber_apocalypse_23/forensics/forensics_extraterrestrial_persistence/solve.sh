#!/usr/bin/env bash
eval `cat persistence.sh | grep echo | cut -d '|' -f 1` | base64 -d | grep HTB | cut -d '=' -f 2
