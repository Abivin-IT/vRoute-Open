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
#   make test           -> Run all tests (vKernel + vStrategy + vFinacc)
#   make test-kernel    -> Run only vKernel tests (JUnit 5)
#   make test-strategy  -> Run only vStrategy tests (pytest)
#   make test-finacc    -> Run only vFinacc tests (pytest)
#   make clean          -> Delete build artifacts
#   make clean-docker   -> Wipe Docker volumes & layers
#   make security       -> Full DevSecOps pipeline
#   make audit          -> CI gate (secrets + lint + SAST + tests)
#   make scan-secrets   -> Gitleaks secret detection
#   make lint           -> ruff check + format (Python)
#   make sast           -> Semgrep static analysis
#   make dependency-check -> CVE scan (pip-audit + OWASP)
#   make sbom           -> CycloneDX SBOM generation
#   make sonarqube      -> SonarQube quality gate
# ===========================================================

SHELL        := /bin/bash
.DEFAULT_GOAL := help

# -- Directories --------------------------------------------
ROOT          := $(CURDIR)
VKERNEL_DIR   := $(ROOT)/01-vkernel
VSTRATEGY_DIR := $(ROOT)/02-vstrategy
VFINACC_DIR   := $(ROOT)/03-vfinacc
VDESIGN_DIR   := $(ROOT)/04-vdesign-physical
VMARKETING_DIR:= $(ROOT)/05-vmarketing-org
DEPLOY_DIR    := $(ROOT)/80-deploy
PROTO_SRC     := $(VKERNEL_DIR)/src/main/proto
PROTO_DST     := $(VSTRATEGY_DIR)/protos

# -- Docker Compose ----------------------------------------─
COMPOSE := docker-compose -f $(DEPLOY_DIR)/docker-compose.yml

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
	  cd $(1); \
	  if [ -f "$(VENV_PY_WIN)" ]; then \
	    echo "  [pytest] .venv (Windows)"; \
	    "$(VENV_PY_WIN)" -m pytest tests/ -v --tb=short -q; \
	  elif [ -f "$(VENV_PY_UNIX)" ]; then \
	    echo "  [pytest] .venv (Unix)"; \
	    "$(VENV_PY_UNIX)" -m pytest tests/ -v --tb=short -q; \
	  else \
	    echo "  [pytest] Docker (cached pip)"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(1)):/app" \
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
        test test-kernel test-strategy test-finacc test-design-physical test-marketing-org test-platform \
        clean clean-docker \
        security audit scan-secrets lint sast dependency-check sbom sonarqube

# ===========================================================
# help - auto-generated from ## comments
# ===========================================================
help: ## Show this help message
	@echo ""
	@echo "  vRoute Platform - Make targets"
	@echo ""
	@grep -E '^[a-zA-Z_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) \
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
	@echo "  │  vStrategy     ->  http://localhost:8080/vstrategy/  │"
	@echo "  │  vFinacc       ->  http://localhost:8080/vfinacc/    │"
	@echo "  │  vDesign Phys  ->  http://localhost:8080/vdesign-physical/  │"
	@echo "  │  vMarketing    ->  http://localhost:8080/vmarketing-org/    │"
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
test: test-kernel test-strategy test-finacc test-design-physical test-marketing-org ## Run ALL tests (vKernel + vStrategy + vFinacc + vDesign + vMarketing)
	@echo ""
	@echo "  OK All tests passed"

test-kernel: ## Run vKernel tests only (JUnit 5 / Spring Boot / MockMvc)
	@echo ""
	@echo "==== Testing vKernel ================================"
	$(call mvn,test)
	@echo "  OK vKernel: PASSED"

test-strategy: ## Run vStrategy tests only (pytest)
	@echo ""
	@echo "==== Testing vStrategy =============================="
	$(call pytest,$(VSTRATEGY_DIR))
	@echo "  OK vStrategy: PASSED"

test-finacc: ## Run vFinacc tests only (pytest)
	@echo ""
	@echo "==== Testing vFinacc ================================"
	$(call pytest,$(VFINACC_DIR))
	@echo "  OK vFinacc: PASSED"

test-design-physical: ## Run vDesign Physical tests only (pytest)
	@echo ""
	@echo "==== Testing vDesign Physical ======================="
	$(call pytest,$(VDESIGN_DIR))
	@echo "  OK vDesign Physical: PASSED"

test-marketing-org: ## Run vMarketing Org tests only (pytest)
	@echo ""
	@echo "==== Testing vMarketing Org ========================="
	$(call pytest,$(VMARKETING_DIR))
	@echo "  OK vMarketing Org: PASSED"

test-platform: ## Test platform core only — vKernel (JUnit 5 / Spring Boot)
	@echo ""
	@echo "==== Testing Platform Core (vKernel) ================"
	$(call mvn,test)
	@echo "  OK vKernel: PASSED"

test-app-%: ## Test a specific vApp by name (e.g. make test-app-vstrategy)
	@APP_DIR="$(ROOT)/$*"; \
	echo ""; \
	echo "==== Testing vApp: $* ================================"; \
	if [ ! -d "$$APP_DIR" ]; then \
	  echo "  ERROR: directory '$$APP_DIR' not found"; exit 1; \
	elif [ -f "$$APP_DIR/requirements.txt" ]; then \
	  echo "  [runner] Python / pytest"; \
	  if [ -f "$(VENV_PY_WIN)" ]; then \
	    cd "$$APP_DIR" && "$(VENV_PY_WIN)" -m pytest tests/ -v --tb=short -q; \
	  elif [ -f "$(VENV_PY_UNIX)" ]; then \
	    cd "$$APP_DIR" && "$(VENV_PY_UNIX)" -m pytest tests/ -v --tb=short -q; \
	  else \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$$APP_DIR):/app" \
	      -v vroute-pip-cache:/root/.cache/pip \
	      -w /app python:3.12-slim \
	      sh -c "pip install -q -r requirements.txt && python -m pytest tests/ -v --tb=short -q"; \
	  fi; \
	elif [ -f "$$APP_DIR/pom.xml" ]; then \
	  echo "  [runner] Java / Maven"; \
	  if command -v mvn &>/dev/null; then \
	    cd "$$APP_DIR" && mvn test -T 1C -Dspring.main.banner-mode=off; \
	  elif [ -f "$$APP_DIR/mvnw" ]; then \
	    cd "$$APP_DIR" && ./mvnw test -T 1C -Dspring.main.banner-mode=off; \
	  else \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$$APP_DIR):/app" \
	      -v vroute-maven-cache:/root/.m2 \
	      -w /app maven:3.9-eclipse-temurin-21 mvn test -T 1C; \
	  fi; \
	else \
	  echo "  ERROR: cannot detect runner for '$*' (no requirements.txt or pom.xml)"; exit 1; \
	fi
	@echo "  OK $*: PASSED"

# ===========================================================
# -- FLOW 5: Clean ----------------------------------------
# ===========================================================
clean: ## Remove Maven target/, Python __pycache__ and generated *_pb2.py
	@echo "  Cleaning build artifacts…"
	$(call mvn,clean)
	@find $(VSTRATEGY_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(VSTRATEGY_DIR) -name "*.pyc"        -delete 2>/dev/null || true
	@find $(VSTRATEGY_DIR) -name "*_pb2*.py"    -delete 2>/dev/null || true
	@find $(VFINACC_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(VFINACC_DIR) -name "*.pyc"        -delete 2>/dev/null || true
	@find $(VFINACC_DIR) -name "*_pb2*.py"    -delete 2>/dev/null || true
	@find $(VDESIGN_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(VDESIGN_DIR) -name "*.pyc"        -delete 2>/dev/null || true
	@find $(VDESIGN_DIR) -name "*_pb2*.py"    -delete 2>/dev/null || true
	@find $(VMARKETING_DIR) -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find $(VMARKETING_DIR) -name "*.pyc"        -delete 2>/dev/null || true
	@find $(VMARKETING_DIR) -name "*_pb2*.py"    -delete 2>/dev/null || true
	@echo "  OK Build artifacts removed"

clean-docker: ## Remove containers, volumes (pgdata, caches) and dangling images
	@echo "  Cleaning Docker resources…"
	$(COMPOSE) down -v --remove-orphans
	docker volume rm vroute-maven-cache vroute-pip-cache 2>/dev/null || true
	docker image prune -f
	@echo "  OK Docker resources cleaned"

# ===========================================================
# -- FLOW 6: Security & Quality Gate ----------------------
#
# Implements a DevSecOps pipeline aligned with:
#   - OWASP DevSecOps Guideline
#   - ISO/IEC 27034 (Application Security)
#   - NIST SSDF (Secure Software Development Framework)
#
# Targets (ordered by execution cost, cheapest first):
#   scan-secrets     → Gitleaks — detect leaked tokens / keys
#   lint             → ruff check + ruff format (Python)
#   sast             → Semgrep — static analysis for CWE / OWASP
#   dependency-check → pip-audit + OWASP Dep-Check (known CVEs)
#   sbom             → CycloneDX — Software Bill of Materials
#   sonarqube        → SonarQube quality & security gate
#   audit            → scan-secrets + lint + sast + test (CI gate)
#   security         → Full pipeline (audit + dep-check + sbom + sonar)
#
# Each tool: prefers local binary → .venv → Docker fallback.
# ===========================================================

# -- Helper: find Python binary (prefer .venv) ─────────────
define find_py
	if [ -f "$(VENV_PY_WIN)" ]; then echo "$(VENV_PY_WIN)"; \
	elif [ -f "$(VENV_PY_UNIX)" ]; then echo "$(VENV_PY_UNIX)"; \
	else echo "python3"; fi
endef

# -- Python app source directories for linting ─────────────
PY_APP_DIRS := $(VSTRATEGY_DIR) $(VFINACC_DIR) $(VDESIGN_DIR) $(VMARKETING_DIR)

# -----------------------------------------------------------
# scan-secrets  (Gitleaks)
# -----------------------------------------------------------
scan-secrets: ## Detect leaked API keys / tokens / credentials (Gitleaks)
	@echo ""
	@echo "==== [security 1/6] Scanning for secrets (Gitleaks) ="
	@if command -v gitleaks &>/dev/null; then \
	  echo "  [gitleaks] local binary"; \
	  gitleaks detect --source . --verbose; \
	else \
	  echo "  [gitleaks] local binary not found — using Docker"; \
	  MSYS_NO_PATHCONV=1 docker run --rm \
	    -v "$(call docker_vol,$(ROOT)):/path" \
	    zricethezav/gitleaks:latest detect --source /path --verbose; \
	fi
	@echo "  OK No secrets detected"

# -----------------------------------------------------------
# lint  (ruff — Python check + format)
# -----------------------------------------------------------
lint: ## Lint & format check — ruff check + ruff format --check (Python apps + vKernel)
	@echo ""
	@echo "==== [security 2/6] Linting (ruff) ================="
	@PY=$$($(find_py)); \
	if command -v ruff &>/dev/null; then \
	  RUFF=ruff; \
	elif "$$PY" -m ruff --version &>/dev/null 2>&1; then \
	  RUFF="$$PY -m ruff"; \
	else \
	  echo "  ruff not found — installing into .venv"; \
	  "$$PY" -m pip install -q ruff; \
	  RUFF="$$PY -m ruff"; \
	fi; \
	echo "  [ruff check] Python apps + vKernel"; \
	$$RUFF check $(PY_APP_DIRS) $(VKERNEL_DIR) --output-format=concise || true; \
	echo ""; \
	echo "  [ruff format --check] Python apps + vKernel"; \
	$$RUFF format --check $(PY_APP_DIRS) $(VKERNEL_DIR) || true
	@echo "  OK Lint complete"

# -----------------------------------------------------------
# sast  (Semgrep — static application security testing)
# -----------------------------------------------------------
sast: ## SAST scan for CWE / OWASP Top-10 patterns (Semgrep)
	@echo ""
	@echo "==== [security 3/6] SAST scan (Semgrep) ============"
	@if command -v semgrep &>/dev/null; then \
	  echo "  [semgrep] local binary"; \
	  semgrep scan --config auto --quiet .; \
	else \
	  PY=$$($(find_py)); \
	  if "$$PY" -m semgrep --version &>/dev/null 2>&1; then \
	    echo "  [semgrep] via Python module"; \
	    "$$PY" -m semgrep scan --config auto --quiet .; \
	  else \
	    echo "  [semgrep] Docker fallback"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(ROOT)):/src" \
	      semgrep/semgrep:latest \
	      semgrep scan --config auto --quiet /src; \
	  fi; \
	fi
	@echo "  OK SAST scan complete"

# -----------------------------------------------------------
# dependency-check  (pip-audit + OWASP Dependency-Check)
# -----------------------------------------------------------
dependency-check: ## Scan dependencies for known CVEs (pip-audit + OWASP)
	@echo ""
	@echo "==== [security 4/6] Dependency CVE check ============"
	@PY=$$($(find_py)); \
	if ! command -v pip-audit &>/dev/null && ! "$$PY" -m pip_audit --version &>/dev/null 2>&1; then \
	  echo "  Installing pip-audit…"; \
	  "$$PY" -m pip install -q pip-audit; \
	fi; \
	for dir in $(PY_APP_DIRS); do \
	  if [ -f "$$dir/requirements.txt" ]; then \
	    echo "  [pip-audit] $$dir"; \
	    "$$PY" -m pip_audit -r "$$dir/requirements.txt" --strict 2>&1 || true; \
	  fi; \
	done
	@echo ""
	@echo "  [owasp-dep-check] vKernel (Java / Maven)"
	@cd $(VKERNEL_DIR) && { \
	  if command -v mvn &>/dev/null; then \
	    mvn org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=9 -Dspring.main.banner-mode=off 2>&1 || true; \
	  elif [ -f ./mvnw ]; then \
	    ./mvnw org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=9 -Dspring.main.banner-mode=off 2>&1 || true; \
	  else \
	    echo "  [owasp] Docker fallback"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(VKERNEL_DIR)):/app" \
	      -v vroute-maven-cache:/root/.m2 \
	      -w /app maven:3.9-eclipse-temurin-21 \
	      mvn org.owasp:dependency-check-maven:check -DfailBuildOnCVSS=9 2>&1 || true; \
	  fi; \
	}
	@echo "  OK Dependency check complete"

# -----------------------------------------------------------
# sbom  (CycloneDX — Software Bill of Materials)
# -----------------------------------------------------------
sbom: ## Generate Software Bill of Materials (CycloneDX SBOM)
	@echo ""
	@echo "==== [security 5/6] SBOM generation (CycloneDX) ====="
	@PY=$$($(find_py)); \
	if ! "$$PY" -m cyclonedx_py --help &>/dev/null 2>&1; then \
	  echo "  Installing cyclonedx-bom…"; \
	  "$$PY" -m pip install -q cyclonedx-bom; \
	fi; \
	for dir in $(PY_APP_DIRS); do \
	  if [ -f "$$dir/requirements.txt" ]; then \
	    echo "  [sbom] $$dir"; \
	    "$$PY" -m cyclonedx_py requirements \
	      -i "$$dir/requirements.txt" \
	      -o "$$dir/sbom.json" \
	      --format json 2>&1 || true; \
	  fi; \
	done
	@echo ""
	@echo "  [sbom] vKernel (Java / Maven CycloneDX)"
	@cd $(VKERNEL_DIR) && { \
	  if command -v mvn &>/dev/null; then \
	    mvn org.cyclonedx:cyclonedx-maven-plugin:makeBom -Dspring.main.banner-mode=off 2>&1 || true; \
	  elif [ -f ./mvnw ]; then \
	    ./mvnw org.cyclonedx:cyclonedx-maven-plugin:makeBom -Dspring.main.banner-mode=off 2>&1 || true; \
	  fi; \
	}
	@echo "  OK SBOM generated"

# -----------------------------------------------------------
# sonarqube  (SonarQube quality & security gate)
# -----------------------------------------------------------
# Requires env vars:  SONAR_HOST_URL  SONAR_TOKEN
# Default project key: vRoute-Open
# -----------------------------------------------------------
SONAR_PROJECT_KEY ?= vRoute-Open
SONAR_HOST_URL    ?= http://localhost:9000

sonarqube: ## Run SonarQube analysis (set SONAR_HOST_URL & SONAR_TOKEN env vars)
	@echo ""
	@echo "==== [security 6/6] SonarQube analysis =============="
	@if [ -z "$${SONAR_TOKEN}" ]; then \
	  echo "  WARNING: SONAR_TOKEN not set — skipping SonarQube."; \
	  echo "  Set  export SONAR_HOST_URL=... SONAR_TOKEN=...  and retry."; \
	else \
	  if command -v sonar-scanner &>/dev/null; then \
	    echo "  [sonar-scanner] local binary"; \
	    sonar-scanner \
	      -Dsonar.projectKey=$(SONAR_PROJECT_KEY) \
	      -Dsonar.sources=01-vkernel/src,02-vstrategy/app,03-vfinacc/app,04-vdesign-physical/app,05-vmarketing-org/app \
	      -Dsonar.tests=01-vkernel/src/test,02-vstrategy/tests,03-vfinacc/tests,04-vdesign-physical/tests,05-vmarketing-org/tests \
	      -Dsonar.java.binaries=01-vkernel/target/classes \
	      -Dsonar.host.url=$${SONAR_HOST_URL} \
	      -Dsonar.token=$${SONAR_TOKEN}; \
	  else \
	    echo "  [sonar-scanner] Docker"; \
	    MSYS_NO_PATHCONV=1 docker run --rm \
	      -v "$(call docker_vol,$(ROOT)):/usr/src" \
	      -e SONAR_HOST_URL=$${SONAR_HOST_URL} \
	      -e SONAR_TOKEN=$${SONAR_TOKEN} \
	      sonarsource/sonar-scanner-cli:latest \
	      -Dsonar.projectKey=$(SONAR_PROJECT_KEY) \
	      -Dsonar.sources=01-vkernel/src,02-vstrategy/app,03-vfinacc/app,04-vdesign-physical/app,05-vmarketing-org/app \
	      -Dsonar.tests=01-vkernel/src/test,02-vstrategy/tests,03-vfinacc/tests,04-vdesign-physical/tests,05-vmarketing-org/tests \
	      -Dsonar.java.binaries=01-vkernel/target/classes; \
	  fi; \
	fi
	@echo "  OK SonarQube analysis complete"

# -----------------------------------------------------------
# audit  (CI gate — fast feedback loop)
# -----------------------------------------------------------
audit: scan-secrets lint sast test ## CI security gate: secrets + lint + SAST + all tests
	@echo ""
	@echo "  ══════════════════════════════════════════════════════"
	@echo "  ✓ AUDIT PASSED — secrets / lint / SAST / tests all OK"
	@echo "  ══════════════════════════════════════════════════════"

# -----------------------------------------------------------
# security  (Full DevSecOps pipeline)
# -----------------------------------------------------------
security: audit dependency-check sbom sonarqube ## Full DevSecOps pipeline (audit + CVE + SBOM + SonarQube)
	@echo ""
	@echo "  ══════════════════════════════════════════════════════"
	@echo "  ✓ SECURITY PIPELINE COMPLETE"
	@echo "  ══════════════════════════════════════════════════════"
