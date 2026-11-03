.PHONY: setup check test lint typecheck package clean
setup:
	bash scripts/dev-setup.sh
check:
	bash scripts/verify-environment.sh
test:
	.venv/bin/python -m pytest
lint:
	.venv/bin/ruff check usr/lib/nls tests
typecheck:
	.venv/bin/mypy usr/lib/nls
package:
	.venv/bin/python -m build
clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache build dist *.egg-info
