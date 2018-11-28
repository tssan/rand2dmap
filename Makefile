
ENV_PATH?=.env
SRC_FULL_PATH?=$(shell pwd)/src
TMP_MAPS_PATH?=.maps


.PHONY: env-setup
env-setup:
	@virtualenv -q -p python3 $(ENV_PATH);
	@mkdir -p $(TMP_MAPS_PATH)


.PHONY: clean-py
clean-py:
	@find . -name "*.pyc" -exec rm -rf {} \; -prune -print
	@find . -name "__pycache__" -exec rm -rf {} \; -prune -print


.PHONY: clean
clean:
	@rm -rf $(ENV_PATH)
	@rm -rf $(TMP_MAPS_PATH)
	@$(MAKE) clean-py


.PHONY: run
run:
	@. $(ENV_PATH)/bin/activate && PYTHONPATH=$(SRC_FULL_PATH) python src/rand2dmap/generator.py
