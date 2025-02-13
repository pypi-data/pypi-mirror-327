# dbnl-sdk

Python SDK development repo

## V0 SDK

V0 SDK are under `src`

To build SDK, run the following command in the root directory

```bash
python -m build
```

## Development

### Setup

We develop the SDK on the lowest supported Python version: 3.9. We use `pyenv` to manage Python version.

```bash
pyenv install 3.9.20
```

Setting up the virtual environment with `virtualenv`

```bash
PYENV_VERSION=3.9 pyenv exec python -m venv --prompt . venv
source venv/bin/activate
```

Install `dev` dependencies.

```bash
pip install -e '.[dev]'
```

If working on the eval package, install `eval` dependencies.

```bash
pip install -e '.[eval]'
```

Use `pre-commit` to enforce code quality standards before unformatted code makes it to CI.
Hooks can be installed to run before each commit with the following command:

```bash
pre-commit install --install-hooks
```

### Testing

To run all the unit tests in the repo:

```bash
make test
```

To manually run all `pre-commit` checks on all files in the repo:

```bash
pre-commit run --all-files
```

#### Integration Tests

This repo also supplies a suite of integration tests, though they are not currently comprehensive (please, make a PR to improve!).

To run the integration tests, you'll need to set the `DBNL_API_URL` and `DBNL_API_TOKEN` env vars. Unless you are testing something specific,
you can just use `https://api.dev.dbnl.com` and your own DBNL auth token (get one in DEV [here](https://app.dev.dbnl.com/tokens) if you need one).

```
DBNL_API_URL="https://api.dev.dbnl.com" DBNL_API_TOKEN=$AUTH_TOKEN make integration-tests
```

Note that this does technically have some side effects in DEV -- it will archive existing integration test projects in our
default namespace and create new ones with the same names (along with creating some runs and such within some of those projects).

### Documentation

We use [sphinx](https://www.sphinx-doc.org/en/master/) for generating documentation from docstrings. All of our
SDK methods should have corresponding docstrings.

Make sure your docs are readable and formatted properly! See [./docs/README.md](./docs/README.md) for instructions on building the documentation locally.

### Releasing the SDK

As the intention is to make this repository open-source in the future, deployment documentation is kept separately.
For convenience and clarity, you can find the instructions [here](https://docs.google.com/document/d/16oTO6OKmMqxUcQuzAyzVSU1VxclIeMqk1zkEy4XAhXA/edit?tab=t.0).
We should remove this before publicizing the repo.
