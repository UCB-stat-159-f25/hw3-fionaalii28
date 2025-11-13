# =========================================================
# Makefile — STAT 159 HW3: LOSC Event Tutorial
# Purpose: Environment setup, MyST site build, and cleanup
# =========================================================

# Environment name
ENV_NAME = ligo

# Prevent accidental filename collisions
.PHONY: env html clean

# ---------------------------------------------------------
# 1. Create or update the Conda environment
# ---------------------------------------------------------
env: environment.yml
	@echo "⟶ Setting up or updating environment: $(ENV_NAME)"
	conda env update -n $(ENV_NAME) -f environment.yml --prune
	@echo "✓ Environment ready (activate with: conda activate $(ENV_NAME))"

# ---------------------------------------------------------
# 2. Build the MyST HTML site locally
# ---------------------------------------------------------
html:
	@echo "⟶ Building local MyST HTML site..."
	myst build --html
	@echo "✓ Build complete — open _build/html/index.html to preview."

# ---------------------------------------------------------
# 3. Clean up generated files and build artifacts
# ---------------------------------------------------------
clean:
	@echo "⟶ Cleaning up figures, audio, and _build directories..."
	rm -rf figures audio _build
	@echo "✓ Cleanup complete."
