#!/bin/sh

for f in test_scripts/test_*.py
do
    echo "Running $f ..."
    python $f
done
