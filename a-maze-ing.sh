#!/bin/bash
cd "$(dirname "$0")" || exit 1

make run
read -r -p "Presiona Enter para ejecutar make clear..."
make clean
