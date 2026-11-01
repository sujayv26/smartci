
import os
import subprocess

# Map source files to the tests that depend on them.
TEST_MAP = {
    "src/pricing.py": [
        "tests/test_pricing.py",
        "tests/test_cart.py"
    ],
    "src/cart.py": [
        "tests/test_cart.py"
    ],
    "src/inventory.py": [
        "tests/test_inventory.py"
    ]
}

# Changes to these files require all tests.
FULL_TEST_PATHS = {
    "requirements.txt",
    "pytest.ini",
    "src/__init__.py"
}


def write_output(name, value):
    output_file = os.environ.get("GITHUB_OUTPUT")

    if output_file:
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{name}={value}\n")
    else:
        print(f"{name}={value}")


def main():
    base = os.environ.get("BASE_SHA")
    head = os.environ.get("HEAD_SHA")

    # Run all tests if this is the first push.
    if not base or set(base) == {"0"}:
        write_output("run_all", "true")
        write_output("has_tests", "true")
        write_output("tests", "")
        return

    # Detect changed files using Git.
    result = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        capture_output=True,
        text=True,
        check=True
    )

    changed_files = result.stdout.splitlines()

    selected_tests = set()
    run_all = False

    for file in changed_files:
        file = file.replace("\\", "/")

        # Configuration and workflow changes require all tests.
        if file in FULL_TEST_PATHS:
            run_all = True
            break

        if file.startswith(".github/workflows/"):
            run_all = True
            break

        # If a test file changes, select that test.
        if file.startswith("tests/"):
            if file.endswith(".py"):
                if os.path.isfile(file):
                    selected_tests.add(file)
            else:
                run_all = True
                break
            continue

        # Select tests based on source dependencies.
        if file in TEST_MAP:
            selected_tests.update(TEST_MAP[file])
            continue

        # Unknown source changes require all tests.
        if file.startswith("src/"):
            run_all = True
            break

    # Remove deleted test files from the selection.
    selected_tests = {
        test for test in selected_tests
        if os.path.isfile(test)
    }

    tests = " ".join(sorted(selected_tests))

    write_output("run_all", str(run_all).lower())
    write_output("has_tests", str(bool(tests)).lower())
    write_output("tests", tests)


if __name__ == "__main__":
    main()
