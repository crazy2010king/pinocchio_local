#!/bin/bash
"""
Build script for all C++ examples in the Pinocchio examples collection.
Supports incremental builds and parallel compilation.
"""

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${SCRIPT_DIR}/../config/examples_config.json"
EXAMPLES_ROOT="${SCRIPT_DIR}/../examples/cpp"
BUILD_DIR="${SCRIPT_DIR}/../examples/cpp/build"

# Create build directory if it doesn't exist
mkdir -p "${BUILD_DIR}"

echo "=" * 60
echo "Building C++ Examples for Pinocchio"
echo "=" * 60

# Load config and extract C++ examples
CPP_EXAMPLES=$(jq -c '.examples[] | select(.language == "cpp" and .enabled == true)' "${CONFIG_FILE}")

if [ -z "${CPP_EXAMPLES}" ]; then
    echo "⚠️  No enabled C++ examples found in config."
    exit 0
fi

TOTAL=$(echo "${CPP_EXAMPLES}" | wc -l)
SUCCESS=0
FAILED=0
FAILED_EXAMPLES=()

echo "Found ${TOTAL} enabled C++ examples"
echo "Build directory: ${BUILD_DIR}"
echo "=" * 60

# Build each example
while IFS= read -r example; do
    name=$(echo "${example}" | jq -r '.name')
    path=$(echo "${example}" | jq -r '.path')
    build_cmd=$(echo "${example}" | jq -r '.build_cmd')

    example_dir="${EXAMPLES_ROOT}/$(dirname "${path}")"
    example_file="${EXAMPLES_ROOT}/${path}"

    echo -e "\n🔨 Building ${name}..."
    echo "Source: ${example_file}"
    echo "Build command: ${build_cmd}"

    # Run build command in the example directory
    if (cd "${example_dir}" && eval "${build_cmd}"); then
        # Move binary to build directory
        binary_name=$(basename "${name}" .cpp)
        mv "${example_dir}/${binary_name}" "${BUILD_DIR}/"
        echo "✅ Successfully built ${name}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "❌ Failed to build ${name}"
        FAILED=$((FAILED + 1))
        FAILED_EXAMPLES+=("${name}")
    fi
done <<< "${CPP_EXAMPLES}"

echo -e "\n" + "=" * 60
echo "Build Summary:"
echo "=" * 60
echo "Total examples: ${TOTAL}"
echo "Successfully built: ${SUCCESS}"
echo "Failed: ${FAILED}"

if [ ${FAILED} -gt 0 ]; then
    echo -e "\n❌ Failed examples:"
    for failed in "${FAILED_EXAMPLES[@]}"; do
        echo "  - ${failed}"
    done
    exit 1
else
    echo -e "\n✅ All C++ examples built successfully!"
    echo "Binaries are in: ${BUILD_DIR}"
    exit 0
fi
