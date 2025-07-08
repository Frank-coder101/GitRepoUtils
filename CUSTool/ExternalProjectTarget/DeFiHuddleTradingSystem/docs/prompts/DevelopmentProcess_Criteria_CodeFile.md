# Advanced Code File Criteria: Completeness and Quality Gaps

This file contains only the advanced criteria not already fully addressed in the main process instructions. Use these as additional required checks for every code file.

---

## 1. Structural Conformance to Architecture
- Code must implement prescribed components, interfaces, boundaries, and patterns as defined in the architecture (e.g., layering, contracts, technology stack).
- Validate against architectural models (UML, C4, OpenAPI, etc.).
- Use static code analysis and architecture lint tools to check for violations (e.g., cross-layer calls, circular dependencies).

## 2. Behavioral Alignment (Functional Realization)
- Code must realize the intended use cases, workflows, and sequences described in architecture artifacts (e.g., sequence diagrams, state machines).
- Use behavior-driven testing (BDD) or map tests to architectural scenarios.
- Compare sequence/activity diagrams to runtime call graphs (via tracing tools or logs).

## 3. Non-Functional Fulfillment (Quality Attributes)
- Code must meet non-functional requirements (performance, scalability, security, modifiability, availability, etc.) as specified in the architecture.
- Validate via NFR testing, benchmarking, static/dynamic analysis, and runtime monitoring.

## 4. Coding Standards and Constraints
- Code must adhere to language-specific style guides, project conventions, approved libraries, and architectural constraints.
- Use static code analysis and lint tools to enforce standards.

## 5. Validation via Reviews and Inspections
- Conduct code walkthroughs against architecture models (especially for high-risk modules).
- Involve architects in pull requests/reviews.
- Use architecture fitness functions to assert ongoing alignment.

## 6. Evaluation Matrix
- For every code file, complete a summary evaluation matrix covering:
  - Traceability
  - Structural conformance
  - Behavioral alignment
  - Non-functional fulfillment
  - Coding/convention adherence
  - Review/inspection status

