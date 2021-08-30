#!/bin/bash

EXIT_CODE=0

# Lets us run all the commands and see all the issues but still error out if at least one fails
if ! poetry run black --check . ; then
    ((EXIT_CODE++))
fi
if ! poetry run isort --check . ; then
    ((EXIT_CODE++))
fi
if ! poetry run flake8 . ; then
    ((EXIT_CODE++))
fi
if ! poetry run mypy . ; then
    ((EXIT_CODE++))
fi

exit $EXIT_CODE
