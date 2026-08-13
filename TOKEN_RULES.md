# TOKEN RULES

> **Single Source of Truth** — This document defines the operational rules
> for how the AI agent interacts with the project workspace. These rules
> exist to minimize token consumption, prevent scope creep, and ensure
> deterministic, reproducible progress. No other document may override or
> duplicate this content.

---

## 1. Scope Isolation Rule

The AI agent must operate **only** within the scope defined by the current
task. The task specifies which files, directories, and modules are in scope.
The agent must not read, write, or modify any file outside the declared
scope.

**Enforcement:** Before any file operation, the agent verifies that the
target file is within the task's declared scope. If a file is outside
scope, the agent does not touch it and reports the violation.

## 2. Read-Only-Required-Files Rule

Governance documents (`PROJECT_CONSTITUTION.md`, `CODING_RULES.md`,
`TOKEN_RULES.md`, `ROADMAP.md`) and configuration files (`.gitignore`,
`requirements.txt`, `requirements-dev.txt`) are **read-only** during
implementation tasks. The agent may read them for reference but must not
modify them unless the task explicitly requires it.

**Exception:** The current task (P0-T01) explicitly requires writing to
these four governance documents. Outside of this task, they are read-only.

## 3. Never-Scan-Whole-Project Rule

The AI agent must never scan the entire project directory tree in a single
operation. Instead, the agent must:

- Use targeted `list_files` calls on specific directories.
- Use targeted `search_files` calls with specific regex patterns.
- Use `read_file` with specific line ranges, not entire large files.
- Never use `find`, `grep -r`, or equivalent recursive scans across the
  entire project root.

**Rationale:** Scanning the whole project consumes excessive tokens and
introduces irrelevant context that can lead to scope drift.

## 4. Never-Refactor-Completed-Modules Rule

Once a module is marked as **Done** in `ROADMAP.md`, the AI agent must not
refactor, restructure, or modify it unless a new task explicitly requires
changes to that module.

**Enforcement:** The agent checks `ROADMAP.md` before modifying any module.
If the module's phase is marked "Done", the agent does not modify it and
reports the violation.

## 5. One-Prompt-One-Deliverable Rule

Each task prompt produces exactly one deliverable. The agent must not
expand scope beyond what is explicitly requested. If the agent identifies
related work that is not in scope, it notes it in the completion report but
does not execute it.

**Enforcement:** The agent's completion report lists only the files that
were created or modified as part of the declared deliverable. Any
out-of-scope work is documented as a recommendation, not executed.

## 6. Stop-Immediately-After-Task Rule

After completing the declared task, the AI agent must stop immediately.
The agent must not:

- Continue to the next phase or task without explicit instruction.
- Refactor or improve code beyond the task scope.
- Add features, tests, or documentation not requested by the task.
- Run additional commands or make additional changes.

**Enforcement:** The agent uses the `attempt_completion` tool to signal
task completion. After completion, the agent does not take further action
unless the user provides a new task.

## 7. Never-Regenerate-Existing-Code Rule

The AI agent must never regenerate, rewrite, or overwrite existing code
that is not part of the current task's declared scope. If a file already
contains content, the agent must use targeted edits (`apply_diff`) to make
specific changes, not full rewrites.

**Exception:** When a task explicitly requires creating a new file or
completely rewriting a file (e.g., the governance documents in P0-T01),
the agent may use `write_to_file`. For all other files, targeted edits
are required.

**Enforcement:** The agent checks whether a file is empty or contains
existing content before writing. If the file has content and the task does
not explicitly require a full rewrite, the agent uses `apply_diff` instead.
