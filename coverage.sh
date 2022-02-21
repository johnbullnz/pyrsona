#!/bin/bash

pytest -Werror --cov-report xml:./cov.xml --cov pyrsona -v -m "not slow" tests
rm .coverage*