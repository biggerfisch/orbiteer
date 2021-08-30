#!/bin/bash

poetry run coverage erase && poetry run coverage run && poetry run coverage report
