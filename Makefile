
DEFAULT: vet

.PHONY: vet
vet:
	@echo "analysis python code"
	@pylint chess
