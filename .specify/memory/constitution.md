# Evolution of Todo Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### I. Spec-Driven Development (Mandatory)
<!-- Example: I. Library-First -->
All development must follow the Spec-Driven Development methodology: Constitution → Specs → Plan → Tasks → Implement. No agent may write code without approved specs and tasks.
<!-- Example: Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries -->

### II. Agent Behavior Rules
<!-- Example: II. CLI Interface -->
Agents must follow strict behavior rules: No manual coding by humans, no feature invention, no deviation from approved specifications, and refinement must occur at spec level, not code level.
<!-- Example: Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats -->

### III. Phase Governance (NON-NEGOTIABLE)
<!-- Example: III. Test-First (NON-NEGOTIABLE) -->
Each phase is strictly scoped by its specification; Future-phase features must never leak into earlier phases; Architecture may evolve only through updated specs and plans.
<!-- Example: TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced -->

### IV. Technology Stack Compliance
<!-- Example: IV. Integration Testing -->
All implementations must use the approved technology stack: Python for backend, Next.js for frontend (later phases), FastAPI, SQLModel, Neon DB, OpenAI Agents SDK, MCP, Docker, Kubernetes, Kafka, Dapr (later phases).
<!-- Example: Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas -->

### V. Quality Principles
<!-- Example: V. Observability, VI. Versioning & Breaking Changes, VII. Simplicity -->
All code must adhere to clean architecture principles, stateless services where required, clear separation of concerns, and cloud-native readiness.
<!-- Example: Text I/O ensures debuggability; Structured logging required; Or: MAJOR.MINOR.BUILD format; Or: Start simple, YAGNI principles -->

### VI. Implementation Stability
The constitution must remain stable across all phases and act as the supreme governing document for all agents, providing consistent guidance throughout the project lifecycle.

## Technology Constraints
<!-- Example: Additional Constraints, Security Requirements, Performance Standards, etc. -->

All technology choices must align with the specified stack: Python for backend services, Next.js for frontend applications in later phases, FastAPI for API development, SQLModel for database modeling, Neon DB for database storage, OpenAI Agents SDK and MCP for agent communication, Docker and Kubernetes for containerization and orchestration, and Kafka and Dapr for messaging and distributed systems in later phases.
<!-- Example: Technology stack requirements, compliance standards, deployment policies, etc. -->

## Development Workflow
<!-- Example: Development Workflow, Review Process, Quality Gates, etc. -->

The development workflow must strictly follow: Constitution compliance check → Specification creation and approval → Plan generation → Task breakdown → Implementation. All changes must be traced back to approved specifications, and code-level refinements are prohibited without corresponding spec updates.
<!-- Example: Code review requirements, testing gates, deployment approval process, etc. -->

## Governance
<!-- Example: Constitution supersedes all other practices; Amendments require documentation, approval, migration plan -->

This constitution supersedes all other practices and development guidelines. All agents must comply with these principles, and any deviation requires explicit constitutional amendment with proper documentation, approval, and migration planning. The constitution acts as the supreme governing document for the entire Evolution of Todo project across all phases.
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: 1.0.0 | **Ratified**: 2025-12-30 | **Last Amended**: 2025-12-30
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
