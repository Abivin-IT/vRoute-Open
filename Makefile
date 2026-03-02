# ===========================================================
# vRoute Platform - Makefile
# Run `make` or `make help` to see all available targets.
#
# Workflows:
#   make proto          -> Sync & regenerate gRPC stubs
#   make build          -> Compile + Docker build (no tests)
#   make dev            -> Start platform, live logs (foreground)
#   make up             -> Start platform in background
#   make down           -> Stop platform
#   make logs           -> Tail service logs
#   make test           -> Run all tests (vKernel + vStrategy)
#   make test-kernel    -> Run only vKernel tests (JUnit 5)
#   make test-strategy  -> Run only vStrategy tests (pytest)
#   make clean          -> Delete build artifacts
#   make clean-docker   -> Wipe Docker volumes & layers
# ===========================================================

SHELL        := /bin/bash
.DEFAULT_GOAL := help

# -- Directories --------------------------------------------
ROOT          := $(CURDIR)
VKERNEL_DIR   := $(ROOT)/vkernel
VSTRATEGY_DIR := $(ROOT)/vstrategy
PROTO_SRC     := $(VKERNEL_DIR)/src/main/proto
PROTO_DST     := $(VSTRATEGY_DIR)/protos

# -- Docker Compose ----------------------------------------─
COMPOSE := docker-compose

# -- Cross-platform volume path helper (Cygwin / MSYS2 / Linux) --
docker_vol = $(shell command -v cygpath &>/dev/null && cygpath -w "$(1)" || echo "$(1)")

# -- Maven: prefer local -> wrapper -> Docker ----------------─
define mvn
	@{ \
	  cd $(VKERNEL_DIR); \
	  if command -v mvn &>/dev/null; then \
	    echo "  [mvn] local Maven"; \
	    mvn $(1) -T 1C -Dspring.main.banner-mode=off; \
	  elif [ -f ./mvnw ]; then \
	    echo "  [mvn] Maven Wrapper"; \
	    ./mvnw $(1) -T 1C -Dspring.main.banner-mode=off; \
	  else \
	    echo "  [mvn] Docker (cached ~/.m2)"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(VKERNEL_DIR)):/app" \
	      -v vroute-maven-cache:/root/.m2 \
	      -w /app \
	      maven:3.9-eclipse-temurin-21 mvn $(1) -T 1C; \
	  fi; \
	}
endef

# -- Python / pytest: prefer .venv -> local -> Docker -------
# Priority: project .venv (has all deps) > Docker fallback.
# System Python is skipped -- it may lack aiosqlite/asyncpg.
VENV_PY_WIN  := $(ROOT)/.venv/Scripts/python
VENV_PY_UNIX := $(ROOT)/.venv/bin/python3

define pytest
	@{ \
	  cd $(VSTRATEGY_DIR); \
	  if [ -f "$(VENV_PY_WIN)" ]; then \
	    echo "  [pytest] .venv (Windows)"; \
	    "$(VENV_PY_WIN)" -m pytest tests/ -v --tb=short -q; \
	  elif [ -f "$(VENV_PY_UNIX)" ]; then \
	    echo "  [pytest] .venv (Unix)"; \
	    "$(VENV_PY_UNIX)" -m pytest tests/ -v --tb=short -q; \
	  else \
	    echo "  [pytest] Docker (cached pip)"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(VSTRATEGY_DIR)):/app" \
	      -v vroute-pip-cache:/root/.cache/pip \
	      -w /app \
	      python:3.12-slim \
	      sh -c "pip install -q -r requirements.txt && \
	             python -m pytest tests/ -v --tb=short -q"; \
	  fi; \
	}
endef

# ===========================================================
# .PHONY - all targets are abstract (no output files)
# ===========================================================
.PHONY: help proto build dev up down logs ps \
        test test-kernel test-strategy \
        clean clean-docker

# ===========================================================
# help - auto-generated from ## comments
# ===========================================================
help: ## Show this help message
	@echo ""
	@echo "  vRoute Platform - Make targets"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	  | sort \
	  | awk 'BEGIN {FS = ":.*?## "}; \
	         {printf "  \033[36mmake %-16s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ===========================================================
# -- FLOW 1: gRPC / Protobuf codegen ----------------------
# Copies the canonical .proto from vkernel to vstrategy,
# then regenerates Python gRPC stubs (kernel_pb2.py etc.).
# ===========================================================
proto: ## Sync .proto files and regenerate gRPC stubs (Python)
	@echo ""
	@echo "==== [proto 1/2] Sync .proto -> vstrategy/protos/ ===="
	@cp -v $(PROTO_SRC)/*.proto $(PROTO_DST)/
	@echo ""
	@echo "==== [proto 2/2] Generate Python gRPC stubs ========═"
	@cd $(VSTRATEGY_DIR) && \
	if python3 -m grpc_tools.protoc --version &>/dev/null; then \
	  python3 -m grpc_tools.protoc \
	    -I protos \
	    --python_out=. \
	    --grpc_python_out=. \
	    protos/*.proto; \
	  echo "  OK Python stubs generated (local)"; \
	else \
	  echo "  [grpcio-tools] Docker fallback"; \
	  MSYS_NO_PATHCONV=1 docker run --rm \
	    -v "$(call docker_vol,$(VSTRATEGY_DIR)):/app" \
	    -w /app \
	    python:3.12-slim \
	    sh -c "pip install -q grpcio-tools && \
	           python -m grpc_tools.protoc -I protos \
	                  --python_out=. --grpc_python_out=. protos/*.proto"; \
	  echo "  OK Python stubs generated (docker)"; \
	fi

# ===========================================================
# -- FLOW 2: Build ----------------------------------------
# Full compile cycle: codegen -> Maven package -> Docker images.
# Tests are skipped intentionally; use `make test` separately.
# ===========================================================
build: proto ## Codegen + compile vKernel + build all Docker images
	@echo ""
	@echo "==== [build 1/2] Compile vKernel (skip tests) ====═══"
	$(call mvn,package -DskipTests)
	@echo ""
	@echo "==== [build 2/2] Build Docker images ================"
	$(COMPOSE) build
	@echo ""
	@echo "  OK Build complete - run 'make up' to start"

# ===========================================================
# -- FLOW 3: Dev mode (Docker Compose) --------------------
# ===========================================================
dev: ## Build + start all services with live logs (foreground, Ctrl-C to stop)
	@echo ""
	@echo "  Starting vRoute Platform (dev mode - press Ctrl-C to stop)"
	@echo ""
	$(COMPOSE) up --build

up: ## Build + start all services in the background (detached)
	@echo ""
	@echo "  Starting vRoute Platform (detached)…"
	$(COMPOSE) up --build -d
	@echo ""
	@sleep 3
	@echo "  ┌--------------------------------------------─┐"
	@echo "  │  vKernel       ->  http://localhost:8080     │"
	@echo "  │  vKernel API   ->  http://localhost:8080/api/v1/ │"
	@echo "  │  vStrategy     ->  http://localhost:8081     │"
	@echo "  │  PostgreSQL    ->  localhost:5432            │"
	@echo "  │  Redis         ->  localhost:6379            │"
	@echo "  └--------------------------------------------─┘"
	@echo ""
	@echo "  make logs  - tail logs     make down  - stop"

down: ## Stop and remove all running containers
	@echo "  Stopping vRoute Platform…"
	$(COMPOSE) down
	@echo "  OK All services stopped"

logs: ## Tail logs from all running services (Ctrl-C to exit)
	$(COMPOSE) logs -f --tail=50

ps: ## Show status of all running containers
	$(COMPOSE) ps

# ===========================================================
# -- FLOW 4: Tests ----------------------------------------
# Smart runner: local toolchain if available, Docker otherwise.
# Maven cache: Docker volume vroute-maven-cache
# Pip cache:   Docker volume vroute-pip-cache
# ===========================================================
test: test-kernel test-strategy ## Run ALL tests (vKernel + vStrategy)
	@echo ""
	@echo "  OK All tests passed"

test-kernel: ## Run vKernel tests only (JUnit 5 / Spring Boot / MockMvc)
	@echo ""
	@echo "==== Testing vKernel ================================"
	$(call mvn,test)
	@echo "  OK vKernel: PASSED"

test-strategy: ## Run vStrategy tests only (pytest)
	@echo ""
	@echo "==== Testing vStrategy ============================══"
	$(call pytest)
	@echo "  OK vStrategy: PASSED"

# ===========================================================
# -- FLOW 5: Clean ----------------------------------------
# ===========================================================
clean: ## Remove Maven target/, Python __pycache__ and generated *_pb2.py
	@echo "  Cleaning build artifacts…"
	$(call mvn,clean)
	@find $(VSTRATEGY_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(VSTRATEGY_DIR) -name "*.pyc"        -delete 2>/dev/null || true
	@find $(VSTRATEGY_DIR) -name "*_pb2*.py"    -delete 2>/dev/null || true
	@echo "  OK Build artifacts removed"

clean-docker: ## Remove containers, volumes (pgdata, caches) and dangling images
	@echo "  Cleaning Docker resources…"
	$(COMPOSE) down -v --remove-orphans
	docker volume rm vroute-maven-cache vroute-pip-cache 2>/dev/null || true
	docker image prune -f
	@echo "  OK Docker resources cleaned"
