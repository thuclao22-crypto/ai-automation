# CODING RULES

> **Single Source of Truth** — This document defines the coding standards
> and conventions for the AI-AUTOMATION-POST project. All code must comply.
> No other document may override or duplicate this content.

---

## 1. Naming Conventions

### 1.1 Folders / Packages

- Package names are lowercase, no separators (e.g., `browser`, `core`,
  `scheduler`, `capabilities`, `ui`, `config`, `logging_module`, `utils`).
- Each package contains an `__init__.py` that exports its public API.
- Package names reflect a single responsibility.

### 1.2 Classes

- Class names use **PascalCase** (e.g., `BrowserAutomator`,
  `SocialMediaPublisher`, `MainWindow`).
- Class names are nouns or noun phrases describing the entity.
- Abstract base classes are prefixed with `Base` (e.g., `BasePlatformAdapter`).

### 1.3 Functions / Methods

- Function and method names use **snake_case** (e.g., `start_browser`,
  `publish_content`, `extract_content`).
- Function names are verbs or verb phrases describing the action.
- Private methods are prefixed with a single underscore (e.g.,
  `_create_widgets`).
- Public methods have no underscore prefix.

### 1.4 Files

- File names use **snake_case** (e.g., `automation.py`, `social_media.py`,
  `main_window.py`).
- File names match the primary class or concept they contain.
- `__init__.py` files are empty except for public API exports.

### 1.5 Variables

- Variable names use **snake_case** (e.g., `platform_name`, `api_config`,
  `headless_mode`).
- Constants use **UPPER_SNAKE_CASE** (e.g., `MAX_RETRIES`,
  `DEFAULT_TIMEOUT_SECONDS`).
- Boolean variables are prefixed with `is_`, `has_`, or `can_` where
  appropriate (e.g., `is_headless`, `has_credentials`).

## 2. SOLID Principles

### 2.1 Single Responsibility Principle (SRP)

Each class has one reason to change. A class must not mix concerns (e.g.,
a class must not both manage browser state and format log messages).

### 2.2 Open/Closed Principle (OCP)

Classes are open for extension but closed for modification. New platform
adapters, for example, are added by implementing an interface, not by
modifying existing adapter code.

### 2.3 Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types. Any subclass instance
must be usable wherever the base class is expected without altering
correctness.

### 2.4 Interface Segregation Principle (ISP)

Interfaces are small and focused. A class must not be forced to implement
methods it does not use. Platform adapters, for example, implement only
the methods relevant to their platform.

### 2.5 Dependency Inversion Principle (DIP)

High-level modules depend on abstractions, not concrete implementations.
Dependencies are injected, not instantiated internally. The composition
root (`main.py`) is the only place where concrete implementations are
wired together.

## 3. Typing Requirements

- All function signatures must include **type hints** for parameters and
  return values.
- All class attributes must be annotated with their types.
- Use `typing` module constructs (`Optional`, `List`, `Dict`, `Tuple`,
  `Protocol`) where appropriate.
- Use `from __future__ import annotations` at the top of every module to
  enable postponed evaluation of annotations.
- Type checkers (mypy or pyright) must pass with no errors.

## 4. Docstring Requirements

- Every module, class, and public function/method must have a docstring.
- Docstrings use **Google style** format.
- Module docstrings describe the module's purpose in one sentence.
- Class docstrings describe the class's responsibility and key behaviors.
- Function docstrings include:
  - A one-line summary of the function's purpose.
  - An `Args:` section listing each parameter with its type and purpose.
  - A `Returns:` section describing the return value and type.
  - A `Raises:` section listing all exceptions the function may raise.
- Private methods (prefixed with `_`) should also have docstrings, but
  they may be brief.

## 5. Error Handling Rules

- **Catch specific exceptions** — Never use bare `except:` or
  `except Exception:`. Catch the most specific exception type possible.
- **Log before re-raising** — If an exception is caught and re-raised, log
  the context before re-raising.
- **Fail fast** — Validate inputs at the top of each public function. Raise
  `ValueError` or `TypeError` for invalid inputs immediately.
- **Wrap external calls** — All calls to external systems (browser, API,
  database) must be wrapped in try/except with appropriate retry or
  fallback logic.
- **Never swallow errors** — If an exception is caught, it must either be
  handled (with a clear recovery path) or re-raised. Silent failure is
  prohibited.
- **Custom exceptions** — Define custom exception classes for domain-specific
  errors (e.g., `BrowserError`, `PublishError`, `SchedulerError`).

## 6. Logging Rules

- Use the standard `logging` module. Never use `print()`.
- Every module gets its own logger: `logger = logging.getLogger(__name__)`.
- Log levels:
  - `DEBUG` — Detailed diagnostic information, useful for debugging.
  - `INFO` — Confirmation that things are working as expected.
  - `WARNING` — Something unexpected happened, but the system continues.
  - `ERROR` — A serious problem; the system could not perform a function.
  - `CRITICAL` — A very serious error; the system may be unable to continue.
- Log messages are structured: include relevant context (platform name,
  URL, selector, task ID) as key-value pairs or formatted strings.
- Never log secrets, tokens, passwords, or full API responses.
- Log at `INFO` level for user-facing actions (publish, schedule, login).
- Log at `DEBUG` level for internal state changes and detailed diagnostics.

## 7. Import Rules

- Imports are grouped in three blocks, separated by blank lines:
  1. **Standard library imports** (e.g., `os`, `sys`, `logging`, `sqlite3`).
  2. **Third-party imports** (e.g., `selenium`, `tkinter`).
  3. **Local application imports** (e.g., `from src.core.social_media import
SocialMediaPublisher`).
- Within each block, imports are sorted alphabetically.
- Use absolute imports, not relative imports (e.g.,
  `from src.browser.automation import BrowserAutomator`, not
  `from ..browser.automation import BrowserAutomator`).
- No wildcard imports (`from module import *`).
- Each import is on its own line.

## 8. Dependency Rules

- The project uses a `requirements.txt` file at the project root for
  dependency management.
- Dependencies are pinned to specific versions.
- New dependencies must be justified: the dependency must solve a problem
  that cannot be reasonably solved with the standard library or an existing
  dependency.
- No dependency is added without updating `requirements.txt` and
  `requirements-dev.txt` (for development-only dependencies).
- The `src/utils/` package contains only pure-Python utilities with no
  external dependencies.

## 9. Code Reuse Rules

- **DRY** — Do not duplicate logic. If the same code appears in two places,
  extract it into a shared function or class.
- **Extract to utils** — Pure utility functions (string formatting, date
  parsing, validation helpers) live in `src/utils/`.
- **Extract to base classes** — Shared behavior across similar classes
  (e.g., platform adapters) is extracted into a base class or mixin.
- **No copy-paste** — Copying code between modules is prohibited. If code
  is copied, it must be refactored into a shared location.

## 10. Comment Rules

- Comments explain **why**, not **what**. Code should be self-documenting.
- Comments are written in English.
- Inline comments are used sparingly and only when the code is not
  self-explanatory.
- Block comments (lines starting with `#`) are used to separate logical
  sections within a function or module.
- Comments must not duplicate information already in docstrings.
- Remove comments that are no longer accurate. Stale comments are worse
  than no comments.

## 11. Prohibited Patterns

The following patterns are strictly prohibited in committed code:

### 11.1 No TODO

- No `TODO`, `FIXME`, `HACK`, `XXX`, or `NOTE` comments.
- If work is incomplete, it is not committed. Code must be complete before
  it is written.

### 11.2 No Placeholder

- No placeholder functions that return `None`, `pass`, or dummy values.
- No `raise NotImplementedError` in production code.
- Every function must have a real implementation.

### 11.3 No Dead Code

- No unused imports, variables, or functions.
- No unreachable code.
- No commented-out code blocks.
- Linters (flake8, ruff) must pass with zero warnings.

### 11.4 No Magic Numbers

- All numeric literals must be named constants with descriptive names.
- Constants are defined at the module level or in a dedicated constants
  module.
- Example: `DEFAULT_TIMEOUT_SECONDS = 30` instead of using `30` directly.

### 11.5 No Duplicate Implementations

- No two functions that do the same thing.
- If similar logic is needed in multiple places, extract a shared function.
- Platform-specific adapters may have similar structure, but shared logic
  must be in the base class.

### 11.6 No Mock Code

- No mock implementations in production code.
- Testing utilities (mocks, fakes) live only in the `tests/` directory.
- Production code must use real implementations.
