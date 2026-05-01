#!/bin/bash

status=true

# ---------------------------------------------------

result=$(uv run python -O ./sorting_demo.py)
echo $result

# ---------------------------------------------------

$status
