# Run full test suite with clean output and durations
test:
	pytest --tb=short --durations=5 -q backend/tests

# Run tests and generate HTML report
test-html:
	pytest --html=report.html --self-contained-html backend/tests
