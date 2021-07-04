#!/bin/bash

# DS STORE
# Find and remove DS_Store files
find / -iname "*DS_Store*" -type f -exec rm -rf {} \; &>/dev/null
echo -e "---
DS_Store : OK" >> $PATHUSER/../logs/report