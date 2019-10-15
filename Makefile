
DEFAULT: vet

.PHONY: vet
vet:
	@echo "validate python code"
	@pylint chess
