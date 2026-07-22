# AGENTS

## Prerequisites

Install the following first:

- Python 3.9
- `pipenv` (`pip install pipenv`)

Then install project dependencies:

- `pipenv install --dev`

## Build

Required installation before building:

- Follow all steps in **Prerequisites**

Build command:

- `pipenv run tox -e build`

## Test

Required installation before testing:

- Follow all steps in **Prerequisites**

Test command:

- `pipenv run tox`

## Lint

Required installation before linting:

- Follow all steps in **Prerequisites**

Lint command:

- `pipenv run flake8 src tests`
