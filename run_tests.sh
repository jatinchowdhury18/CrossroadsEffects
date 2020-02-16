#!/bin/sh

PY=python
if [[ "$OSTYPE" == "darwin"* || $MACHTYPE == "x86_64-redhat-linux-gnu" ]]; then
    PY=python3
fi

pattern=test_scripts/*_test_*.py
if [[ $1 == "--quick" ]]; then
    pattern=test_scripts/q_test_*.py
elif [[ $1 == "--evolve" ]]; then
    pattern=test_scripts/e_test_*.py
elif [[ $1 == "--params" ]]; then
    pattern=test_scripts/p_test_*.py
fi

for f in $pattern
do
    echo "Running $f ..."
    $PY $f || exit 1
done
