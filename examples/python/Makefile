IMAGE_TAG ?= battlebot-python
HISTORY ?= RP2;SS1;SS2;

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: image
image:  ## Build the docker image
	docker build -t $(IMAGE_TAG) .

.PHONY: run
run: image  ## Run the image without any history
	docker run --network=none $(IMAGE_TAG)

.PHONY: run-with-history
run-with-history: image  ## Run the image with a provided history
	docker run -e PLAYER_NUMBER=1 --network=none $(IMAGE_TAG) "$(HISTORY)"

.PHONY: push 
push: image  ## pushthe docker image
	docker push $(IMAGE_TAG)
