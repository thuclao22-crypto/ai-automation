# PROJECT CONSTITUTION

> **Single Source of Truth** — This document defines the immutable identity,
> scope, and governing principles of the AI-AUTOMATION-POST project. Every
> future prompt, task, and code change must be evaluated against the rules
> declared here. No other document may override or duplicate this content.

---

## 1. Project Vision

AI-AUTOMATION-POST is a desktop application that automates the end-to-end
workflow of creating, scheduling, and publishing content to multiple social
media platforms. It combines browser automation (Chrome/Selenium) for
platforms that lack public APIs, direct API integration for platforms that
provide them, and an AI-powered capability engine for content generation.
The user interacts through a Tkinter-based graphical interface that exposes
platform management, content editing, scheduling controls, and AI capability
triggers — all from a single window.

The project is written in Python 3 and structured as a modular monolith:
each concern (browser control, social media publishing, UI, scheduling,
capabilities, logging, configuration) lives in its own package under `src/`
and communicates through well-defined interfaces.

## 2. Project Scope

### In Scope

- **Browser Automation** — Driving Chrome via Selenium WebDriver to perform
  actions on social media platforms that do not expose a public API
  (login, navigation, form filling, content submission, media upload).
- **Social Media Publishing** — A platform-agnostic publishing layer that
  abstracts the differences between API-based and browser-based posting.
- **Content Management** — Creating, editing, validating, and templating
  post content (text, images, links) before publication.
- **Scheduler Engine** — Scheduling posts for future publication, managing
  a job queue, and persisting scheduled tasks.
- **Capability Engine** — AI-assisted content generation (caption writing,
  hashtag suggestion, content rewriting) invoked on demand from the UI.
- **User Interface** — A Tkinter desktop UI providing platform configuration,
  content editing, scheduling controls, and capability triggers.
- **Configuration & Secrets** — Environment-based configuration loading and
  secure credential storage.
- **Logging & Monitoring** — Structured application logging for debugging,
  auditing, and operational visibility.

### Out of Scope

- Mobile application development.
- Web-based (browser-hosted) frontend.
- Real-time chat or messaging features.
- Analytics or reporting dashboards beyond basic publish status.
- Third-party service integrations not related to social media posting.
- Cloud deployment or server-side hosting — this is a desktop application.

## 3. Core Principles

1. **Modularity First** — Every feature lives in a dedicated module with a
   single responsibility. Modules communicate through interfaces, not direct
   coupling.
2. **Explicit Over Implicit** — Configuration, dependencies, and data flow
   must be visible and traceable. No hidden magic.
3. **Fail Fast, Recover Gracefully** — Errors are detected early, logged
   with full context, and the system attempts recovery or surfaces the
   failure to the user.
4. **Security by Default** — Credentials are never hardcoded. All secrets
   come from environment variables or encrypted storage.
5. **Documentation-First** — Every module, class, and public function is
   documented before or during implementation. Documentation is the
   contract.
6. **Single Source of Truth** — Governance documents (this file,
   `CODING_RULES.md`, `TOKEN_RULES.md`, `ROADMAP.md`) are the only
   authoritative references. No duplicated governance content exists
   elsewhere.
7. **No Placeholder Code** — Every line of code must serve a real purpose.
   TODOs, stubs, and mock implementations are prohibited in committed code.

## 4. Architecture Philosophy

The project follows a **layered modular monolith** architecture:

```
src/
├── main.py              # Application entry point — composition root
├── config/              # Configuration loading and validation
├── logging_module/      # Structured logging infrastructure
├── browser/             # Chrome/Selenium browser automation
├── core/                # Social media publishing abstraction
├── scheduler/           # Task scheduling and job queue
├── capabilities/        # AI content generation engine
├── ui/                  # Tkinter graphical user interface
└── utils/               # Shared utilities (no business logic)
```

Each layer depends only on the layers below it. The UI layer depends on
core, scheduler, capabilities, and browser. The core layer depends on
browser and config. No layer may depend upward. Cross-layer communication
flows through dependency injection or explicit interface contracts.

## 5. Module Independence Rule

Each module under `src/` must be independently testable and runnable. A
module must not import from a sibling module unless that sibling is a
lower-level layer (per the Architecture Philosophy above). If a module
needs functionality from another module, it must do so through a defined
interface or protocol, not by reaching into internal implementation
details.

**Enforcement:** Any pull request that introduces a circular dependency
between modules is rejected. Any module that cannot be imported in
isolation (without side effects) is rejected.

## 6. Chrome Control Philosophy

Browser automation is the most fragile component of this project. Chrome
control must be:

- **Deterministic** — Every browser action has a clear, predictable outcome.
  No implicit waits or race conditions.
- **Observable** — Every browser action is logged with the URL, selector,
  and outcome.
- **Recoverable** — If the browser crashes or becomes unresponsive, the
  system detects the failure, attempts to restart the browser, and resumes
  or surfaces the error.
- **Isolated** — Browser state (cookies, local storage, profiles) is
  isolated per platform session. No cross-contamination between platform
  sessions.
- **Headless by Default** — The browser runs headless in production.
  Headless mode is disabled only for debugging.

## 7. Capability Engine Philosophy

The AI capability engine generates content suggestions (captions, hashtags,
rewrites) on demand. It must be:

- **Stateless** — Each capability invocation is independent. No session
  state is carried between calls.
- **Configurable** — The AI model, prompt templates, and parameters are
  configurable via environment variables.
- **Observable** — Every capability invocation is logged with the prompt,
  model used, and response metadata.
- **Fallback-Aware** — If the AI service is unavailable, the system falls
  back to a default behavior (e.g., empty suggestion, cached result) and
  logs the fallback.
- **User-Controlled** — The user must explicitly trigger each capability
  invocation. No automatic AI generation without user consent.

## 8. Scheduler Philosophy

The scheduler manages future publication tasks. It must be:

- **Persistent** — Scheduled tasks survive application restarts. Tasks are
  stored in a local database (SQLite).
- **Deterministic** — Tasks execute at their scheduled time. No drift or
  missed executions.
- **Observable** — Every scheduling decision, execution, and failure is
  logged.
- **Recoverable** — If a scheduled task fails, the system retries according
  to a configurable retry policy. After exhausting retries, the task is
  marked as failed and surfaced to the user.
- **Thread-Safe** — The scheduler runs in a background thread and must not
  block the UI thread. All shared state is protected by locks.

## 9. Security Principles

1. **No Hardcoded Secrets** — API keys, tokens, passwords, and connection
   strings must never appear in source code. All secrets are loaded from
   environment variables or encrypted local storage.
2. **Credential Isolation** — Each platform's credentials are stored
   separately and are only accessible to the module that needs them.
3. **Secure Storage** — Credentials at rest are encrypted using the
   operating system's credential store (e.g., Windows Credential Manager,
   macOS Keychain) or a local encrypted file.
4. **Input Validation** — All user input is validated before use. No raw
   user input is passed to browser automation or API calls without
   sanitization.
5. **Audit Logging** — All security-relevant actions (credential access,
   platform login, content publication) are logged with timestamps and
   user context.
6. **Least Privilege** — The application requests only the permissions it
   needs. Browser automation uses a dedicated Chrome profile with no
   access to the user's personal browsing data.

## 10. Development Principles

### 10.1 Documentation-First

Every module, class, and public function must have a docstring before
implementation begins. The docstring defines the contract: what the
function does, its arguments, return values, and exceptions. Code that
lacks documentation is considered incomplete.

### 10.2 Single Source of Truth

The four governance documents at the project root
(`PROJECT_CONSTITUTION.md`, `CODING_RULES.md`, `TOKEN_RULES.md`,
`ROADMAP.md`) are the only authoritative references for project identity,
coding standards, token usage rules, and development roadmap. No other
document may duplicate or override their content. If a conflict arises
between a governance document and any other file, the governance document
wins.

## 11. Definition of Done Philosophy

A task is **Done** when all of the following are true:

1. **Code** — All code is written, passes linting, and has no TODOs,
   placeholders, or dead code.
2. **Tests** — All new logic has unit tests with ≥80% coverage. Integration
   tests cover the end-to-end workflow.
3. **Documentation** — All docstrings are complete. The relevant
   governance document is updated if the task changes project scope or
   architecture.
4. **Build** — The project builds and runs without errors.
5. **Review** — The code has been reviewed against `CODING_RULES.md` and
   `TOKEN_RULES.md`.

A task is **Not Done** if any of these criteria are unmet. Partial
completion is not accepted.
