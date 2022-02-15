#!/bin/sh

MARKER_PREFIX="##"
VERSION=$(echo "$1" | sed 's/^v//g')

IFS=''
found=0

while read -r "line"; do
  # If not found and matching heading
  if [ $found -eq 0 ] && echo "$line" | grep -q "$MARKER_PREFIX \[$VERSION\]"; then
    echo "$line"
    found=1
    continue
  fi

  # If needed version if found, and reaching next delimter - stop
  if [ $found -eq 1 ] && echo "$line" | grep -q -E "$MARKER_PREFIX \[[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+\]"; then
    found=0
    break
  fi

  # Keep printing out lines as no other version delimiter found
  if [ $found -eq 1 ]; then
    echo "$line"
  fi
done < CHANGELOG.md