---
name: verify-input-edge-cases
owner: qa-agent
project: todo-app-phase-1
version: 1.0.0
---

# Verify Input Edge Cases

## Purpose
Test boundary conditions, malformed inputs, and edge cases for all todo CLI operations to ensure robust error handling, validation, and graceful degradation.

## When to Use
- After implementing input validation for any operation
- Before completing acceptance criteria review
- When testing error handling improvements
- During regression testing for validation bugs
- Before major releases to ensure input robustness

## Inputs
**Required:**
- `app_command`: The CLI command to invoke the todo app (e.g., `python todo.py`, `./todo`)

**Optional:**
- `operation_filter`: Test only specific operation edge cases (add | list | update | complete | delete | all)
- `spec_file`: Path to spec.md for reference to validation rules
- `verbose`: Boolean flag for detailed output (default: false)

## Step-by-Step Process

### Step 1: Environment Setup
1. Verify todo app is accessible at `app_command`
2. If `spec_file` provided, read validation rules from spec
3. Prepare test data for edge cases
4. Initialize results tracking structure

### Step 2: Test Empty/Missing Input Cases

#### 2.1 Add Operation - Empty Input
1. Execute: `{app_command} add ""`
2. Verify non-zero exit code (validation error expected)
3. Verify error message mentions empty or missing title
4. Execute: `{app_command} add "   "` (whitespace only)
5. Verify proper validation (reject or trim per spec)

#### 2.2 Add Operation - No Argument
1. Execute: `{app_command} add`
2. Verify non-zero exit code
3. Verify helpful error message (e.g., "Missing todo text")

#### 2.3 Update Operation - Empty Input
1. Add test todo, capture ID
2. Execute: `{app_command} update {id} ""`
3. Verify validation error or acceptance per spec
4. Execute: `{app_command} update {id}`
5. Verify error message for missing text argument

#### 2.4 Operations Without Arguments
1. Execute: `{app_command} complete`
2. Verify error message for missing ID
3. Execute: `{app_command} delete`
4. Verify error message for missing ID

### Step 3: Test Invalid ID Cases

#### 3.1 Non-Existent IDs
1. Execute: `{app_command} update 99999 "text"`
2. Verify error: "Todo not found" or similar
3. Verify non-zero exit code
4. Execute: `{app_command} complete 99999`
5. Verify same error behavior
6. Execute: `{app_command} delete 99999`
7. Verify same error behavior

#### 3.2 Malformed IDs
1. Execute: `{app_command} update abc "text"` (string instead of number)
2. Verify error: "Invalid ID" or "ID must be number"
3. Execute: `{app_command} complete -5` (negative number)
4. Verify appropriate validation error
5. Execute: `{app_command} delete 1.5` (decimal)
6. Verify integer validation error

#### 3.3 Special Character IDs
1. Execute: `{app_command} update "'; DROP TABLE todos;" "text"` (SQL injection attempt)
2. Verify safe handling (validation error, not execution)
3. Execute: `{app_command} complete "../../../etc/passwd"` (path traversal attempt)
4. Verify safe handling

### Step 4: Test Boundary Length Cases

#### 4.1 Maximum Length Title
1. Generate string of maximum allowed length per spec (default: 200 chars)
2. Execute: `{app_command} add "{max_length_string}"`
3. Verify acceptance or appropriate error
4. If accepted, verify full text stored via list command

#### 4.2 Over-Maximum Length Title
1. Generate string of max length + 1
2. Execute: `{app_command} add "{over_max_string}"`
3. Verify validation error with clear message
4. Verify non-zero exit code

#### 4.3 Extremely Long Input
1. Generate string of 10,000 characters
2. Execute: `{app_command} add "{extreme_string}"`
3. Verify graceful rejection (not crash)
4. Verify clear error message about length limit

### Step 5: Test Special Character Handling

#### 5.1 Quotes and Escapes
1. Execute: `{app_command} add "Todo with \"double quotes\""`
2. Verify proper storage and retrieval
3. Execute: `{app_command} add "Todo with 'single quotes'"`
4. Verify proper handling
5. Execute: `{app_command} add "Todo with both \"types\" of 'quotes'"`
6. Verify correct escaping

#### 5.2 Newlines and Control Characters
1. Execute: `{app_command} add "Todo\nwith\nnewlines"`
2. Verify handling per spec (accept, reject, or sanitize)
3. Execute: `{app_command} add "Todo\twith\ttabs"`
4. Verify consistent handling
5. Execute: `{app_command} add "Todo\x00with\x00nulls"`
6. Verify safe handling (no crashes)

#### 5.3 Unicode and Emoji
1. Execute: `{app_command} add "Todo with emoji 🚀✅"`
2. Verify proper storage and display
3. Execute: `{app_command} add "中文 Русский العربية"`
4. Verify Unicode support
5. Execute: `{app_command} add "Special: ™ © ® € £ ¥"`
6. Verify special character handling

### Step 6: Test Duplicate Detection (if specified)

#### 6.1 Exact Duplicates
1. Execute: `{app_command} add "Duplicate todo"`
2. Execute: `{app_command} add "Duplicate todo"` (exact same)
3. Verify behavior per spec (allow, warn, or reject)
4. If allowed, verify both appear in list with unique IDs

#### 6.2 Case Sensitivity
1. Execute: `{app_command} add "Case Test"`
2. Execute: `{app_command} add "case test"`
3. Verify whether treated as duplicate per spec

### Step 7: Test Concurrent/State Edge Cases

#### 7.1 Delete Then Access
1. Add test todo, capture ID
2. Execute: `{app_command} delete {id}`
3. Execute: `{app_command} complete {id}` (operate on deleted)
4. Verify error: "Todo not found"
5. Execute: `{app_command} update {id} "text"`
6. Verify same error behavior

#### 7.2 Complete Then Complete
1. Add test todo, capture ID
2. Execute: `{app_command} complete {id}`
3. Execute: `{app_command} complete {id}` (already complete)
4. Verify idempotent (no error) or appropriate message per spec

#### 7.3 Operations on Empty List
1. Clear all todos
2. Execute: `{app_command} list`
3. Verify friendly empty state message
4. Execute: `{app_command} complete 1`
5. Verify appropriate "not found" error

### Step 8: Compile Edge Case Report
1. Categorize results by edge case type
2. Count total edge cases tested vs passed
3. List any failures with input, expected behavior, actual behavior
4. Highlight any crashes or unexpected errors
5. Generate timestamped report

## Output

### Success Output Format
```
Input Edge Cases Test Report
==============================
Timestamp: 2025-12-30T15:00:00Z
App Command: python todo.py

Results by Category:
✓ Empty/Missing Input: 8/8 cases passed
✓ Invalid IDs: 9/9 cases passed
✓ Boundary Lengths: 4/4 cases passed
✓ Special Characters: 9/9 cases passed
✓ Duplicates: 3/3 cases passed
✓ State Edge Cases: 5/5 cases passed

Overall: 38/38 edge cases passed (100%)
Status: ALL EDGE CASES HANDLED CORRECTLY

No crashes, no unexpected errors detected.
```

### Failure Output Format
```
Input Edge Cases Test Report
==============================
Timestamp: 2025-12-30T15:00:00Z
App Command: python todo.py

Results by Category:
✓ Empty/Missing Input: 8/8 cases passed
✗ Invalid IDs: 8/9 cases passed
  Failed: Malformed ID - string input
    Command: python todo.py update abc "text"
    Expected: Non-zero exit code with error message
    Actual: Exit code 0, todo created with ID "abc"
    Risk: Data corruption, unexpected behavior
✓ Boundary Lengths: 4/4 cases passed
✗ Special Characters: 8/9 cases passed
  Failed: Null byte handling
    Command: python todo.py add "Todo\x00null"
    Expected: Validation error or sanitization
    Actual: Application crash (exit code 139)
    Risk: HIGH - crash vulnerability
✓ Duplicates: 3/3 cases passed
✓ State Edge Cases: 5/5 cases passed

Overall: 36/38 edge cases passed (94.7%)
Status: FAILURES DETECTED - 2 ISSUES FOUND

Critical Issues:
1. [HIGH] Application crash on null byte input - security risk
2. [MEDIUM] Invalid ID accepted as valid - data integrity risk
```

## Failure Handling

### Application Crash
- **Detection**: App exits with signal (segfault, abort) or exit code > 128
- **Action**: Capture crash details (signal, exit code, input that caused crash)
- **Severity**: Mark as HIGH or CRITICAL
- **Report**: Include full command and crash type
- **Exit**: Continue testing remaining cases, flag crash in report
- **Next Steps**: Developer must fix crash before release

### Unexpected Acceptance
- **Detection**: Invalid input accepted when validation expected
- **Action**: Document what was accepted and why it's problematic
- **Severity**: Mark as MEDIUM (data integrity risk)
- **Report**: Show input, expected rejection, actual acceptance
- **Exit**: Mark test as failed, continue testing
- **Next Steps**: Add or fix validation logic

### Unclear Error Messages
- **Detection**: Error message doesn't clearly indicate the problem
- **Action**: Document actual vs ideal error message
- **Severity**: Mark as LOW (usability issue)
- **Report**: Suggest improved error message
- **Exit**: Mark as warning, not failure
- **Next Steps**: Consider improving user-facing error messages

### Missing Spec Validation Rules
- **Detection**: `spec_file` provided but validation rules unclear
- **Action**: Test with reasonable defaults (reject empty, validate IDs, limit length)
- **Report**: Note which validations were assumed
- **Exit**: Mark tests as "partial" - needs spec clarification
- **Next Steps**: Update spec with explicit validation rules

### Inconsistent Behavior
- **Detection**: Same edge case handled differently across operations
- **Action**: Document all instances of the inconsistency
- **Severity**: Mark as MEDIUM (design consistency issue)
- **Report**: Show side-by-side comparison
- **Exit**: Mark tests as failed for inconsistency
- **Next Steps**: Establish consistent validation policy across operations

## Notes
- Edge case testing is critical for production readiness
- Crashes on any input are unacceptable and must be fixed
- Clear error messages improve user experience significantly
- Validation should be consistent across all operations
- Security-relevant cases (injection attempts) must fail safely
- Phase 1 may have simpler validation - document limitations
