# High-Scale PGS Prime Generator - Makefile (Apple Silicon Only)
# =============================================================
#
# Apple-only build for macOS on Apple Silicon.
# Assumes GMP/MPFR installed via Homebrew in /opt/homebrew.
#
# Usage:
#   make       - Build library, CLI, and tests
#   make test  - Build and run tests
#   make clean - Clean build artifacts
#   make info  - Show build configuration

.DEFAULT_GOAL := all

SRC_DIR := src
INCLUDE_DIR := include
TEST_DIR := tests
RESEARCH_DIR := research
BUILD_DIR := build
BIN_DIR := bin

CC := clang

UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)
ifneq ($(UNAME_S),Darwin)
$(error High-Scale PGS is Apple Silicon only: expected Darwin)
endif
ifneq ($(UNAME_M),arm64)
$(error High-Scale PGS is Apple Silicon only: expected arm64)
endif

GMP_INCLUDE ?= -I/opt/homebrew/include
GMP_LIB ?= -L/opt/homebrew/lib -lgmp
MPFR_INCLUDE ?= -I/opt/homebrew/include
MPFR_LIB ?= -L/opt/homebrew/lib -lmpfr

MISSING := $(shell test -f /opt/homebrew/include/gmp.h || echo missing_gmp_hdr)
MISSING += $(shell test -f /opt/homebrew/include/mpfr.h || echo missing_mpfr_hdr)
MISSING += $(shell test -f /opt/homebrew/lib/libgmp.dylib || echo missing_gmp_lib)
MISSING += $(shell test -f /opt/homebrew/lib/libmpfr.dylib || echo missing_mpfr_lib)
ifneq (,$(filter missing_%,$(MISSING)))
$(error GMP/MPFR not found at Homebrew paths (/opt/homebrew). Install with `brew install gmp mpfr` or override GMP_INCLUDE/MPFR_INCLUDE/GMP_LIB/MPFR_LIB)
endif

CFLAGS := -std=c99 -O3 -march=native -Wall -Wextra -I$(INCLUDE_DIR) $(GMP_INCLUDE) $(MPFR_INCLUDE)
LDFLAGS := $(GMP_LIB) $(MPFR_LIB) -lm
DEBUG_CFLAGS := -std=c99 -O0 -g3 -fno-omit-frame-pointer -DDEBUG

LIB_SOURCES := \
	$(SRC_DIR)/pgs_chamber.c \
	$(SRC_DIR)/pgs_diagnostics.c \
	$(SRC_DIR)/pgs_emit.c \
	$(SRC_DIR)/pgs_parse.c \
	$(SRC_DIR)/pgs_status.c \
	$(SRC_DIR)/pgs_wheel.c
LIB_OBJECTS := $(patsubst $(SRC_DIR)/%.c,$(BUILD_DIR)/%.o,$(LIB_SOURCES))

CLI_SOURCE := $(SRC_DIR)/pgs_cli.c
CLI_OBJECT := $(BUILD_DIR)/pgs_cli.o

TEST_PARSE_SOURCE := $(TEST_DIR)/test_parse.c
TEST_PARSE_OBJECT := $(BUILD_DIR)/test_parse.o
TEST_SCAFFOLD_SOURCE := $(TEST_DIR)/test_scaffold.c
TEST_SCAFFOLD_OBJECT := $(BUILD_DIR)/test_scaffold.o
TEST_EMIT_SOURCE := $(TEST_DIR)/test_emit.c
TEST_EMIT_OBJECT := $(BUILD_DIR)/test_emit.o
TEST_WHEEL_SOURCE := $(TEST_DIR)/test_wheel.c
TEST_WHEEL_OBJECT := $(BUILD_DIR)/test_wheel.o
TEST_INTEGER_CHAMBER_SOURCE := $(TEST_DIR)/test_integer_chamber.c
TEST_INTEGER_CHAMBER_OBJECT := $(BUILD_DIR)/test_integer_chamber.o
RESEARCH_BATCH_CLOSURE_SOURCE := $(RESEARCH_DIR)/batch_closure_chamber_probe.c
RESEARCH_BATCH_CLOSURE_OBJECT := $(BUILD_DIR)/batch_closure_chamber_probe.o
RESEARCH_DIVISOR_COST_SOURCE := $(RESEARCH_DIR)/gmp_divisor_state_cost_probe.c
RESEARCH_DIVISOR_COST_OBJECT := $(BUILD_DIR)/gmp_divisor_state_cost_probe.o
RESEARCH_OPTION_FEASIBILITY_SOURCE := $(RESEARCH_DIR)/pgs_option_feasibility_probe.c
RESEARCH_OPTION_FEASIBILITY_OBJECT := $(BUILD_DIR)/pgs_option_feasibility_probe.o
RESEARCH_CERTIFICATE_VERIFIER_SOURCE := $(RESEARCH_DIR)/pgs_certificate_verifier_probe.c
RESEARCH_CERTIFICATE_VERIFIER_OBJECT := $(BUILD_DIR)/pgs_certificate_verifier_probe.o
RESEARCH_WITNESS_MINER_SOURCE := $(RESEARCH_DIR)/pgs_witness_miner_probe.c
RESEARCH_WITNESS_MINER_OBJECT := $(BUILD_DIR)/pgs_witness_miner_probe.o

STATIC_LIB := $(BUILD_DIR)/libpgs_high_scale.a
CLI_EXECUTABLE := $(BIN_DIR)/pgs_cli
TEST_PARSE_EXECUTABLE := $(BIN_DIR)/test_parse
TEST_SCAFFOLD_EXECUTABLE := $(BIN_DIR)/test_scaffold
TEST_EMIT_EXECUTABLE := $(BIN_DIR)/test_emit
TEST_WHEEL_EXECUTABLE := $(BIN_DIR)/test_wheel
TEST_INTEGER_CHAMBER_EXECUTABLE := $(BIN_DIR)/test_integer_chamber
RESEARCH_BATCH_CLOSURE_EXECUTABLE := $(BIN_DIR)/batch_closure_chamber_probe
RESEARCH_DIVISOR_COST_EXECUTABLE := $(BIN_DIR)/gmp_divisor_state_cost_probe
RESEARCH_OPTION_FEASIBILITY_EXECUTABLE := $(BIN_DIR)/pgs_option_feasibility_probe
RESEARCH_CERTIFICATE_VERIFIER_EXECUTABLE := $(BIN_DIR)/pgs_certificate_verifier_probe
RESEARCH_WITNESS_MINER_EXECUTABLE := $(BIN_DIR)/pgs_witness_miner_probe

$(BUILD_DIR):
	@mkdir -p $(BUILD_DIR)

$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c | $(BUILD_DIR)
	@echo "Compiling $<..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/%.o: $(TEST_DIR)/%.c | $(BUILD_DIR)
	@echo "Compiling $<..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(STATIC_LIB): $(LIB_OBJECTS) | $(BUILD_DIR)
	@echo "Creating static library..."
	@ar rcs $@ $^

$(CLI_OBJECT): $(CLI_SOURCE) | $(BUILD_DIR)
	@echo "Compiling CLI..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(CLI_EXECUTABLE): $(CLI_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking CLI executable..."
	@$(CC) $(CLI_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(TEST_PARSE_OBJECT): $(TEST_PARSE_SOURCE) | $(BUILD_DIR)
	@echo "Compiling test_parse..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(TEST_PARSE_EXECUTABLE): $(TEST_PARSE_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking test_parse executable..."
	@$(CC) $(TEST_PARSE_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(TEST_SCAFFOLD_OBJECT): $(TEST_SCAFFOLD_SOURCE) | $(BUILD_DIR)
	@echo "Compiling test_scaffold..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(TEST_SCAFFOLD_EXECUTABLE): $(TEST_SCAFFOLD_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking test_scaffold executable..."
	@$(CC) $(TEST_SCAFFOLD_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(TEST_EMIT_OBJECT): $(TEST_EMIT_SOURCE) | $(BUILD_DIR)
	@echo "Compiling test_emit..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(TEST_EMIT_EXECUTABLE): $(TEST_EMIT_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking test_emit executable..."
	@$(CC) $(TEST_EMIT_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(TEST_WHEEL_OBJECT): $(TEST_WHEEL_SOURCE) | $(BUILD_DIR)
	@echo "Compiling test_wheel..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(TEST_WHEEL_EXECUTABLE): $(TEST_WHEEL_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking test_wheel executable..."
	@$(CC) $(TEST_WHEEL_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(TEST_INTEGER_CHAMBER_OBJECT): $(TEST_INTEGER_CHAMBER_SOURCE) | $(BUILD_DIR)
	@echo "Compiling test_integer_chamber..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(TEST_INTEGER_CHAMBER_EXECUTABLE): $(TEST_INTEGER_CHAMBER_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking test_integer_chamber executable..."
	@$(CC) $(TEST_INTEGER_CHAMBER_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(RESEARCH_BATCH_CLOSURE_OBJECT): $(RESEARCH_BATCH_CLOSURE_SOURCE) | $(BUILD_DIR)
	@echo "Compiling batch_closure_chamber_probe..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(RESEARCH_BATCH_CLOSURE_EXECUTABLE): $(RESEARCH_BATCH_CLOSURE_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking batch_closure_chamber_probe executable..."
	@$(CC) $(RESEARCH_BATCH_CLOSURE_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(RESEARCH_DIVISOR_COST_OBJECT): $(RESEARCH_DIVISOR_COST_SOURCE) | $(BUILD_DIR)
	@echo "Compiling gmp_divisor_state_cost_probe..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(RESEARCH_DIVISOR_COST_EXECUTABLE): $(RESEARCH_DIVISOR_COST_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking gmp_divisor_state_cost_probe executable..."
	@$(CC) $(RESEARCH_DIVISOR_COST_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(RESEARCH_OPTION_FEASIBILITY_OBJECT): $(RESEARCH_OPTION_FEASIBILITY_SOURCE) | $(BUILD_DIR)
	@echo "Compiling pgs_option_feasibility_probe..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(RESEARCH_OPTION_FEASIBILITY_EXECUTABLE): $(RESEARCH_OPTION_FEASIBILITY_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking pgs_option_feasibility_probe executable..."
	@$(CC) $(RESEARCH_OPTION_FEASIBILITY_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(RESEARCH_CERTIFICATE_VERIFIER_OBJECT): $(RESEARCH_CERTIFICATE_VERIFIER_SOURCE) | $(BUILD_DIR)
	@echo "Compiling pgs_certificate_verifier_probe..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(RESEARCH_CERTIFICATE_VERIFIER_EXECUTABLE): $(RESEARCH_CERTIFICATE_VERIFIER_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking pgs_certificate_verifier_probe executable..."
	@$(CC) $(RESEARCH_CERTIFICATE_VERIFIER_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

$(RESEARCH_WITNESS_MINER_OBJECT): $(RESEARCH_WITNESS_MINER_SOURCE) | $(BUILD_DIR)
	@echo "Compiling pgs_witness_miner_probe..."
	@$(CC) $(CFLAGS) -c $< -o $@

$(RESEARCH_WITNESS_MINER_EXECUTABLE): $(RESEARCH_WITNESS_MINER_OBJECT) $(STATIC_LIB) | $(BIN_DIR)
	@echo "Linking pgs_witness_miner_probe executable..."
	@$(CC) $(RESEARCH_WITNESS_MINER_OBJECT) $(STATIC_LIB) $(LDFLAGS) -o $@

.PHONY: all lib cli test-executables research test clean info help

all: lib cli test-executables
	@echo "Build complete."

lib: $(STATIC_LIB)

cli: $(CLI_EXECUTABLE)

test-executables: $(TEST_PARSE_EXECUTABLE) $(TEST_SCAFFOLD_EXECUTABLE) $(TEST_EMIT_EXECUTABLE) $(TEST_WHEEL_EXECUTABLE) $(TEST_INTEGER_CHAMBER_EXECUTABLE)

research: $(RESEARCH_BATCH_CLOSURE_EXECUTABLE) $(RESEARCH_DIVISOR_COST_EXECUTABLE) $(RESEARCH_OPTION_FEASIBILITY_EXECUTABLE) $(RESEARCH_CERTIFICATE_VERIFIER_EXECUTABLE) $(RESEARCH_WITNESS_MINER_EXECUTABLE)

test: test-executables
	@echo ""
	@echo "Running scale parser tests..."
	@$(TEST_PARSE_EXECUTABLE)
	@echo ""
	@echo "Running scaffold tests..."
	@$(TEST_SCAFFOLD_EXECUTABLE) > /tmp/pgs_scaffold_test.out
	@cat /tmp/pgs_scaffold_test.out
	@echo ""
	@echo "Running emitter tests..."
	@$(TEST_EMIT_EXECUTABLE) > /tmp/pgs_emit_test.out
	@test "$$(cat /tmp/pgs_emit_test.out)" = '{"n":"10","q":"13"}'
	@cat /tmp/pgs_emit_test.out
	@echo ""
	@echo "Running wheel tests..."
	@$(TEST_WHEEL_EXECUTABLE)
	@echo ""
	@echo "Running integer chamber tests..."
	@$(TEST_INTEGER_CHAMBER_EXECUTABLE)
	@echo ""
	@echo "Running CLI tests..."
	@sh $(TEST_DIR)/test_cli.sh $(CLI_EXECUTABLE)
	@echo ""
	@echo "Running forbidden-symbol tests..."
	@sh $(TEST_DIR)/test_forbidden_symbols.sh . $(CLI_EXECUTABLE) $(STATIC_LIB)

info:
	@echo "High-Scale PGS Prime Generator Build Information (Apple Silicon only)"
	@echo "GMP Include:  $(GMP_INCLUDE)"
	@echo "GMP Lib:      $(GMP_LIB)"
	@echo "MPFR Include: $(MPFR_INCLUDE)"
	@echo "MPFR Lib:     $(MPFR_LIB)"
	@echo "CFLAGS:       $(CFLAGS)"
	@echo "LDFLAGS:      $(LDFLAGS)"

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf $(BUILD_DIR) $(BIN_DIR)

help:
	@echo "High-Scale PGS Prime Generator - Build System (Apple Silicon only)"
	@echo ""
	@echo "Available targets:"
	@echo "  all              - Build library, CLI, and tests"
	@echo "  lib              - Build static library only"
	@echo "  cli              - Build CLI tool"
	@echo "  research         - Build side research probes"
	@echo "  test             - Build and run tests"
	@echo "  clean            - Remove build artifacts"
	@echo "  info             - Show build configuration"
	@echo "  help             - Show this help"
