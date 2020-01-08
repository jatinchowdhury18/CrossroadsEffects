#!/bin/sh

for f in test_scripts/test_*.py
do
    echo "Running $f ..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        python3 $f
    else
        python $f
    fi
done
