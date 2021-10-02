#!/bin/sh

PYTHONPATH=$(dirname $0)/tools/ python3 -m build $@
