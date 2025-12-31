---
name: run-regression-suite
owner: qa-agent
project: todo-app-phase-1
version: 1.0.0
---

# Run Regression Suite

## Purpose
Execute a comprehensive regression test suite combining CRUD validation, edge case verification, and acceptance criteria checks to ensure new changes haven't broken existing functionality.

## When to Use
- Before creating a pull request
- After refactoring or code changes
- Before tagging a release
- After fixing bugs to confirm no new issues introduced
- When multiple features have been implemented and need validation
- Daily as part of CI/CD pipeline (when available)

## Inputs
**Required:**
- `app_command`: The CLI command to invoke the todo app (e.g., `python todo.py`, `./todo`)

**Optional:**
- `spec_file`: Path to spec.md for acceptance criteria validation
- `baseline_report`: Path to previous regression report for comparison
- `test_suite`: Specific suite to run (crud | edge | acceptance | all) [default: all]
- `fail_fast`: Stop on first failure (default: false)
- `output_format`: Report format (markdown | json | text) [default: markdown]

## Step-by-Step Process

### Step 1: Pre-Flight Checks
1. Verify `app_command` is valid and app is accessible
2. Execute: `{app_command} --version` or `{app_command} --help`
3. Verify successful response (exit code 0)
4. If `spec_file` provided, verify file exists and is readable
5. If `baseline_report` provided, load for comparison
6. Create timestamped test session directory for artifacts

### Step 2: Run CRUD Operations Test Suite
1. Invoke `validate-crud-operations` skill with parameters:
   - `operation`: "all"
   - `app_command`: {app_command}
   - `verbose`: false
2. Capture test results and metrics
3. Parse output for pass/fail counts
4. Store CRUD test report in session directory
5. If `fail_fast` enabled and failures detected, skip to Step 8
6. Otherwise, continue to next test suite

### Step 3: Run Edge Cases Test Suite
1. Invoke `verify-input-edge-cases` skill with parameters:
   - `app_command`: {app_command}
   - `operation_filter`: "all"
   - `spec_file`: {spec_file} (if provided)
   - `verbose`: false
2. Capture test results and metrics
3. Parse output for pass/fail counts and severity levels
4. Store edge case test report in session directory
5. If `fail_fast` enabled and critical failures detected, skip to Step 8
6. Otherwise, continue to next test suite

### Step 4: Run Acceptance Criteria Tests (if spec available)
1. If `spec_file` not provided, skip this step
2. Read `spec_file` and extract all acceptance criteria
3. For each criterion:
   - Parse criterion into testable assertion
   - Map to corresponding CLI command(s)
   - Execute command and verify output matches criterion
   - Record pass/fail with criterion reference
4. Generate acceptance criteria coverage report
5. Store report in session directory

### Step 5: Run Feature Workflow Tests
1. Test common user workflows end-to-end:

   **Workflow 1: Basic Todo Lifecycle**
   - Add new todo
   - List todos to verify
   - Complete the todo
   - List again to verify completion
   - Delete the todo
   - Verify deletion

   **Workflow 2: Multiple Todos Management**
   - Add 5 different todos
   - List all (verify count is 5)
   - Complete 2 todos
   - List and verify 2 marked complete, 3 active
   - Delete 1 completed todo
   - List and verify correct state
   - Clear remaining todos

   **Workflow 3: Error Recovery**
   - Attempt invalid operation (e.g., complete non-existent ID)
   - Verify error, app still functional
   - Perform valid operation
   - Verify success

2. Record workflow results (each workflow pass/fail)
3. Store workflow report in session directory

### Step 6: Performance Baseline Checks (Phase 1 - Basic)
1. Measure response time for common operations:
   - Add todo: execute 10 times, calculate average time
   - List todos: with 0, 10, 50 items (if supported)
   - Complete todo: execute 10 times, average time
2. Verify no operation takes >5 seconds (Phase 1 threshold)
3. If `baseline_report` exists, compare against previous times
4. Flag any operation that's >50% slower than baseline
5. Store performance metrics in session directory

### Step 7: Aggregate Results
1. Collect all test suite results:
   - CRUD operations: X/Y passed
   - Edge cases: X/Y passed (note critical failures)
   - Acceptance criteria: X/Y passed (if spec available)
   - Workflows: X/Y passed
   - Performance: within/exceeding thresholds
2. Calculate overall pass percentage
3. Identify all failures and categorize by severity:
   - CRITICAL: crashes, data corruption, security issues
   - HIGH: functional failures, incorrect behavior
   - MEDIUM: validation gaps, inconsistencies
   - LOW: usability issues, unclear errors
4. If `baseline_report` exists, generate delta report:
   - New failures introduced
   - Previously failing tests now passing
   - Performance regressions
5. Determine overall regression status:
   - PASSED: All tests passed, no critical issues
   - PASSED WITH WARNINGS: Minor issues only
   - FAILED: Critical or high-severity failures
   - DEGRADED: Performance regressions detected

### Step 8: Generate Comprehensive Report
1. Create regression report in specified `output_format`
2. Include:
   - Executive summary (overall status, pass rate)
   - Test suite breakdown
   - All failures with details
   - Performance metrics
   - Baseline comparison (if available)
   - Recommendations for fixes
   - Timestamp and environment info
3. Save report to session directory
4. Output report path and summary to stdout

## Output

### Success Output Format (Markdown)
```markdown
# Regression Test Report
**Status**: ✅ PASSED
**Timestamp**: 2025-12-30T16:00:00Z
**App**: `python todo.py`
**Session**: regression-2025-12-30-160000

## Executive Summary
All regression tests passed successfully. No issues detected.

## Test Suite Results

### CRUD Operations
- **Status**: ✅ PASSED
- **Tests**: 19/19 passed (100%)
- **Details**: All create, read, update, complete, and delete operations functioning correctly.

### Edge Cases
- **Status**: ✅ PASSED
- **Tests**: 38/38 passed (100%)
- **Details**: All boundary conditions, invalid inputs, and error cases handled appropriately.

### Acceptance Criteria
- **Status**: ✅ PASSED
- **Coverage**: 12/12 criteria met (100%)
- **Details**: All acceptance criteria from spec.md validated successfully.

### Workflow Tests
- **Status**: ✅ PASSED
- **Workflows**: 3/3 passed (100%)
- **Details**: All user workflows completed successfully end-to-end.

### Performance
- **Status**: ✅ WITHIN THRESHOLDS
- **Add**: avg 0.15s (baseline: 0.14s, +7%)
- **List**: avg 0.08s (baseline: 0.09s, -11%)
- **Complete**: avg 0.12s (baseline: 0.13s, -8%)

## Overall Metrics
- **Total Tests**: 72/72 passed
- **Pass Rate**: 100%
- **Critical Issues**: 0
- **High Issues**: 0
- **Medium Issues**: 0
- **Low Issues**: 0

## Recommendations
✅ Ready for pull request/release. No action required.

---
*Report saved to: ./test-sessions/regression-2025-12-30-160000/report.md*
```

### Failure Output Format (Markdown)
```markdown
# Regression Test Report
**Status**: ❌ FAILED
**Timestamp**: 2025-12-30T16:00:00Z
**App**: `python todo.py`
**Session**: regression-2025-12-30-160000

## Executive Summary
Regression tests failed with 3 issues detected (1 critical, 2 high). **DO NOT MERGE/RELEASE** until issues are resolved.

## Test Suite Results

### CRUD Operations
- **Status**: ✅ PASSED
- **Tests**: 19/19 passed (100%)

### Edge Cases
- **Status**: ❌ FAILED
- **Tests**: 36/38 passed (94.7%)
- **Critical Issues**: 1
- **High Issues**: 1

**Failures:**
1. **[CRITICAL]** Application crash on null byte input
   - Command: `python todo.py add "Todo\x00null"`
   - Expected: Validation error or sanitization
   - Actual: Segmentation fault (exit code 139)
   - **Impact**: Security vulnerability, DoS risk

2. **[HIGH]** Invalid ID accepted
   - Command: `python todo.py update abc "text"`
   - Expected: Validation error
   - Actual: Todo created with ID "abc"
   - **Impact**: Data integrity risk

### Acceptance Criteria
- **Status**: ❌ FAILED
- **Coverage**: 11/12 criteria met (91.7%)

**Failures:**
1. **[HIGH]** Criterion AC-05: "Completed todos should be visually distinct in list"
   - Expected: Completed todos marked with indicator (✓, [DONE], etc.)
   - Actual: No visual distinction in output
   - **Impact**: User experience degradation

### Workflow Tests
- **Status**: ✅ PASSED
- **Workflows**: 3/3 passed (100%)

### Performance
- **Status**: ⚠️ DEGRADED
- **Add**: avg 1.25s (baseline: 0.14s, **+793%** ⚠️)
- **List**: avg 0.09s (baseline: 0.09s, ±0%)
- **Complete**: avg 0.13s (baseline: 0.13s, ±0%)
- **Warning**: Add operation significantly slower than baseline

## Baseline Comparison
Comparing to baseline: ./reports/regression-2025-12-29.md

**New Failures Introduced**:
- [CRITICAL] Null byte crash (not present in baseline)
- [HIGH] Invalid ID acceptance (not present in baseline)

**Performance Regressions**:
- Add operation: 0.14s → 1.25s (+793%)

## Overall Metrics
- **Total Tests**: 69/72 passed
- **Pass Rate**: 95.8%
- **Critical Issues**: 1 🚨
- **High Issues**: 2 ⚠️
- **Medium Issues**: 0
- **Low Issues**: 0

## Recommendations

### Immediate Actions Required
1. **[CRITICAL]** Fix null byte crash before any release
   - Add input sanitization to remove/reject null bytes
   - Add test case to prevent regression

2. **[HIGH]** Implement ID validation
   - Reject non-numeric IDs
   - Add validation layer before processing

3. **[HIGH]** Add visual distinction for completed todos
   - Implement per acceptance criterion AC-05
   - Add formatting to list output

4. **Investigate** Add operation performance regression
   - Profile add operation to identify bottleneck
   - Verify no unintended I/O or delays introduced

### Re-test After Fixes
Run regression suite again after implementing fixes to confirm resolution.

---
*Report saved to: ./test-sessions/regression-2025-12-30-160000/report.md*
```

## Failure Handling

### Skill Invocation Failure
- **Detection**: `validate-crud-operations` or `verify-input-edge-cases` skill fails to execute
- **Action**: Log error message from skill invocation
- **Report**: Mark affected test suite as "ERROR - could not execute"
- **Exit**: Continue with remaining suites if possible
- **Next Steps**: Verify skill files exist and are properly configured

### App Not Responding
- **Detection**: App command times out (>30s) or hangs
- **Action**: Kill process, mark as critical failure
- **Report**: "Application timeout or hang detected during regression"
- **Severity**: CRITICAL
- **Exit**: Abort regression suite immediately
- **Next Steps**: Investigate infinite loop or blocking I/O issue

### Test Environment Corruption
- **Detection**: Inconsistent results across test runs (flaky tests)
- **Action**: Re-run failed tests up to 3 times
- **Report**: Mark as "UNSTABLE" if results vary
- **Exit**: Flag as medium severity issue
- **Next Steps**: Investigate test isolation or state pollution

### Missing Baseline Report
- **Detection**: `baseline_report` path provided but file not found
- **Action**: Log warning, proceed without comparison
- **Report**: Note "No baseline comparison available"
- **Exit**: Continue regression without delta analysis
- **Next Steps**: User verifies baseline path or accepts no comparison

### Spec File Parsing Error
- **Detection**: `spec_file` provided but cannot parse acceptance criteria
- **Action**: Log warning with parse error details
- **Report**: Mark acceptance tests as "SKIPPED - parse error"
- **Exit**: Continue with other test suites
- **Next Steps**: Verify spec file format matches expected structure

### Critical Failure in Fail-Fast Mode
- **Detection**: `fail_fast` enabled and critical/high severity failure occurs
- **Action**: Stop test execution immediately
- **Report**: Generate partial report with results up to failure point
- **Exit**: Return failure status immediately
- **Next Steps**: Developer fixes critical issue before full regression

## Notes
- Regression suite is the gatekeeper for releases - must pass before merge/deploy
- Critical failures block releases unconditionally
- Performance baselines help detect unintended regressions early
- Comprehensive reporting enables fast diagnosis and fixes
- Test sessions are isolated to allow parallel execution and debugging
- Phase 1 has simpler performance requirements - will evolve in later phases
- Skill composition (invoking other skills) reduces duplication and ensures consistency
