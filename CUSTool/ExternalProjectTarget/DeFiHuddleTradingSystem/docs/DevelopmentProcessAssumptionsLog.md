# Development Process Assumptions & Ambiguity Log

## Entry: Requirement 1.1
- Ambiguity: Original requirement 1.1 was broad and lacked actionable detail.
- Resolution: Clarified as a set of actionable, testable sub-requirements (1.1.1–1.1.4) focusing on onboarding, automation, feedback, and accessibility.
- Assumption: Users are unfamiliar with trading and require step-by-step guidance and automation for all complex operations.
- Assumption: All advanced features must be accessible without technical knowledge.
- All changes traceable to original 1.1.

## Entry: Requirement 1.2
- Ambiguity: Original requirement 1.2 was broad and did not specify which tasks should be automated or what "simplest usage" means.
- Resolution: Clarified as maximizing automation and minimizing user effort, with actionable sub-requirements (1.2.1–1.2.4).
- Assumption: All non-essential user actions are handled by the system.
- Assumption: Simplest usage means the fewest possible steps for all workflows, with defaults and guidance provided.
- All changes traceable to original 1.2.

## Entry: Requirement 1.3
- Ambiguity: Original requirement 1.3 was metaphorical and not directly actionable.
- Resolution: Clarified as a set of actionable requirements for interface simplicity and complexity abstraction (1.3.1–1.3.4).
- Assumption: "As simple as a car" means the user interface must be intuitive, with all complexity hidden.
- Ambiguity: The metaphor is now translated into requirements for interface design and complexity abstraction.
- All changes traceable to original 1.3.

## Entry: Requirement 2.1
- Ambiguity: Original requirement 2.1 did not specify installation, testing, or documentation for cross-platform support.
- Resolution: Clarified as full feature parity, installation packages, automated testing, and documentation of platform-specific differences (2.1.1–2.1.4).
- Assumption: "Run" means full feature parity and support, not just basic operation.
- All changes traceable to original 2.1.

## Entry: Requirement 2.2
- Ambiguity: Original requirement 2.2 did not specify what aspects are optimized for Canadian users.
- Resolution: Clarified as defaults for Canadian market data, currency, compliance, and localization (2.2.1–2.2.4).
- Assumption: "Primarily" means all defaults and optimizations are for Canada, but other regions are not excluded.
- All changes traceable to original 2.2.

## Entry: Requirement 2.3
- Ambiguity: Original requirement 2.3 did not specify what data sources, integration, or compliance means.
- Resolution: Clarified as documentation, integration, reliability, and update mechanisms for all data sources and market feeds (2.3.1–2.3.4).
- Assumption: "To be specified during design" means all details must be documented before implementation.
- All changes traceable to original 2.3.

## Entry: Requirement 2.4
- Ambiguity: Original requirement 2.4 did not specify what "in scope" means for features or how to handle future asset classes.
- Resolution: Clarified as initial support for stocks, extensibility for other asset classes, and documentation of deferred requirements (2.4.1–2.4.4).
- Assumption: "Multi-asset coverage" means the architecture must be extensible beyond stocks.
- All changes traceable to original 2.4.

## Entry: Requirement 2.5
- Ambiguity: Original requirement 2.5 was a notation/convention, not a functional requirement, and did not specify how key concepts are tracked or referenced.
- Resolution: Clarified as a process requirement for glossary, traceability, and mapping of key concepts (2.5.1–2.5.3).
- Assumption: The use of `...` is a formal convention for marking key concepts.
- All changes traceable to original 2.5.

## Entry: Requirement 2.6
- Ambiguity: Original requirement 2.6 was a notation/convention, not a functional requirement, and did not specify how configurability is implemented or documented.
- Resolution: Clarified as a process requirement for user interfaces, documentation, and validation of all configurable items (2.6.1–2.6.3).
- Assumption: The use of `(configurable)` is a formal convention for marking user-modifiable elements.
- All changes traceable to original 2.6.

## Entry: Requirement 2.7
- Ambiguity: Original requirement 2.7 was a clarification, not a functional requirement, and did not specify how to handle display or documentation.
- Resolution: Clarified as a system requirement for canonical use of exchange time, accurate retrieval, display, and documentation (2.7.1–2.7.4).
- Assumption: All time-based logic must use exchange time as the canonical reference.
- All changes traceable to original 2.7.

## Entry: Requirement 2.8
- Ambiguity: Original requirement 2.8 did not specify authentication methods, security controls, or compliance.
- Resolution: Clarified as a system requirement for authentication methods, security controls, compliance, and security review (2.8.1–2.8.4).
- Assumption: "Will be clarified at solution design time" means all details must be specified and documented before implementation.
- All changes traceable to original 2.8.

## Entry: Requirement 2.9
- Ambiguity: Original requirement 2.9 did not specify data storage or documentation of operational limitations.
- Resolution: Clarified as a system requirement for single-user mode, single account, local storage, and documentation (2.9.1–2.9.4).
- Assumption: "Single user mode" means no multi-user or concurrent sessions.
- All changes traceable to original 2.9.

## Entry: Requirement 3.1.3
- Ambiguity: Original requirement 3.1.3 did not specify how fee data is managed, retrieved, or what external dependencies exist.
- Resolution: Clarified as a set of requirements for fee data management, including retrieval, update mechanisms, and error handling (3.1.3.1–3.1.3.4).
- Assumption: Authoritative sources or APIs for all fee types (broker, exchange, instrument, trading) are available and accessible at system startup.
- Assumption: Government taxes and tariffs are not required for any internal trading calculations or reporting, only for user tax reporting outside the system.
- Ambiguity resolved: If fee data cannot be retrieved, the system must alert the user and not proceed with incomplete fee calculations.

## Entry: Requirement 3.1.4
- Ambiguity: Original requirement 3.1.4 did not specify how watchlist data is managed, retrieved, or what external dependencies exist.
- Resolution: Clarified as a set of requirements for watchlist data management, including retrieval, update mechanisms, and error handling (3.1.4.1–3.1.4.4).
- Assumption: Google Drive API access and user authentication are available for watchlist synchronization.
- Assumption: If Google Drive sync fails, local watchlist management is sufficient for system operation.
- Ambiguity resolved: Watchlist creation, editing, and update mechanisms must be explicitly documented and implemented for both manual and automated (API) entry.

## Entry: Requirement 3.1.5
- Ambiguity: Original requirement 3.1.5 did not specify what events are logged, at what level of detail, or how log data is protected.
- Resolution: Clarified as a set of requirements for logging events, including authentication, data access, and system changes, with specific fields and formats (3.1.5.1–3.1.5.4).
- Assumption: The system can generate and display unique identifiers for all audit log entries in real time.
- Assumption: Secure, tamper-evident storage (e.g., append-only log, cryptographic hash chaining) is feasible for audit logs.
- Ambiguity resolved: Audit log access is restricted to authorized users, and the retention policy must be documented.

## Entry: Requirement 4.1
- Ambiguity: Original requirement 4.1 did not specify what "user-friendly" means in the context of configuration or how it is validated.
- Resolution: Clarified as a set of requirements for user interface design, validation, and documentation of configuration options (4.1.1–4.1.4).
- Assumption: All required user inputs for configuration can be captured via a GUI and/or CLI interface.
- Assumption: Grouping and expand/collapse functionality is feasible in both GUI and CLI implementations.
- Ambiguity resolved: The configuration wizard must validate all inputs and provide contextual help for each setting.

## Entry: Requirement 4.2
- Ambiguity: Original requirement 4.2 did not specify what "guided setup" entails or how installation issues are handled.
- Resolution: Clarified as a set of requirements for automated environment setup, dependency installation, and guided troubleshooting (4.2.1–4.2.4).
- Assumption: All required environment setup and dependency installation steps can be automated for supported platforms.
- Assumption: Both GUI and CLI installer modes are feasible for the target user base.
- Ambiguity resolved: The installer must log all actions and provide actionable feedback for missing prerequisites.

## Entry: Requirement 4.3
- Ambiguity: Original requirement 4.3 did not specify what "simplified configuration" means or how it differs from the regular configuration.
- Resolution: Clarified as a set of requirements for a simplified configuration interface, default settings, and user guidance (4.3.1–4.3.3).
- Assumption: All configuration settings can be presented in a centralized, human-readable interface with inline help/tooltips.
- Assumption: Default values and their explanations are available for all settings and can be restored by the user.
- Ambiguity resolved: The configuration interface must allow users to review and restore default values at any time.

## Entry: Requirement 4.4
- Ambiguity: Original requirement 4.4 did not specify how mode selection interacts with configuration or operation.
- Resolution: Clarified as a set of requirements for mode selection, including available modes, selection criteria, and impact on configuration and operation (4.4.1–4.4.3).
- Assumption: The mode selection menu can be implemented in both GUI and CLI interfaces.
- Assumption: All relevant settings for each mode can be displayed and confirmed before activation.
- Ambiguity resolved: The mode selection menu must be accessible from both the configuration wizard and the main application interface.

## Entry: Requirement 4.5
- Ambiguity: Original requirement 4.5 did not specify how advanced features are presented or managed in the user interface.
- Resolution: Clarified as a set of requirements for the abstraction of advanced features, including user interface options, technical detail hiding, and guidance (4.5.1–4.5.3).
- Assumption: All advanced features can be abstracted behind simple, high-level options in the user interface.
- Assumption: Users do not need to understand technical details to enable or disable advanced features.
- Ambiguity resolved: The user interface must provide clear descriptions and guidance for each advanced feature.

## Entry: Requirement 4.6
- Ambiguity: Original requirement 4.6 did not specify how user guidance is provided or how errors are handled and reported.
- Resolution: Clarified as a set of requirements for user guidance, error message formatting, and documentation links (4.6.1–4.6.3).
- Assumption: All user-facing errors and warnings can be mapped to unique error IDs and linked to technical logs.
- Assumption: Contextual help and documentation links are available for all error scenarios.
- Ambiguity resolved: Error messages must be free of technical jargon and always provide actionable suggestions.

## Entry: Requirement 4.7
- Ambiguity: Original requirement 4.7 did not specify how `Scale In` and `Scale Out` orders are treated in relation to bracket orders.
- Resolution: Clarified as separate processing and adjustment rules for `Scale In` and `Scale Out` orders, including logging requirements (4.7.1–4.7.3).
- Assumption: The system can distinguish and process `Scale In` and `Scale Out` orders separately from bracket orders.
- Assumption: The system can automatically adjust bracket orders in response to scale in/out actions.
- Ambiguity resolved: All scale in/out and bracket order adjustments must be logged with rationale and parameters.

## Entry: Requirement 5.1
- Ambiguity: Original requirement 5.1 did not specify what constitutes a "back test" or "strategy" and how they are documented or validated.
- Resolution: Clarified as a set of requirements for back testing framework, including test case definition, execution, and result analysis (5.1.1–5.1.4).
- Assumption: Back testing datasets can be sourced in multiple formats and validated for integrity.
- Assumption: All required KPIs and scenario types can be logged and analyzed per strategy and session.
- Ambiguity resolved: Back test re-runs are mandatory if fee structures change, and historical performance analysis must be provided.

## Entry: Requirement 5.2
- Ambiguity: Original requirement 5.2 was vague about the confirmation process, liability language, and auditability.
- Resolution: Clarified as requiring explicit, logged user confirmation with liability release, persistent UI indicator, and re-confirmation on restart.
- Assumption: "Accepts all liabilities and frees author" means a formal, logged acknowledgment is required before live mode is enabled.
- Assumption: User identity is available for logging; if not, session ID or device ID will be used.
- All changes traceable to original 5.2.

## Entry: Requirement 5.3
- Ambiguity: Original requirement 5.3 was broad and did not specify boundaries for auto-tuning, logging, or user control.
- Resolution: Clarified as detailed requirements for training log structure, auto-tuning scope and safeguards, learning/enhancement cycles, and user management of enhancements.
- Assumption: Only settings explicitly marked as auto-tunable may be changed by the AI; all critical/risk settings are protected.
- Assumption: All logs must be both human- and machine-readable.
- Assumption: User approval is required for all code changes unless explicitly configured otherwise.
- All changes traceable to original 5.3.

## Entry: Requirements 17–24
- Ambiguity: Original requirements were concise but lacked explicit detail on logging, user notification, and configuration boundaries.
- Resolution: Clarified as explicit, testable requirements for polling, alerting, user controls, state persistence, and data formats.
- Assumption: All polling intervals, thresholds, and criteria are user-configurable unless otherwise stated.
- Assumption: All logs and alerts must be both human- and machine-readable where applicable.
- Assumption: Emergency stop and symbol deactivation must persist across restarts unless explicitly cleared by the user.
- All changes traceable to original requirements 17–24.
