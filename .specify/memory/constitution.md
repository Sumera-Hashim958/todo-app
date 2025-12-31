<!--
SYNC IMPACT REPORT
==================
Version Change: [INITIAL] → 1.0.0
Bump Rationale: MINOR - Initial constitution ratification for Todo App Phase I

Modified Principles: N/A (initial creation)
Added Sections:
  - Core Principles (7 principles)
  - Phase I Scope Constraints
  - Agent Architecture Rules
  - Quality Assurance Requirements
  - Specification Rules
  - Execution Lifecycle
  - Governance

Removed Sections: N/A

Templates Requiring Updates:
  ✅ spec-template.md - Aligned with specification rules
  ✅ plan-template.md - Constitution Check section present
  ✅ tasks-template.md - Aligned with execution lifecycle
  ⚠️  Command files - May need review for agent orchestration references

Follow-up TODOs: None

Generated: 2025-12-31
-->

# Todo App – Phase I Constitution

## Core Principles

### I. Specification Is the Source of Truth

No code may exist without an approved specification. Specifications override assumptions, preferences, and shortcuts. Every feature MUST have a complete specification in `specs/<feature>/spec.md` before any implementation begins. Specifications define acceptance criteria, edge cases, and error conditions that are non-negotiable for implementation approval.

**Rationale**: Spec-driven development ensures clarity of requirements, prevents scope creep, and provides a measurable definition of "done" for every feature.

### II. Agents, Not Prompts

All meaningful work MUST be executed by agents or sub-agents. Skills are reusable intelligent units, not one-off instructions. Ad-hoc prompts are prohibited for development tasks. Every agent MUST have a single, clearly defined responsibility and one or more reusable skills stored in `.claude/skills/`.

**Rationale**: Agent orchestration enables consistent, repeatable, and traceable development processes. Skills capture reusable intelligence that compounds project value.

### III. Quality Gates Over Speed (NON-NEGOTIABLE)

Failing QA is a hard stop. Partial correctness is considered failure. The QA Agent MUST validate every implementation against acceptance criteria before approval. Quality gate results are:
- **FAIL** → Execution stops immediately
- **CONDITIONAL** → Must be resolved before proceeding
- **PASS** → Proceed to next phase

**Rationale**: Quality defects compound exponentially. Catching issues at quality gates is 10-100x cheaper than fixing them in production.

### IV. Deterministic Behavior

Same input → same output. No randomness. No hidden or uncontrolled state. All operations MUST be deterministic and repeatable. Global mutable state is prohibited unless explicitly scoped and controlled. Randomness (UUIDs, timestamps for business logic) is prohibited.

**Rationale**: Deterministic systems are testable, debuggable, and predictable. Non-determinism makes testing impossible and debugging a nightmare.

### V. Test Execution and Coverage Validation

The QA Agent MUST enforce test execution for every implementation. Tests MUST cover:
- All CRUD operations (Create, Read, Update, Delete)
- Edge cases (empty inputs, invalid IDs, boundary conditions)
- Error scenarios (malformed input, state conflicts)
- Acceptance criteria from specifications

**Rationale**: Automated testing is the only scalable way to verify correctness. Untested code is assumed broken.

### VI. CLI-Only Interface

Phase I allows CLI-based interaction only. All user interaction MUST occur through command-line arguments and text input/output. Text in/out protocol: `stdin/args → stdout, errors → stderr`. No graphical interfaces, web interfaces, or background services are permitted.

**Rationale**: CLI is the simplest interface, easy to test, and forces clear input/output contracts.

### VII. Simplicity and Constraints

Start simple. YAGNI (You Aren't Gonna Need It) principles apply. Phase I is intentionally limited in scope but maximal in quality. Complex solutions require explicit justification via Complexity Tracking in plan.md.

**Rationale**: Simplicity reduces bugs, improves maintainability, and accelerates delivery. Complexity is a liability.

## Phase I Scope Constraints

### ✅ Allowed

- **CLI-based interaction only**: Command-line arguments and text I/O
- **In-memory data storage**: Data structures in Python memory (lists, dicts)
- **Python standard library only**: No external dependencies beyond stdlib
- **Full CRUD operations**: Create, Read, Update, Delete for todos
- **Explicit error handling**: Clear error messages for all failure modes
- **Structured command syntax**: Predictable, documented CLI commands
- **Automated tests**: QA validation via skills (validate-crud-operations, verify-input-edge-cases, run-regression-suite)

### ❌ Prohibited

The following are **HARD VIOLATIONS** resulting in automatic Phase I failure:

- **Databases**: SQL (PostgreSQL, MySQL, SQLite) or NoSQL (MongoDB, Redis)
- **File persistence**: JSON files, CSV files, TXT files, pickle files
- **Web frameworks**: FastAPI, Flask, Django, or any HTTP server
- **UI/Frontend components**: HTML, CSS, JavaScript, React, Vue
- **External APIs or SDKs**: Third-party libraries, API calls, network requests
- **Background services**: Daemons, scheduled tasks, async workers
- **Network calls**: HTTP requests, sockets, webhooks
- **Uncontrolled global mutable state**: Global variables modified by multiple functions without clear ownership

**Enforcement**: Constitution violations detected during QA MUST result in immediate FAIL status.

## Agent Architecture Rules

### Main Agent

The Main Agent orchestrates the entire workflow, delegates work to sub-agents, enforces constitutional compliance, and approves final outputs. The Main Agent is responsible for:
- Interpreting user requirements
- Routing work to appropriate sub-agents
- Validating constitutional compliance before approval
- Generating final deliverables

### Sub-Agents

Each sub-agent MUST have:
- **Single Responsibility**: One clearly defined domain (e.g., QA, domain expertise, CLI implementation)
- **Owned Skills**: One or more reusable skills in `.claude/skills/` that the agent executes
- **Explicit Ownership**: Clear accountability for deliverables and quality

**Defined Sub-Agents for Phase I**:
- `todo-spec-guardian`: Enforces SDD workflow, blocks code without specs
- `todo-domain-expert`: Defines business rules and acceptance criteria for `/sp.specify`
- `python-cli-specialist`: Validates Python CLI implementation patterns
- `qa-agent`: Executes quality assurance (owns validate-crud-operations, verify-input-edge-cases, run-regression-suite)
- `hackathon-judge-reviewer`: Reviews deliverables against hackathon criteria

### Skills (Reusable Intelligence)

Skills MUST be:
- **Stored** in `.claude/skills/` as Markdown files
- **Deterministic**: Same input produces same output
- **Reusable**: Applicable across multiple features (or explicitly scoped to Phase I)
- **Agent-owned**: Each skill has a designated owner agent

Skills MUST include:
- Purpose (what problem it solves)
- When to use (invocation triggers)
- Inputs (required and optional parameters)
- Step-by-step process (execution algorithm)
- Output (expected deliverables)
- Failure handling (error scenarios and recovery)

## Quality Assurance Requirements

### QA Is Not Optional

The QA Agent (`qa-agent`) MUST enforce:
- **Test Execution**: Run all relevant tests for every implementation
- **Coverage Validation**: Verify all acceptance criteria are tested
- **Requirement Traceability**: Map implementation to spec requirements
- **Code Quality Audits**: Validate adherence to standards and patterns
- **Phase I Constraint Compliance**: Block any violations of scope constraints

### Quality Gates

All implementations MUST pass through quality gates:

**FAIL** → Execution stops immediately:
- Any CRITICAL issue (crashes, data corruption, security vulnerabilities)
- Any HIGH issue (acceptance criteria failures, incorrect behavior)
- Phase I constraint violations

**CONDITIONAL** → Must be resolved:
- MEDIUM issues (validation gaps, inconsistencies)
- Documentation gaps affecting usability

**PASS** → Proceed:
- All acceptance criteria met
- No CRITICAL or HIGH issues
- All tests passing
- Constitutional compliance verified

### Test Requirements

For every feature, the QA Agent MUST execute:
1. **CRUD Validation** (`validate-crud-operations` skill)
2. **Edge Case Testing** (`verify-input-edge-cases` skill)
3. **Regression Suite** (`run-regression-suite` skill) before PR/release

## Specification Rules

All features MUST include specifications in `specs/<feature>/spec.md` with:

### Mandatory Sections

- **Clear Description**: What the feature does from user perspective
- **Acceptance Criteria**: Measurable, testable criteria for "done"
- **Edge Cases**: Boundary conditions, error scenarios, invalid inputs
- **Error Conditions**: Expected error messages and handling
- **CLI Commands**: Exact command syntax with examples

### CLI Command Standards

CLI commands MUST be:
- **Explicit**: Clear, unambiguous syntax
- **Predictable**: Consistent patterns across features
- **Fully Documented**: Help text, examples, error messages

Example:
```bash
# Good: Explicit, clear parameters
python todo.py add "Buy groceries"
python todo.py list
python todo.py complete 1

# Bad: Vague, ambiguous
python todo.py do something
```

### Specification Quality

Specifications MUST be:
- **Human-readable**: Clear language accessible to non-technical stakeholders
- **Machine-enforceable**: Acceptance criteria testable by QA Agent
- **Technology-agnostic**: Describe "what" not "how" (implementation details belong in plan.md)

## Execution Lifecycle (Enforced Order)

Phase I development MUST follow this strict sequence:

1. **Constitution** (this document) → Defines laws and constraints
2. **Specification** (`/sp.specify`) → Defines requirements and acceptance criteria
3. **Planning** (`/sp.plan`) → Defines technical approach and architecture
4. **Task Generation** (`/sp.tasks`) → Breaks plan into actionable tasks
5. **Execution** (`/sp.implement`) → Implements tasks sequentially
6. **QA Validation** (automatic via `qa-agent`) → Validates each task completion
7. **Approval** → Task approved only after QA PASS

**No step may be skipped or reordered**. Violations result in automatic rejection.

### Checkpoint Requirements

**After Specification**:
- `todo-spec-guardian` validates spec exists and is complete
- `todo-domain-expert` validates business rules and edge cases

**After Planning**:
- Constitution Check section completed
- No Phase I constraint violations
- ADR created for significant architectural decisions

**After Each Task**:
- `qa-agent` validates implementation against acceptance criteria
- Relevant QA skills executed (CRUD validation, edge case testing)
- PASS status required before proceeding to next task

**Before PR/Release**:
- `run-regression-suite` executes full test suite
- All acceptance criteria met
- No CRITICAL or HIGH issues
- Constitutional compliance verified

## Governance

### Constitutional Supremacy

This constitution supersedes all other practices, preferences, and shortcuts. Any conflict between this constitution and other guidance MUST be resolved in favor of the constitution.

### Amendment Process

Constitution amendments require:
1. **Documentation**: Proposed change with rationale in ADR
2. **Approval**: Explicit user consent
3. **Migration Plan**: Steps to update existing artifacts and code
4. **Version Bump**: Semantic versioning (MAJOR.MINOR.PATCH)

### Compliance Review

All PRs and reviews MUST verify:
- [ ] Specification exists and is approved
- [ ] Implementation matches specification acceptance criteria
- [ ] QA validation passed (no CRITICAL/HIGH issues)
- [ ] Phase I constraints not violated
- [ ] Agent orchestration followed (no ad-hoc prompts)
- [ ] Skills used appropriately and reusably

### Complexity Justification

Any complexity beyond Phase I scope MUST be justified in the `Complexity Tracking` section of plan.md, documenting:
- What constraint is violated
- Why it's needed for this feature
- What simpler alternative was rejected and why

Unjustified complexity results in FAIL status.

### Enforcement

Constitutional violations are detected by:
- `todo-spec-guardian`: Blocks code without specs, enforces SDD workflow
- `qa-agent`: Validates Phase I constraints, runs quality gates
- `python-cli-specialist`: Ensures CLI-only interface
- Main Agent: Final constitutional compliance check before approval

**Penalty for Violation**: Automatic FAIL status, execution halted until resolved.

---

**Version**: 1.0.0 | **Ratified**: 2025-12-31 | **Last Amended**: 2025-12-31
