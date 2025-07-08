# False Negatives Test Anti Pattern in Integration and Unit TestModes

## Context
- In integration and unit testing, a common anti-pattern is when a test always passes (false negative) because the code under test returns a success value (e.g., `True`) regardless of whether the integration or logic actually succeeded.
- This can mask real integration failures and give a false sense of reliability.

## Examples Found in Project
- `OrderManager.cancel_order` previously always returned `True` in integration mode, even if the broker was not connected. This caused tests to pass even when IBKR was unavailable.
- `RiskEngine.check_risk` always returned `True` (stub), so tests using `assertTrue(result)` would always pass, even though no real risk logic was implemented.

## Corrective Actions
- `OrderManager.cancel_order` now checks broker connectivity and IBKR availability in integration mode, raising an exception if not connected, matching the logic in `place_order`.
- `RiskEngine.check_risk` now raises `NotImplementedError` in integration mode until real logic is implemented.
- Corresponding tests have been updated to expect these failures in integration mode (using `assertRaises`).

## Test Discovery Note
- If test runs report "NO TESTS RAN," check for test discovery issues (e.g., missing `__init__.py`, test file/class/method naming).
- The logic is now correct: integration tests will fail if integration is not implemented or the broker is unavailable.

## Guidance
- Always ensure that integration and unit test logic does not return unconditional success in any mode where real integration or logic is required.
- Use exceptions and explicit failure modes to ensure tests fail when integration is not available or not implemented.

---

*This prompt documents the anti-pattern of false negatives in integration/unit test modes and the corrective actions taken in this project.*
