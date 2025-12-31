---
description: "Task list for Todo CLI Core feature implementation"
---

# Tasks: Todo CLI Core

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (complete), spec.md (complete), data-model.md (complete), contracts/ (complete)

**Tests**: Not explicitly requested in specification - QA agent will validate via black-box testing skills

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `todo.py`, `models/`, `services/`, `validators/`, `utils/` at repository root
- No tests/ directory - QA agent performs black-box testing via CLI

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Create project structure and basic infrastructure

- [x] T001 Create project directory structure (models/, services/, validators/, utils/)
- [x] T002 [P] Create empty __init__.py files in models/, services/, validators/, utils/ directories
- [x] T003 Create main entry point file todo.py with basic imports

**Checkpoint**: Project structure exists, ready for foundational components

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement input validation module in validators/input_validator.py with validate_text() function (empty/whitespace check, length limit 200 chars, control char detection)
- [x] T005 [P] Implement validate_id() function in validators/input_validator.py (positive integer validation, error handling)
- [x] T006 [P] Implement output formatter module in utils/formatter.py with format_todo() function (ID, status indicator, text)
- [x] T007 [P] Implement error_exit() function in utils/formatter.py (stderr output, exit codes)
- [x] T008 [P] Implement success_message() function in utils/formatter.py (stdout output)
- [x] T009 Initialize global storage in todo.py (todos = [], next_id = 1)

**Checkpoint**: Foundation ready - validation, formatting, and storage initialized

---

## Phase 3: User Story 1 - Add New Todo Items (Priority: P1) 🎯 MVP

**Goal**: Enable users to create new todo items via `python todo.py add "text"`

**Independent Test**: Run add command with various inputs, verify todos are stored and retrievable via list command

### Implementation for User Story 1

- [x] T010 [P] [US1] Implement add_todo() function in services/todo_service.py (validate text, assign ID, create todo dict, append to list, increment next_id, return todo)
- [x] T011 [P] [US1] Implement find_todo_by_id() helper function in services/todo_service.py (linear search through todos list, return todo or None)
- [x] T012 [US1] Implement add command handler in todo.py (parse args, call validate_text, call add_todo, print success message, handle errors)
- [x] T013 [US1] Implement basic command routing in todo.py (check sys.argv for command, route to add handler, handle unknown commands)
- [x] T014 [US1] Add help text support in todo.py (display usage when no args or 'help' command, include add command example)

**Checkpoint**: User Story 1 complete - users can add todos and see confirmation

---

## Phase 4: User Story 2 - View All Todo Items (Priority: P1) 🎯 MVP

**Goal**: Enable users to view all todo items via `python todo.py list`

**Independent Test**: Add multiple todos, run list command, verify all appear with IDs and status

### Implementation for User Story 2

- [x] T015 [US2] Implement get_all_todos() function in services/todo_service.py (return copy of todos list)
- [x] T016 [US2] Implement format_todo_list() function in utils/formatter.py (iterate todos, format each with ID/status/text, handle empty list)
- [x] T017 [US2] Implement list command handler in todo.py (call get_all_todos, format output, handle empty list with "No todos found" message)
- [x] T018 [US2] Add list command to command routing in todo.py (route 'list' to list handler)
- [x] T019 [US2] Update help text in todo.py to include list command example

**Checkpoint**: User Stories 1 AND 2 complete - users can add and view todos (MVP functional)

---

## Phase 5: User Story 3 - Mark Todo Items as Complete (Priority: P2)

**Goal**: Enable users to mark todos complete via `python todo.py complete <id>`

**Independent Test**: Add todos, mark specific ID complete, verify status change in list output

### Implementation for User Story 3

- [x] T020 [US3] Implement complete_todo() function in services/todo_service.py (validate ID, find todo, set completed=True, return todo, handle not found)
- [x] T021 [US3] Implement complete command handler in todo.py (parse ID arg, validate ID, call complete_todo, print success message, handle errors)
- [x] T022 [US3] Add complete command to command routing in todo.py (route 'complete' to complete handler)
- [x] T023 [US3] Update help text in todo.py to include complete command example
- [x] T024 [US3] Update format_todo() in utils/formatter.py to include visual distinction for completed todos ([✓] vs [ ])

**Checkpoint**: User Story 3 complete - users can mark todos as complete with visual feedback

---

## Phase 6: User Story 4 - Update Todo Item Text (Priority: P3)

**Goal**: Enable users to update todo text via `python todo.py update <id> "new text"`

**Independent Test**: Add todo, update its text, verify new text appears in list

### Implementation for User Story 4

- [x] T025 [US4] Implement update_todo() function in services/todo_service.py (validate ID, find todo, validate new text, update text field, return todo, handle not found)
- [x] T026 [US4] Implement update command handler in todo.py (parse ID and text args, validate both, call update_todo, print success message, handle errors)
- [x] T027 [US4] Add update command to command routing in todo.py (route 'update' to update handler)
- [x] T028 [US4] Update help text in todo.py to include update command example

**Checkpoint**: User Story 4 complete - users can edit todo text

---

## Phase 7: User Story 5 - Delete Todo Items (Priority: P3)

**Goal**: Enable users to delete todos via `python todo.py delete <id>`

**Independent Test**: Add todos, delete specific ID, verify it no longer appears in list

### Implementation for User Story 5

- [x] T029 [US5] Implement delete_todo() function in services/todo_service.py (validate ID, find todo, remove from list, return deleted todo, handle not found)
- [x] T030 [US5] Implement delete command handler in todo.py (parse ID arg, validate ID, call delete_todo, print success message, handle errors)
- [x] T031 [US5] Add delete command to command routing in todo.py (route 'delete' to delete handler)
- [x] T032 [US5] Update help text in todo.py to include delete command example

**Checkpoint**: User Story 5 complete - all CRUD operations functional

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements affecting multiple user stories

- [x] T033 [P] Add UTF-8 encoding configuration in todo.py (sys.stdout.reconfigure if needed for cross-platform emoji support)
- [x] T034 [P] Implement argument count validation for all commands in todo.py (check sys.argv length, display usage on insufficient args)
- [x] T035 [P] Add Phase I data loss warning to help text in todo.py ("Note: This is an in-memory application. All data is lost when the program exits.")
- [x] T036 Review all error messages for clarity and consistency across all command handlers
- [x] T037 Verify exit code usage (0 for success, 1 for errors, 2 for usage errors) in all command handlers
- [x] T038 Final validation against contracts/cli-commands.md (verify all command contracts implemented correctly)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (Add): Can start after Foundational
  - US2 (List): Depends on US1 (needs todos to display)
  - US3 (Complete): Depends on US1 and US2 (needs add/list to test completion)
  - US4 (Update): Depends on US1 and US2 (needs add/list to test updates)
  - US5 (Delete): Depends on US1 and US2 (needs add/list to test deletion)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories - can start after Foundational
- **User Story 2 (P1)**: Depends on US1 (needs add_todo function to create test data)
- **User Story 3 (P2)**: Depends on US1 and US2 (needs ability to add and list todos)
- **User Story 4 (P3)**: Depends on US1 and US2 (needs ability to add and list todos)
- **User Story 5 (P3)**: Depends on US1 and US2 (needs ability to add and list todos)

### Within Each Phase

- Setup: All tasks [P] can run in parallel
- Foundational: Tasks T004-T008 marked [P] can run in parallel, T009 should be last
- User Stories: Tasks within each story should be done sequentially (services first, then handlers, then routing)
- Polish: Tasks marked [P] can run in parallel

### Parallel Opportunities

- **Setup Phase**: T002 can run in parallel (creating __init__ files in different directories)
- **Foundational Phase**: T004-T008 can all run in parallel (different files, independent functions)
- **User Story Phases**: Tasks within same story typically sequential, but different stories could be worked on in parallel after dependencies met
- **Polish Phase**: T033-T035 can run in parallel (different concerns, different code sections)

---

## Implementation Strategy

### MVP First (User Stories 1 & 2 Only)

This is the recommended starting point for maximum value with minimum effort:

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T009) → Foundation ready ✅
3. Complete Phase 3: User Story 1 - Add (T010-T014) → Can add todos ✅
4. Complete Phase 4: User Story 2 - List (T015-T019) → Can view todos ✅
5. **STOP and VALIDATE**: Test add/list workflow end-to-end
6. Deploy/demo MVP (basic todo capture and viewing)

**MVP Validation**:
```bash
# Add some todos
python todo.py add "Buy groceries"
python todo.py add "Write report"

# List todos
python todo.py list
# Should show:
#   1  [ ] Buy groceries
#   2  [ ] Write report
```

### Incremental Delivery (Add User Stories One at a Time)

After MVP validation passes:

1. Add User Story 3 (Complete) → Test independently → Deploy/Demo
2. Add User Story 4 (Update) → Test independently → Deploy/Demo
3. Add User Story 5 (Delete) → Test independently → Deploy/Demo
4. Complete Polish phase → Final validation → Release

Each user story adds value without breaking previous functionality.

### Full Feature Implementation

For complete feature delivery:

1. Phases 1-2: Foundation (T001-T009)
2. Phase 3: US1 Add (T010-T014)
3. Phase 4: US2 List (T015-T019)
4. Phase 5: US3 Complete (T020-T024)
5. Phase 6: US4 Update (T025-T028)
6. Phase 7: US5 Delete (T029-T032)
7. Phase 8: Polish (T033-T038)
8. QA Validation: Run qa-agent regression suite
9. Ready for production

---

## Notes

- [P] tasks within a phase can be started simultaneously (different files, no dependencies)
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- QA validation happens after each phase via qa-agent skills (validate-crud-operations, verify-input-edge-cases)
- Commit after completing each user story phase
- Stop at any checkpoint to validate story independently
- MVP = User Stories 1 + 2 (add and list functionality)
- Full feature = All 5 user stories + polish

---

## QA Validation Checkpoints

**After Each User Story Phase**:
- Run relevant qa-agent validation (e.g., after US1: test add command edge cases)
- Verify acceptance scenarios from spec.md
- Test error handling for that story's operations

**Before Final Release** (after Phase 8):
- Run full regression suite: `qa-agent run-regression-suite`
- Validate all 19 functional requirements
- Verify all 8 success criteria
- Test all edge cases from spec.md
- Constitutional compliance check (CLI-only, in-memory, stdlib only)

---

## Total Task Count: 38 tasks

**Breakdown by Phase**:
- Phase 1 (Setup): 3 tasks
- Phase 2 (Foundational): 6 tasks
- Phase 3 (US1 - Add): 5 tasks
- Phase 4 (US2 - List): 5 tasks
- Phase 5 (US3 - Complete): 5 tasks
- Phase 6 (US4 - Update): 4 tasks
- Phase 7 (US5 - Delete): 4 tasks
- Phase 8 (Polish): 6 tasks

**MVP Scope**: 19 tasks (Phases 1-4)
**Full Feature**: 38 tasks (All phases)
