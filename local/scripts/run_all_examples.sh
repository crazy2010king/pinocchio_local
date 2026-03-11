#!/bin/bash
"""
Main script to run Pinocchio examples.
Supports running all examples, by category, or individual examples.
"""

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../config/examples_config.json"
EXAMPLES_ROOT="${SCRIPT_DIR}/../examples"
TEST_RESULTS_DIR="${SCRIPT_DIR}/../test_results"
LOGS_DIR="${TEST_RESULTS_DIR}/logs"
REPORTS_DIR="${TEST_RESULTS_DIR}/reports"
SCREENSHOTS_DIR="${TEST_RESULTS_DIR}/screenshots"

# Create directories if they don't exist
mkdir -p "${LOGS_DIR}" "${REPORTS_DIR}" "${SCREENSHOTS_DIR}"

# Default values
CATEGORY=""
EXAMPLE_NAME=""
PARALLEL=1
TIMEOUT_MULTIPLIER=1
SKIP_FAILED=false
VERBOSE=false

# Show help
show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "Run Pinocchio examples"
    echo
    echo "Options:"
    echo "  --category CATEGORY   Run only examples from the specified category"
    echo "  --example NAME        Run only the specified example"
    echo "  --parallel N          Run N examples in parallel (default: 1)"
    echo "  --timeout-multiplier N Multiply timeout values by N (default: 1)"
    echo "  --skip-failed         Skip examples that failed in previous runs"
    echo "  --verbose             Show verbose output"
    echo "  --help                Show this help message"
    echo
    echo "Categories: kinematics, dynamics, collision, simulation, autodiff, other"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --category)
            CATEGORY="$2"
            shift 2
            ;;
        --example)
            EXAMPLE_NAME="$2"
            shift 2
            ;;
        --parallel)
            PARALLEL="$2"
            shift 2
            ;;
        --timeout-multiplier)
            TIMEOUT_MULTIPLIER="$2"
            shift 2
            ;;
        --skip-failed)
            SKIP_FAILED=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

echo "=" * 60
echo "Pinocchio Examples Runner"
echo "=" * 60

# Load examples from config
if [ -n "${EXAMPLE_NAME}" ]; then
    EXAMPLES=$(jq -c --arg name "${EXAMPLE_NAME}" '.examples[] | select(.name == $name and .enabled == true)' "${CONFIG_FILE}")
elif [ -n "${CATEGORY}" ]; then
    EXAMPLES=$(jq -c --arg cat "${CATEGORY}" '.examples[] | select(.category == $cat and .enabled == true)' "${CONFIG_FILE}")
else
    EXAMPLES=$(jq -c '.examples[] | select(.enabled == true)' "${CONFIG_FILE}")
fi

if [ -z "${EXAMPLES}" ]; then
    echo "⚠️  No matching examples found."
    exit 0
fi

TOTAL=$(echo "${EXAMPLES}" | wc -l)
echo "Found ${TOTAL} examples to run"
echo "Logs directory: ${LOGS_DIR}"
echo "=" * 60

# Counters
SUCCESS=0
FAILED=0
SKIPPED=0
TIMED_OUT=0
RESULTS_FILE="${REPORTS_DIR}/run_results_$(date +%Y%m%d_%H%M%S).json"
RESULTS=()

# Run each example
while IFS= read -r example; do
    name=$(echo "${example}" | jq -r '.name')
    category=$(echo "${example}" | jq -r '.category')
    language=$(echo "${example}" | jq -r '.language')
    path=$(echo "${example}" | jq -r '.path')
    timeout=$(echo "${example}" | jq -r '.timeout')
    run_cmd=$(echo "${example}" | jq -r '.run_cmd')

    # Calculate actual timeout
    actual_timeout=$((timeout * TIMEOUT_MULTIPLIER))

    # Skip if example failed previously
    if [ "${SKIP_FAILED}" = true ] && [ -f "${LOGS_DIR}/${name}.failed" ]; then
        echo "⏭️  Skipping ${name} (failed previously)"
        SKIPPED=$((SKIPPED + 1))
        RESULTS+=("{\"name\":\"${name}\",\"status\":\"skipped\",\"reason\":\"previously failed\"}")
        continue
    fi

    echo -e "\n▶️  Running ${name} (${language}, ${category})..."
    echo "Timeout: ${actual_timeout}s"

    log_file="${LOGS_DIR}/${name}.log"
    start_time=$(date +%s)

    # Determine working directory and command
    if [ "${language}" = "python" ]; then
        work_dir="${EXAMPLES_ROOT}/python"
        cmd="python3 ${EXAMPLES_ROOT}/${path}"
    else
        work_dir="${EXAMPLES_ROOT}/cpp/build"
        cmd="${run_cmd}"
    fi

    # Run the command with timeout
    set +e
    if [ "${VERBOSE}" = true ]; then
        timeout "${actual_timeout}s" bash -c "cd '${work_dir}' && ${cmd}" 2>&1 | tee "${log_file}"
    else
        timeout "${actual_timeout}s" bash -c "cd '${work_dir}' && ${cmd}" > "${log_file}" 2>&1
    fi
    exit_code=$?
    set -e

    end_time=$(date +%s)
    duration=$((end_time - start_time))

    # Check result
    if [ ${exit_code} -eq 124 ]; then
        echo "⏱️  ${name} timed out after ${duration}s"
        TIMED_OUT=$((TIMED_OUT + 1))
        touch "${LOGS_DIR}/${name}.failed"
        status="timeout"
    elif [ ${exit_code} -eq 0 ]; then
        echo "✅ ${name} completed successfully in ${duration}s"
        SUCCESS=$((SUCCESS + 1))
        rm -f "${LOGS_DIR}/${name}.failed"
        status="success"
    else
        echo "❌ ${name} failed with exit code ${exit_code} after ${duration}s"
        FAILED=$((FAILED + 1))
        touch "${LOGS_DIR}/${name}.failed"
        status="failed"
    fi

    # Save result
    RESULTS+=("{\"name\":\"${name}\",\"category\":\"${category}\",\"language\":\"${language}\",\"status\":\"${status}\",\"duration\":${duration},\"log_file\":\"${log_file}\",\"exit_code\":${exit_code}}")

done <<< "${EXAMPLES}"

# Generate results summary
echo -e "\n" + "=" * 60
echo "Run Summary:"
echo "=" * 60
echo "Total examples: ${TOTAL}"
echo "Success: ${SUCCESS}"
echo "Failed: ${FAILED}"
echo "Timed out: ${TIMED_OUT}"
echo "Skipped: ${SKIPPED}"
echo "Success rate: $(( (SUCCESS * 100) / TOTAL ))%"

# Save results to file
echo "["$(IFS=,; echo "${RESULTS[*]}")"]" > "${RESULTS_FILE}"
echo -e "\n📝 Full results saved to: ${RESULTS_FILE}"
echo "📊 Run generate_report.py to create a detailed report"

echo "=" * 60

# Exit with error if any failures
if [ ${FAILED} -gt 0 ] || [ ${TIMED_OUT} -gt 0 ]; then
    exit 1
else
    exit 0
fi
