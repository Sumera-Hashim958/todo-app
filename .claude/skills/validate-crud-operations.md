---
name: validate-crud-operations
owner: qa-agent
project: todo-app-phase-1
version: 1.0.0
---

# Validate CRUD Operations

## Purpose
Systematically test all Create, Read, Update, Delete operations for todo items in the CLI application to ensure each operation works correctly and produces expected outputs.

## When to Use
- After implementing any CRUD operation (add, list, update, complete, delete)
- Before marking a task as complete in `/sp.implement`
- When regression testing after code changes
- Before creating a pull request or release
- When investigating reported bugs in CRUD functionality

## Inputs
**Required:**
- `operation`: The CRUD operation to test (add | list | update | complete | delete | all)
- `app_command`: The CLI command to invoke the todo app (e.g., `python todo.py`, `./todo`)

**Optional:**
- `test_data_file`: Path to JSON file containing test cases (defaults to inline test cases)
- `verbose`: Boolean flag for detailed output (default: false)

## Step-by-Step Process

### Step 1: Setup Test Environment
1. Verify the todo app CLI is accessible at the specified `app_command`
2. Clear any existing test data to ensure clean state
3. Create a temporary test data directory if needed
4. Confirm the app returns help text when run with `--help` or no args

### Step 2: Test CREATE Operation (Add)
1. Execute: `{app_command} add "Test todo item"`
2. Verify exit code is 0 (success)
3. Verify output confirms creation (e.g., "Added: Test todo item" or similar)
4. Execute list command to confirm item exists
5. Test adding item with special characters: `{app_command} add "Item with 'quotes' and \"escapes\""`
6. Verify proper handling of special characters
7. Test adding item with maximum allowed length
8. Verify acceptance or appropriate error message

### Step 3: Test READ Operation (List)
1. Execute: `{app_command} list`
2. Verify exit code is 0
3. Verify output shows previously added items
4. Verify format is human-readable (numbered list or similar)
5. Test listing when no todos exist (empty state)
6. Verify appropriate message (e.g., "No todos found")
7. Add 5 test todos and verify all appear in list output
8. Verify correct ordering (by ID or creation order)

### Step 4: Test UPDATE Operation
1. Add a test todo item and capture its ID
2. Execute: `{app_command} update {id} "Updated text"`
3. Verify exit code is 0
4. Verify output confirms update
5. Execute list to confirm text changed
6. Test updating with invalid ID (e.g., 99999)
7. Verify appropriate error message and non-zero exit code
8. Test updating with empty text
9. Verify appropriate validation error or acceptance per spec

### Step 5: Test COMPLETE Operation
1. Add a test todo item and capture its ID
2. Execute: `{app_command} complete {id}`
3. Verify exit code is 0
4. Verify output confirms completion
5. Execute list and verify item is marked complete or filtered
6. Test completing invalid ID
7. Verify appropriate error message and non-zero exit code
8. Test completing already-completed item
9. Verify idempotent behavior or appropriate error per spec

### Step 6: Test DELETE Operation
1. Add a test todo item and capture its ID
2. Execute: `{app_command} delete {id}`
3. Verify exit code is 0
4. Verify output confirms deletion
5. Execute list and verify item no longer appears
6. Test deleting invalid ID
7. Verify appropriate error message and non-zero exit code
8. Test deleting already-deleted item
9. Verify appropriate error handling

### Step 7: Generate Test Report
1. Collect all test results (pass/fail for each operation)
2. Count total tests, passed, failed, skipped
3. List any failures with specific command and expected vs actual output
4. Calculate pass percentage
5. Generate timestamped test report

## Output

### Success Output Format
```
CRUD Operations Test Report
============================
Timestamp: 2025-12-30T14:30:00Z
App Command: python todo.py

Results:
✓ CREATE: 3/3 tests passed
✓ READ: 4/4 tests passed
✓ UPDATE: 4/4 tests passed
✓ COMPLETE: 4/4 tests passed
✓ DELETE: 4/4 tests passed

Overall: 19/19 tests passed (100%)
Status: ALL TESTS PASSED
```

### Failure Output Format
```
CRUD Operations Test Report
============================
Timestamp: 2025-12-30T14:30:00Z
App Command: python todo.py

Results:
✓ CREATE: 3/3 tests passed
✗ READ: 3/4 tests passed
  Failed: List empty state
    Command: python todo.py list
    Expected: "No todos found"
    Actual: "" (empty output)
    Exit Code: 0 (expected: 0)
✓ UPDATE: 4/4 tests passed
✓ COMPLETE: 4/4 tests passed
✓ DELETE: 4/4 tests passed

Overall: 18/19 tests passed (94.7%)
Status: FAILURES DETECTED

Failed Tests:
1. READ - List empty state: Expected message not displayed
```

## Failure Handling

### App Command Not Found
- **Detection**: Command execution fails with "command not found" or similar
- **Action**: Report error with clear message: "Todo app not found at: {app_command}"
- **Exit**: Return failure status with code SKILL_ERROR_APP_NOT_FOUND
- **Next Steps**: User must verify app path or build app before retesting

### Test Data Corruption
- **Detection**: Unable to verify created items in subsequent list operations
- **Action**: Report: "Data inconsistency detected - created item not found in list"
- **Cleanup**: Attempt to clear test data
- **Exit**: Return failure status with code SKILL_ERROR_DATA_CORRUPTION
- **Next Steps**: Investigate app's data persistence mechanism

### Unexpected Exit Codes
- **Detection**: Operation returns non-zero exit code for expected-success operation
- **Action**: Capture stderr, stdout, and exit code
- **Report**: Include full command, expected code, actual code, and all output
- **Exit**: Mark test as failed, continue with remaining tests
- **Next Steps**: Developer investigates specific operation failure

### Timeout During Test
- **Detection**: Any single operation takes >10 seconds
- **Action**: Kill the process, mark test as failed
- **Report**: "Operation timed out after 10s: {command}"
- **Exit**: Continue with remaining tests if possible
- **Next Steps**: Investigate performance issue or infinite loop

### Missing Required Input
- **Detection**: `operation` or `app_command` parameter not provided
- **Action**: Report: "Missing required parameter: {parameter_name}"
- **Exit**: Return failure status with code SKILL_ERROR_INVALID_INPUT
- **Next Steps**: User provides missing parameter and retries

## Notes
- This skill focuses on black-box testing via CLI interface only
- Each test is independent and should not rely on state from previous tests
- All tests should be repeatable and deterministic
- Test execution order matters for data-dependent tests (create before list, etc.)
- Phase 1 assumes in-memory or simple file-based storage - persistence not guaranteed across app restarts
