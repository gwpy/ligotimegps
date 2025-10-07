# ligotimegps

ligotimegps is a Python library for converting to and from GPS time used in
gravitational-wave astrophysics.

The project exists to provide a lightweight, platform-independent implementation
of the `LIGOTimeGPS` object provided by the Python bindings of the LVK Analysis
Library (`lal`, part of `lalsuite`).

## Tech stack

-   **Programming Language**: Python 3.11+

-   **Platform support**: Linux, macOS, Windows

-   **Versioning**: `setuptools_scm`

-   **Packaging**: `pyproject.toml` installable with `pip`/`uv` with dependency groups

-   **Testing**: `pytest` (config in `pyproject.toml`)

-   **Linting/formatting**: `ruff` (config in `pyproject.toml`), plus `mypy` settings

-   **Documentation**: Sphinx sources under `docs/`

## Repository layout (high level)

-   `ligotimegps/` — main package.

-   `docs/` — user/developer documentation (Sphinx).

-   `tests` are located inside the project (e.g. `ligotimegps/tests/`).

-   The `worktrees/` directory may be present to hold multiple git worktrees -
    ignore it during repo-wide scans and analysis.

## Coding guidelines

-   **Style: follow PEP 8 with opinionated `ruff` rules in `pyproject.toml`.
    The project runs `ruff` in CI and locally via `python -m ruff .`.
    All features should uses the latest syntax supported by the minimum Python
    version.

-   **Type checking**: all code should include comprehensive type annotations following
    PEP 563, 585, 604, and 673.
    `mypy` is configured to check typing.
    Type annotations are not required for test functions and methods, but should be
    included in any helper functions, or fixtures, as appropriate.

-   **Documentation**: all public classes, methods, and functions should include
    docstrings following the NumPy/SciPy docstring standard.
    Use Sphinx-compatible reStructuredText markup.
    Docstrings should include type hints even if the function is already annotated.

-   **Tests**: use `pytest`. New code must include unit tests.
    Run tests locally via:

    ```shell
    uv pip install . --group dev
    uv run pytest .
    ```

    -   Keep tests small and focused; prefer `pytest.mark.parametrize` or separate tests
        over large tests with multiple independent assertions.
        Use mocking where appropriate to avoid slow or flaky tests.

## Commands & quick-start (recommended)

-   Preferred quick dev setup (isolated environment):

    Use `uv` to manage virtual environments (https://pypa.github.io/uv/).

    # create & activate venv
    uv venv --seed
    . .venv/bin/activate

    # install editable package with dev extras (per `CONTRIBUTING.md`)
    uv pip install . --group dev

-   Run tests (fast subset):

    python -m pytest . -q

-   Run ruff locally:

    python -m ruff .
