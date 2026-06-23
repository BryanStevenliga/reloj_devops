# Variables
IMAGE_NAME = ghcr.io/bryanstevenliga/reloj_devops:latest
STACK_FILE = stack.yml
STACK_NAME = reloj_stack

# En Windows, si las variables están en el sistema, se invocan de esta manera en make
VPS_USER = $(USERNAME)
VPS_HOST = $(VPS_HOST)
VPS_SSH_PORT = $(VPS_SSH_PORT)

# Default target
.PHONY: all
all: help

# Help
.PHONY: help
help:
	@echo Available targets:
	@echo   build      Build Docker image locally
	@echo   push       Push image to GitHub Container Registry
	@echo   deploy     Deploy stack to VPS (updates stack without downtime)
	@echo   clean      Remove local Docker images

# Build Docker image en Windows
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Push image to GHCR desde Windows
.PHONY: push
push:
	echo %GHCR_PAT% | docker login ghcr.io -u %GITHUB_ACTOR% --password-stdin
	docker push $(IMAGE_NAME)

# Deploy desde Windows usando SSH
.PHONY: deploy
deploy:
	@echo Actualizando stack en el VPS desde Windows...
	sshpass -p "%VPS_PASSWORD%" ssh -p %VPS_SSH_PORT% %VPS_USER%@%VPS_HOST% "cd ~/landinga && echo \"%GHCR_PAT%\" | docker login ghcr.io -u %GITHUB_ACTOR% --password-stdin && docker pull $(IMAGE_NAME) && docker stack deploy -c $(STACK_FILE) --with-registry-auth $(STACK_NAME)"

# Clean local Docker images en Windows
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME) 2>nul || exit 0