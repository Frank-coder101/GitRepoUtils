# Architecture Artifact Criteria: Advanced Completeness and Quality Gaps

This file contains only the advanced criteria not already fully addressed in the main process instructions. Use these as additional required checks for every architecture artifact.

---

## 1. Complete Functional and Non-Functional Coverage
- Every artifact must explicitly document how it addresses:
  - Functional requirements (structure, logic, data flows, behaviors, component responsibilities)
  - Non-functional requirements (performance, scalability, availability, security, etc.)
  - Constraints and assumptions (regulatory, temporal, resource, etc.)

## 2. Viewpoint Alignment (ISO/IEC/IEEE 42010)
- Validate/generate artifacts from all relevant architectural viewpoints:
  - Functional
  - Information/Data
  - Development
  - Technology
  - Security
  - Operational
- Each viewpoint should address the stakeholder concerns associated with the requirement.

## 3. 5 Dimensions of Satisfaction
For each artifact, explicitly check:
- Correctness: Does the artifact address all aspects of the requirement?
- Clarity: Can a stakeholder clearly understand how the requirement is met?
- Consistency: Is it free of conflict with other requirements or artifacts?
- Feasibility: Is the described architecture implementable within real-world constraints?
- Testability: Can the requirement be verified against the artifact (e.g., via test cases, reviews)?

## 4. Acceptance Criteria & Verification Tests
- For each artifact, generate or require:
  - Scenario-based validations (usage/operational scenarios that exercise the requirement)
  - Quality attribute scenarios (concrete measurement criteria: response time, load, availability, etc.)
  - Formal reviews/walkthroughs with requirement owners and technical leads

## 5. Golden Questions (Checkpoints)
Before considering an artifact complete, answer YES to all:
- Is this artifact explicitly linked to one or more requirements?
- Does it cover every functional and non-functional element the requirement describes?
- Can a developer or tester implement/test this without ambiguity or external info?
- Are the assumptions, constraints, and rationale clearly documented?
- Is this artifact aligned with stakeholder concerns identified for this requirement?

## 6. Universal Completeness Criteria (from standards)
- Clearly scoped (what is included/excluded)
- Consistent with context (system boundaries, integrations)
- Component breakdown (modules, services, interfaces, roles)
- Data concerns defined (entities, relationships, flows, master data)
- Technology stack specified (runtime, frameworks, protocols, platforms, NFRs)
- Rationale documented (design decisions, trade-offs, constraints, patterns)
- Viewpoints addressed (stakeholder-specific views)
- Traceability established (requirement-to-architecture trace)
- Sufficient detail for development (interfaces, models, diagrams, state transitions)
- Verified and reviewed (peer reviews, stakeholder validation, quality gates)

## 7. Viewpoint Coverage Table
- For each artifact, check if all relevant viewpoints (Functional, Logical, Data, Development, Technology, Security, Operational) are covered.
- Generate missing child artifacts as needed for any uncovered viewpoints.

## 8. Decision Matrix and Zachman Crosswalk
- Use the decision matrix and Zachman crosswalk to systematically identify when decomposition or additional artifacts are needed.
- Decompose artifacts if:
  - They span multiple domains (App/Data/Tech)
  - Mix multiple stakeholder concerns
  - Lack detail in interfaces, flows, or behaviors
  - Are generic (not developer-specific)
  - Are compound views of architecture tiers
- Use Zachman columns (What, How, Where, Who, When, Why) to check for missing child artifacts.