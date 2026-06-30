install:
	pip install -e ".[dev]"

install-agentscope:
	pip install -e ".[dev,agentscope]"

run:
	uvicorn main:app --reload

verify:
	python -m verification.run_verification

test:
	pytest -q
