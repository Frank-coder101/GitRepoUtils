Trading System Requirements

# 1 Goal
1.1 The system shall provide an intuitive, guided experience for new retail investors, enabling them to access advanced institutional trading capabilities with minimal prior knowledge or manual configuration.
    1.1.1 The system shall include a user-friendly onboarding process that explains key concepts and steps.
    1.1.2 The system shall automate all complex trading operations, requiring only essential user inputs.
    1.1.3 The system shall provide clear feedback and guidance at each step, minimizing the risk of user error.
    1.1.4 The system shall ensure all advanced features are accessible without requiring users to understand underlying technical details.
1.2 The system shall maximize automation and minimize user effort at every stage of operation.
    1.2.1 The system shall automate all routine trading tasks, requiring user input only for essential decisions.
    1.2.2 The system shall provide default configurations and intelligent suggestions to reduce manual setup.
    1.2.3 The system shall support one-click or minimal-step workflows for all major user actions.
    1.2.4 The system shall continuously monitor for opportunities to further simplify user interactions, with regular usability reviews.
1.3 The system shall deliver advanced trading capabilities through an interface as simple and intuitive as operating a car, abstracting all underlying technical complexity from the user.
    1.3.1 The system shall provide a consistent, user-friendly interface for all features, regardless of underlying complexity.
    1.3.2 The system shall abstract all technical and engineering details, exposing only essential controls and information to the user.
    1.3.3 The system shall ensure that advanced features are accessible through simple, guided workflows.
    1.3.4 The system shall regularly evaluate user experience to identify and remove unnecessary complexity.

# 2 Cross-Platform Requirement
2.1 The system shall be fully cross-platform, supporting Windows 10 and later, macOS, and Linux distributions.
    2.1.1 The system shall provide installation packages and instructions for each supported operating system.
    2.1.2 The system shall ensure all features are available and functionally equivalent across all supported platforms.
    2.1.3 The system shall include automated cross-platform testing as part of the CI/CD pipeline.
    2.1.4 The system shall document any platform-specific limitations or differences.
2.2 The system shall be optimized for primary use by users in Canada.
    2.2.1 The system shall default to Canadian market data, exchanges, and regulatory settings.
    2.2.2 The system shall support Canadian currency (CAD) and local conventions in all user interfaces and reports.
    2.2.3 The system shall ensure compliance with Canadian trading regulations and data privacy laws.
    2.2.4 The system shall provide localization for Canadian English and French where applicable.
2.3 The system shall define and document all data sources and market feeds during the design phase.
    2.3.1 The system shall identify all required data sources (e.g., market data, news, historical prices) and document their providers.
    2.3.2 The system shall specify integration methods and data formats for each data source and market feed.
    2.3.3 The system shall ensure all data sources are reliable, secure, and compliant with relevant regulations.
    2.3.4 The system shall provide mechanisms for updating or replacing data sources as needed.
2.4 The system shall support multi-asset coverage, with initial scope limited to stocks.
    2.4.1 The system shall implement all trading, data, and reporting features for stocks in the initial release.
    2.4.2 The system shall be designed to allow future extension to other asset classes (e.g., ETFs, options, futures, crypto).
    2.4.3 The system shall document the prioritization and requirements for deferred asset classes in the “Deferred Requirements” section.
    2.4.4 The system shall ensure all architecture and code are modular to facilitate future asset class integration.
2.5 All requirements using the character ` at the beginning and end of words indicate key functional concepts critical to design and implementation.
    2.5.1 The system documentation shall include a glossary or index of all such key functional concepts.
    2.5.2 All architecture and code artifacts shall reference these concepts for traceability.
    2.5.3 The requirements traceability matrix shall map each key concept to its implementation and related artifacts.
2.6 All requirements using the text `(configurable)` indicate that the preceding value, item, component, or logic must be user-configurable.
    2.6.1 The system shall provide user interfaces or configuration files to allow modification of all items marked as `(configurable)`.
    2.6.2 The system documentation shall include a list of all configurable items and instructions for their modification.
    2.6.3 All configuration changes shall be validated to ensure system integrity and prevent invalid states.
2.7 All time values related to trading operations shall be based on the symbol's exchange's regular hours and time zone, not the end user's time zone.
    2.7.1 The system shall retrieve and maintain accurate exchange hours and time zone data for all supported symbols.
    2.7.2 The system shall calculate all time-based operations (e.g., offsets, cutoffs) using the exchange's local time.
    2.7.3 The system shall display all relevant times to the user in both the exchange's local time and the user's local time, with clear labeling.
    2.7.4 The system documentation shall clearly state this convention for all time-related requirements.
2.8 The system shall define and implement user authentication and security requirements during the solution design phase.
    2.8.1 The system shall identify all authentication methods required (e.g., password, OAuth, multi-factor authentication) and document them in the design.
    2.8.2 The system shall specify security controls for data protection, access control, and secure communications.
    2.8.3 The system shall ensure compliance with relevant security standards and regulations.
    2.8.4 The system shall include a security review and threat assessment as part of the design process.
2.9 The system shall operate in single-user mode on a local PC, supporting only one brokerage account per instance.
    2.9.1 The system shall restrict access to a single user session at a time.
    2.9.2 The system shall allow configuration and connection to only one brokerage account per installation.
    2.9.3 The system shall store all user and account data locally, with appropriate security controls.
    2.9.4 The system documentation shall clearly state these operational limitations.

# 3 Functional Requirements

## 3.1 User Journey

### 3.1.1 First Launch
3.1.1.1 User inputs total funds available for trading with this solution
3.1.1.2 Connects to brokers account.  

### 3.1.2 Subsequent Launches
3.1.2.1 The application will run the logic described in the Execution Cycles (see 7.0) in one of the following `modes`:  
3.1.2.1.1 `BackTesting`
3.1.2.1.2 `Live`
3.1.2.2 Live mode requires explicit user confirmation.  
3.1.2.3 If in live mode, pull broker and instrument-specific fees when performing opportunity analysis during the cycles.

### 3.1.3 Fee Management
3.1.3.1 The system shall, on every startup, automatically retrieve and update all applicable trading fees, including broker, exchange, instrument-specific, and trading fees, from authoritative sources or APIs.
    3.1.3.1.1 The system shall log the source and timestamp of each fee retrieved.
    3.1.3.1.2 The system shall validate the completeness and correctness of the fee data before use.
    3.1.3.1.3 The system shall alert the user if any required fee data cannot be retrieved or validated.
3.1.3.2 The system shall explicitly exclude government taxes and tariffs from all fee calculations and reporting.
    3.1.3.2.1 The system documentation shall clearly state that government taxes and tariffs are not included in fee calculations.
### 3.1.4 Watchlist management
3.1.4.1 The system shall maintain a user-defined `persistent watchlist` for long-term symbol entries.
    3.1.4.1.1 The system shall provide user interfaces for creating, editing, and deleting entries in the persistent watchlist, supporting both manual entry and saved API queries.
    3.1.4.1.2 The persistent watchlist shall be stored in a secure, user-accessible location and synchronized with a designated Google Drive account at regular, user-configurable intervals.
    3.1.4.1.3 If Google Drive synchronization is not feasible, the system shall initialize the watchlist with default values and maintain local updates.
    3.1.4.1.4 The system shall log all changes to the watchlist, including the source (manual, API, sync), timestamp, and user identity.
    3.1.4.1.5 The system documentation shall describe how symbols are added, updated, and removed from the persistent watchlist, including storage and update mechanisms.
### 3.1.5 Logging and auditing
3.1.5.1 The system shall implement a unified audit log for all orders, order rejections, and user confirmations.
    3.1.5.1.1 Each audit log entry shall include a unique identifier, which must be displayed to the user whenever a related user message is shown.
    3.1.5.1.2 Each entry shall include a timestamp, all relevant order details, and profit/loss (P&L) information.
    3.1.5.1.3 For runtime exceptions, the log entry shall include the most precise call stack reference available, down to the line number.
    3.1.5.1.4 The audit log shall be stored in a secure, tamper-evident format and be accessible for review by authorized users.
    3.1.5.1.5 The system documentation shall describe the audit log structure, retention policy, and access controls.

# 4 User Experience and Accessibility Requirements (Added July 2, 2025)

4.1 User-Friendly Configuration
4.1.1 The system shall provide a simple, user-friendly configuration interface for all required user inputs (funds, trade settings, risk settings, etc.), grouping related settings and enabling each group to be expanded or collapsed for ease of use.
4.1.2 The system shall ensure that users (including end users, installers, and developers) are not required to manually edit configuration files for initial setup; all required inputs must be accessible via the configuration interface.
4.1.3 The system shall include a configuration wizard (GUI and/or CLI) that guides users through all necessary setup steps, validating inputs and providing contextual help or tooltips for each setting.

4.2 Guided Setup and Installation  
4.2.1 The system shall provide a step-by-step guided installation process or installer that automates environment setup, dependency installation, and initial configuration, ensuring all required components are installed and configured correctly for the user's platform.
    4.2.1.1 The installer shall validate system prerequisites and provide clear, actionable feedback if any requirements are missing.
    4.2.1.2 The installer shall support both GUI and CLI modes, where feasible, to accommodate different user preferences and environments.
    4.2.1.3 The installer shall log all actions and outcomes for troubleshooting and support purposes.
 
4.3 Simplified Configuration  
4.3.1 The system shall provide a centralized, human-readable configuration interface that includes inline help text or tooltips for each setting, ensuring users can easily understand and modify all configuration options.
4.3.2 The system shall provide default values for all configuration settings, with clear explanations of each value and its impact on system behavior, accessible directly within the configuration interface.
    4.3.2.1 The configuration interface shall allow users to review and restore default values as needed.
4.4 User-Friendly Mode Selection  
4.4.1 The system shall present users with a clear, interactive menu to select between `BackTesting` and `Live` modes, displaying all relevant settings for the selected mode before proceeding.
    4.4.1.1 The mode selection menu shall be accessible from both the initial configuration wizard and the main application interface.
    4.4.1.2 The system shall validate the user's selection and confirm all settings before activating the chosen mode.

4.5 Abstraction of Advanced Features
4.5.1 The system shall abstract advanced institutional features (e.g., multi-timeframe analysis, regime detection, analysis methods, scoring) behind simple, high-level options for users, ensuring these features are accessible without requiring technical expertise.
    4.5.1.1 The user interface shall provide clear descriptions and guidance for each advanced feature, allowing users to enable or disable them as needed.
    4.5.1.2 The system shall ensure that enabling advanced features does not require manual configuration or understanding of underlying algorithms.

4.6 User Guidance and Error Handling  
4.6.1 The system shall present all user-facing errors and warnings in plain language, with actionable suggestions for resolution and a uniquely identifiable error ID that correlates to a technical error log entry.
    4.6.1.1 The error messages shall be clear, concise, and free of technical jargon.
    4.6.1.2 Each error or warning shall include a reference or link to relevant documentation or help resources.
4.6.2 The system shall provide contextual help or direct links to documentation whenever errors occur, ensuring users can quickly access guidance to resolve issues.

4.7 `Scale In` and `Scale Out` Orders
4.7.1 The system shall implement `Scale In` and `Scale Out` order types, which are distinct from `take profit` and `stop loss` (bracket) orders.
    4.7.1.1 A `Scale In` order is a near-immediate limit order to add to a position, with the limit price calculated using the current ask or bid price (depending on long/short) to maximize immediate execution.
    4.7.1.2 A `Scale Out` order is a near-immediate limit order to reduce position risk, with the limit price calculated using the current ask or bid price (depending on long/short) to maximize immediate execution.
    4.7.1.3 Whenever a `Scale In` or `Scale Out` order is placed, the corresponding bracket orders (take profit and stop loss) must be automatically adjusted to ensure the position is closed if either bracket order is executed.
    4.7.1.4 The system shall log all scale in/out and bracket order adjustments, including the rationale and resulting order parameters.

# 5 Runtime Modes

## 5.1 Back Testing
5.1.1 The system shall find, create, pull, and use a back testing dataset to simulate market activity for stocks.
    5.1.1.1 The system shall support importing datasets from multiple sources and formats (e.g., CSV, API, database).
    5.1.1.2 The system shall validate the integrity and completeness of all back testing datasets before use.
5.1.2 The system shall log KPIs per strategy, including:
    5.1.2.1 Success rate
    5.1.2.2 Profit or loss percentage
    5.1.2.3 Total exposure
5.1.3 The system shall persist back test results and compare them with prior runs, providing historical performance analysis.
5.1.4 The system shall require a re-run of back tests if fee structures change.
5.1.5 The system shall include baseline back tests for recession periods (1968–1975) and the last 6 years.
5.1.6 The system shall simulate regime transitions and stop-loss/take-profit logic across all bars in the dataset.
5.1.7 The system shall log all simulated trades with outcome scores for each trade.
5.1.8 The system shall persist session-level KPIs, including:
    5.1.8.1 Total return
    5.1.8.2 Max drawdown
    5.1.8.3 Win/loss rate
    5.1.8.4 Sharpe ratio
5.1.9 The system shall support multi-scenario back test runs, including:
    5.1.9.1 Trade halt
    5.1.9.2 Market crash
    5.1.9.3 Recession
    5.1.9.4 Normal
    5.1.9.5 Inflation
    5.1.9.6 1929 style depression

## 5.2 Live Mode (Upgraded and Decomposed)
5.2.1 The system shall require explicit user confirmation before entering live trading mode, displaying a clear warning about risks and requiring the user to accept all liabilities and release the system author from any liability or damages.
    5.2.1.1 The confirmation dialog shall include a summary of live trading risks, a statement of liability release, and require the user to check an explicit acknowledgment box before proceeding.
    5.2.1.2 The system shall log the user's confirmation, including timestamp, user identity, and the exact text of the warning and acknowledgment.
    5.2.1.3 The system shall prevent activation of live mode unless the confirmation is completed in the current session.
    5.2.1.4 The system shall provide a mechanism to review the most recent live mode confirmation in the audit log.
5.2.2 The system shall display a persistent indicator in the UI when operating in live mode, including a warning color scheme and mode label.
5.2.3 The system shall require re-confirmation if the application is restarted or if the user logs out and back in.

## 5.3 Training, Machine Learning, and Auto Tuning Capabilities (Upgraded and Decomposed)
5.3.1 The system shall maintain a detailed, structured `Training Log` for all machine learning, training, and auto-tuning activities, capturing:
    5.3.1.1 Title, rationale, timestamp, related configuration setting, and code reference for each training or tuning event.
    5.3.1.2 All analyzed and scored opportunities, including symbol, overall score, and sub-scores for each analysis method.
    5.3.1.3 All trades, including symbol, trigger, order details (entry, scale in/out, exit, stop loss, take profit), runtime errors (with unique error ID), and profit/loss outcomes.
    5.3.1.4 The log must be both human-readable and machine-readable (e.g., JSON or CSV).
5.3.2 The system shall enable the AI service to autonomously tune only designated configuration settings and code logic, with safeguards:
    5.3.2.1 Only settings explicitly marked as auto-tunable may be modified by the AI; critical settings (e.g., account balance, trade size limits, risk settings) are excluded and protected.
    5.3.2.2 All auto-tuning changes must be preceded by a backup of the affected configuration and code, and changes must be applied without requiring a system restart.
    5.3.2.3 The AI service must support grid search, random search, and Bayesian optimization for tuning scoring and strategy weights.
    5.3.2.4 The AI service must be able to propose and apply code logic changes for sections 6, 7, and 8, with user approval required for activation.
    5.3.2.5 The system shall implement safeguards against overfitting, such as penalizing high-variance or scenario-specific configurations.
5.3.3 The system shall implement a `Learning Cycle` that runs only during off-hours or when triggered by the user, and is preempted by all other execution cycles:
    5.3.3.1 The AI service is invoked with the current `Training Log`, system configuration, and source code.
    5.3.3.2 The AI analysis must produce repeatable results in a standardized format, and results are stored in an `Enhancement Log`.
5.3.4 The system shall implement an `Enhancements Activation Cycle` that runs only during off-hours or when triggered by the user, and is preempted by all other cycles:
    5.3.4.1 The system shall verify if user approval is required for activation of enhancements (configurable, default true for all changes).
    5.3.4.2 The system shall display a list of proposed enhancements and obtain user approval before activation.
    5.3.4.3 For each approved enhancement, the system shall backup the affected configuration/code and log a summary report, including configurations tried, win/loss ratio, volatility, diagnostics, and backup reference.
5.3.5 The system shall provide an `Enhancements Management` interface for users to:
    5.3.5.1 View the full history of enhancements and restore the system to any previous state.
    5.3.5.2 Designate and restore to a `last known good version` at any time, even after system or PC restart.
    5.3.5.3 View and restore only the list of designated `last known good version` points.

# 6 Analysis and Scoring
Each `instrument` (symbol) will be analyzed in a decomposed approach using `analysis methods`.
The overall scoring of each `instrument` will be broken down by each `analysis method` carrying their own score which are each moified by configurable weights (0-100)

6.1 `Technical Analysis Methods`
Score each item using PhD-level / institutional-grade analysis
6.1.1 Regression forecasting  
6.1.2 Regime states (Scalp, Long, Take Profit, Reversal, Liquidate, Short)  
6.1.3 All 20 candle patterns  
6.1.4 SMA 5, 9, 55, 200 (and crossovers)  
6.1.5 EMA 21  
6.1.6 Candle crossover of above SMAs and EMA  
6.1.7 Reversals and divergences with RSI, CMF, MACD  
6.1.8 Swing trade profiles, oscillators, contrarian setups  
6.1.9 Momentum, streak logic, Fibonacci, Elliott wave, Bollinger Bands  
6.1.10 Order block detection  
6.1.11 Market depth (warn if unavailable)
6.1.12 Multi-Timeframe Analysis (MTFA)  
6.1.12.1 pull data for multiple configurable timeframes and re-runs all above `technical analysis` steps
6.1.12.2 Each cross-timeframe agreement multiplies the score by a configurable factor

# 7 Execution Cycles

## 7.1 Execution Logic
7.1.1 All cycles should be executed in parallel -if possible, easy to troubleshoot, easy to extend.
7.1.2 Each cycle has priority over the other cycles (in the order they are documented) and preempts the cycles defined thereafter in this section
7.1.3 Each cycle must track the `Average Cycle Time` and alert and log a warning if current cycle time is taking longer than 10% of the average time

## 7.2 `Portfolio Protection` - `Cycle A` - Every Minute
7.1.1 Evaluate each open position to determine if there is an action to be taken
7.1.1.1 Determine if position should `urgently` be acted on if:
7.1.1.1.1 The price is worse than the stop loss (meaning the stop loss order failed to trigger
or
7.1.1.1.2 If light weight assessment of the following is higher than tolerance level (configurable): 
7.1.1.1.2.1 liquidation risk, or, 
7.1.1.1.2.2 trade halt risk 
7.1.1.1.3 If 7.1.1.1.1 or 7.1.1.1.2.1 or 7.1.1.1.2.2 are true:
7.1.1.1.3.1 exit the position using logic defined in `Trade Execution` and flag the request as `urgent`
7.1.1.1.3.2 display a non modal alert message to the user detailing the action and why it was taken and also place message in `trade log`
7.1.1.1.3.3 go to next open position
7.1.1.2 If no `urgent` action for the position, then run `technical analysis` and 
7.1.1.2.1 If new score is lower than minimum acceptable score, exit position using logic defined in `Trade Execution`
7.1.1.2.1.1 log an alert message in `trade log` detailing the action and why it was taken
7.1.1.2.1.2 go to next open position
7.1.1.3 Persist new score of position in `portfolio positions score` list
7.1.1.4 If `Dynamic End-of-Day Position Closing` (configurable) is set to true, meaning all positions are to be closed before end of regular trading hours
7.1.1.4.1 If Now is > `Market Close Today` - `Shrink Down Time Offset` (configurable, default to 15 minutes)
7.1.1.4.1.1 If old score > new score
7.1.1.4.1.1.1 Close postion using logic defined in `Trade Execution` as "urgent"
7.1.1.4.2 If Now is > `Market Close Today` - `Cutoff Time Offset` (configurable, default to 5 minutes)
7.1.1.4.2.1 Close postion using logic defined in `Trade Execution` as "urgent"
7.1.1.5 Pending orders review
7.1.1.5.1 if there are any pending limit orders for the position that not are braket related (stop loss or take profit) 
7.1.1.5.2 If the old score is higher than new score by more than 1% (configurable)
7.1.1.5.2.1 If it is a scale in order, prepare a message to the user "There is a shrinking opportunity pending order" 
7.1.1.5.2.2 If it is a scale out order, prepare a message to the user "There is a growing risk pending order"
7.1.1.5.3 If the new score is higher than old score by more than 1%  (configurable)
7.1.1.5.3.1 If it is a scale in order, prepare a message to the user "There is a growing opportunity pending order" 
7.1.1.5.3.2 If it is a scale out order, prepare a message to the user "Unexpected shrinking risk pending order please verify situation"
7.1.1.5.4 the message must offer a `mute timer` attribute for that specific message type and specifc symbol in case the user does not want to get more notifications on this specific issue. Mute durations are calculated using 4 drop down values to compute the timer's expiry date. The drop downs are: 7.1.1.5.4.1 minutes (0,5,15,30,45), 7.1.1.5.4.2 hours (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), 7.1.1.5.4.3 days (0,1,2,3,4,5,6), 7.1.1.5.4.4 weeks (0,1,2,3,4). All the drop downs are set to 0 for defaults. When all drop downs are set to 0 no `mute timer` should be created.
7.1.1.5.5 if a message was prepared, and a related `mute timer` has not expired, send the message with the the details of the order (limit, market, etc.) and log the message to the trade log - regardless of the timer status.
7.1.1.5.6 delete any expired related `mute timer`
7.1.1.6 Position sizing review
7.1.1.6.1 If position is in the top 30% of `portfolio positions score` list
7.1.1.6.1.1 and portolio available funds is more than 30% of the total account value
7.1.1.6.1.2 and the position is below the `max position size` by at least `minimum position size`
7.1.1.6.1.3 then scale into the position with an order of `minimum position size` using logic defined in `Trade Execution` (will use limit order type)
7.1.1.6.2 If position is in the bottom 30% of `portfolio positions score` list
7.1.1.6.2.1 and portolio available funds is less than 30% of the total account value
7.1.1.6.2.2 then scale out of the position with an order reducing the position in half using logic defined in `Trade Execution` (will use limit order type)
7.1.1.7 If there is no trailing stop-loss order on the position
7.1.1.7.1 if there was a stop-loss order (other than trailing)
7.1.1.7.1.1 cancel that order
7.1.1.7.1.2 persist data about the original stop-loss order
7.1.1.7.1.3 calculate and create new trailing stop-loss order

## 7.2 `Opportunity Monitoring` - `Cycle B` - Every Minute
7.2.1 `Opportunity Monitoring` - `News Wire Events` - Cycle B.1 - Prefer Event Driven - Every Minute
7.2.1.1 Get a notification call back about a news event (or less preferred, pull from news feed each time for new articles)
7.2.1.2 Parse the content of the news article for stock symbols
7.2.1.3 Add each symbol to `opportunities_identified` list
7.2.2 `Opportunity Monitoring` - `Market Scanning` - Cycle B.2 - Every Minute
7.2.2.1 Conduct market scan and add symbols to `opportunities_identified` list
7.2.3 `Opportunity Monitoring` - `Long Term Entries` - Cycle B.3 - Every Minute 
7.2.3.1 Pull top 10 (configurable) and bottom 10 (configurable) instruments from the `persistent watchlist` that have the highest absolute (+ or -) price change % during the last 2 minutes
7.2.3.2 Add symbols to `opportunities_identified` list
7.2.7 Analyze each symbol in `opportunities_identified` using logic section in 6 `Analysis and Scoring`
7.2.7.1 Remove from the `opportunities_identified` list any symbol whose score is lower than the `minimum acceptable score to take a position`
7.2.7.2 If the porfolio balance is too low for another `minimum position size`
7.2.7.2.1 Create a `temporary symbol table` with columns "symbol, score, size, source" 
7.2.7.2.2 Merge the list of current portfolio position (and their symbol, score, using their market value for size, and "portfolio" as source) with the list of `opportunities_identified` (and their symbol, score, using minimum initial position size setting value for the size column for all of those items, and "new" as source). Sort the `temporary symbol table` by score column with the highest at the top
7.2.7.2.3 Loop through each temporary symbol item
7.2.7.2.3.1 if adding the temporary symbol size to a `temporary total value` variable would be less than than the total allowed trading size of the portfolio
7.2.7.2.3.1.1 add temporary symbol size to the `temporary total value`
7.2.7.2.3.2 if not
7.2.7.2.3.2.1 if the "source" value of the given temporary symbol is "portfolio" 
7.2.7.2.3.2.1.1 exit the position using logic defined in `Trade Execution` and flag the request as `urgent`
7.2.7.2.3.2.2 Remove the temporary symbol whether "source" value is "portfolio" or "new"
7.2.7.2.4 Loop again through each temporary symbol item remaining in `temporary symbol table`
7.2.7.2.4.1 if the "source" value of the given temporary symbol is "new" 
7.2.7.2.4.1.1 open a new position using logic defined in `Trade Execution`

# 8 Trade Execution
8.1 If opening a position
8.1.1 Calculate appropriate sizing using config constraints   
8.1.2 Use limit order if long, use market order if short
8.1.3 Always with trailing stop loss order using configurable percentage
8.2 If closing position
8.2.1 If the closing order is classified as `urgent` or is a short position being closed
8.2.1.1 close position at market value
8.2.2 Cancel any and all pending orders for that symbol
8.2.3 Use calculate limit order using 2 second price slope
8.3 Add order details (and any related order cancelations) to order confirmation log
8.4 Remove position from `portfolio positions score` list

# 9 Deferred Requirements

## 9.1 Options
9.1.1 Automated option chain scanning
9.1.2 Contract roll logic  
9.1.3 Detection of improperly formatted dates in options symbols

## 9.2 Crypto Trades
9.2.1 Crypto assets (e.g., COINBASE:XRPUSDC) will be analyzed and scored  
9.2.2 Coinbase Prime API integration is deferred

## 9.3 Futures
9.3.1 Automated futures expiry handling  
9.3.2 Contract roll logic  
9.3.3 Symbol auto-expansion  
9.3.4 Detection of improperly formatted dates in futures symbols

# 11 Enhanced and Clarified Requirements

## 11.1 Risk Assessment Metrics
- 11.1.1 "Liquidation risk" is defined as: (current price - liquidation price) / current price, where liquidation price is the price at which the broker would forcibly close the position due to insufficient margin.
- 11.1.2 "Trade halt risk" is defined as the probability of a trading halt event for a symbol, based on recent volatility, news events, and exchange halt lists. Configurable threshold (default: 5% probability).
- 11.1.3 All risk thresholds must be configurable parameters, settable in the configuration interface.

## 11.2 Score Thresholds
- 11.2.1 The "minimum acceptable score" is a configurable parameter (default: 60 out of 100).
- 11.2.2 Scoring methodology must be clearly documented and accessible to the user.

## 11.3 Temporary Symbol Table Algorithm
- 11.3.1 Temporary symbol table must include: symbol, score, size (in dollars), and source ("portfolio" or "new").
- 11.3.2 Total allowed trading size is configurable (default: 100% of available funds).
- 11.3.3 Pseudocode for merging and processing the table must be included in system documentation.

## 11.4 News and Scanning Details
- 11.4.1 News source is configurable (default: Yahoo Finance RSS or NewsAPI.org).
- 11.4.2 Market scanning to use configurable API (default: IBKR TWS or Yahoo screener).

## 11.5 2-Second Price Slope Algorithm
- 11.5.1 Defined as: (P_now - P_2s_ago)/2, used to adjust limit order price.

## 11.6 Trailing Stop Logic
- 11.6.1 For longs: stop = max(current price - X%), and must never decrease.
- 11.6.2 For shorts: stop = min(current price + X%), and must never increase.
- 11.6.3 X is configurable (default: 2%).

## 11.7 Multi-Timeframe Analysis
- 11.7.1 Must run on 1m, 5m, 15m (default) and multiply score by configurable factor if alignment found.

## 11.8 User Interface Decisions
- 11.8.1 First release must support GUI based configuration screen.

## 11.9 Error Identification and Logging
- 11.9.1 Use format “E#####” (e.g., E10001), log to file with timestamp and call stack.
- 11.9.2 Log rotation every 10MB or 7 days; file location configurable.

## 11.10 Documentation Requirement
- 11.10.1 Must include install guide, config wizard help, error ID list, trade logic references.

## 11.11 Quantifiable Language
- 11.11.1 Replace vague terms like “PhD-level” with exact indicators (e.g., regression forecasting, candle analysis).

# 12 Numbering Consistency
12.1 All section and subsection numbers must be strictly sequential. Any reserved numbers must be explained or removed.

# 13 Glossary of Trading Terms
13.1 A glossary must define all specialized terms or link to authoritative external references (e.g., “order block detection”, “regime state”).

# 15 Mobile and Remote Access (Deferred, Configurable)
- 15.1 The solution must expose a lightweight web-based or mobile-accessible interface (read-only in initial version) that allows the user to:
  - 15.1.1 View current portfolio positions and their scores
  - 15.1.2 View active orders and their status
  - 15.1.3 Receive push notifications or alerts for key events (e.g., errors, trades, risk conditions)
- 15.2 This interface must connect securely to the local system and must be disabled by default.
- 15.3 Authentication must be enforced before granting access to remote data.
- 15.4 Full trading functionality via remote access is deferred to a future version.

# 16 Crash Recovery and Resume Logic
- 16.1 The system must persist the following runtime state to disk every 30 seconds (configurable):
  - 16.1.1 Portfolio positions and scores
  - 16.1.2 Current active orders
  - 16.1.3 Execution cycle status and counters
- 16.2 Upon restart, the system must detect the presence of a saved state and prompt the user to:
  - 16.2.1 Resume previous session
  - 16.2.2 Start a clean session (with archive of prior state)
- 16.3 If live orders are present at restart, the system must re-fetch and reconcile them with internal state before any cycles are started.

# 17 Margin Monitoring and Account-Level Alerts (Upgraded and Decomposed)
17.1 The system shall query broker APIs every 60 seconds (configurable) to retrieve:
    17.1.1 Cash balance
    17.1.2 Maintenance margin available
    17.1.3 Margin usage percentage
17.2 If margin usage exceeds a configurable threshold (default: 80%):
    17.2.1 The system shall log the event with an `E#####` error code, timestamp, and details.
    17.2.2 The system shall display a persistent warning to the user until margin usage drops below the threshold.
    17.2.3 The system shall halt all new position entries until margin usage is below the threshold.
17.3 If broker API returns errors or stale data for more than 3 consecutive attempts:
    17.3.1 The system shall notify the user with a clear alert and log the event.
    17.3.2 The system shall skip the impacted cycle and attempt to recover in the next scheduled check.

# 18 Manual Override and Emergency Stop Functionality (Upgraded and Decomposed)
18.1 The user shall be able to activate `EMERGENCY STOP` via a key press or UI button, which:
    18.1.1 Cancels all open orders immediately
    18.1.2 Halts all execution cycles
    18.1.3 Prevents new trades from being submitted until trading is re-enabled by the user
18.2 The system shall confirm activation and deactivation of emergency stop via a user prompt or confirmation dialog.
18.3 Emergency stop state shall persist across restarts unless explicitly cleared by the user.

# 19 Automated Symbol Lifecycle Management (Upgraded and Decomposed)
19.1 The system shall periodically review symbols on the `persistent watchlist` for:
    19.1.1 10-day average volume below 10,000 (configurable)
    19.1.2 Zero price movement in past 5 days (configurable)
    19.1.3 Any broker error returned while fetching data for symbol
19.2 If a symbol matches any criteria above, it shall be flagged for deactivation.
19.3 Deactivated symbols shall:
    19.3.1 Be removed from active cycles
    19.3.2 Be tagged as "disabled" in the watchlist file (not deleted)
    19.3.3 Appear in a "flagged symbols" section in the UI
19.4 Users shall be able to manually re-activate a disabled symbol from the UI or watchlist file.

# 20 Market Hours and Edge Case Handling (Upgraded and Decomposed)
20.1 Before placing any order, the system shall:
    20.1.1 Determine if the market is open for the symbol’s exchange
    20.1.2 Prevent orders during pre-market/after-hours unless explicitly enabled
20.2 On holidays or early close days:
    20.2.1 Adjust execution cycle windows to match early close time
    20.2.2 Recalculate `Shrink Down Time Offset` and `Cutoff Time Offset` accordingly

# 21 Broker Disconnection and Retry Logic (Upgraded and Decomposed)
21.1 All broker API interactions shall use a retry mechanism:
    21.1.1 Retry failed API calls up to 3 times with exponential backoff
    21.1.2 If failure persists, log `E#####`, notify the user, and skip the impacted cycle

# 22 Position-Level Trade Journaling for Strategy Debugging (Upgraded and Decomposed)
22.1 For every executed trade, the system shall log a trade journal entry containing:
    22.1.1 Entry and exit timestamps
    22.1.2 Entry score and signal rationale
    22.1.3 Exit reason (e.g., TP hit, SL triggered, manual override)
    22.1.4 Related screenshots or indicator snapshots if configured
    22.1.5 Performance metrics: P&L, drawdown, slippage
22.2 Trade journal entries shall be both human-readable and machine-readable (CSV and JSON).

# 23 Broker Capability Validation Layer (Upgraded and Decomposed)
23.1 At startup, the system shall perform a capability check on the connected broker account for:
    23.1.1 Supported order types (e.g., bracket, trailing stop)
    23.1.2 Max open order and contract limits
    23.1.3 Required permissions for data access (e.g., real-time market data)
23.2 If any required capability is missing, the system shall warn the user before starting any cycle.

# 24 Risk-to-Reward Ratio Enforcement (Upgraded and Decomposed)
24.1 Each trade opportunity shall include a projected reward-to-risk ratio based on entry, take-profit, and stop-loss levels.
24.2 If R:R < configurable minimum (default: 1.5):
    24.2.1 Exclude the trade from execution queue
    24.2.2 Log as rejected opportunity with justification

## 24. Execution Mode-Driven Configuration
24.1 All environment variables and execution parameters must be set based on the current EXECUTION_MODE.
24.2 If EXECUTION_MODE is not explicitly supplied, it must default to "backtest".
24.3 The following execution modes are supported:
    - backtest
    - live
    - unit (for unit testing)
    - integration (for integration testing)
24.4 For each execution mode, the following environment variables and parameters must be set:
    - backtest:
        - No external dependencies required.
        - Use mock data sources.
    - live:
        - IBKR_HOST: Must be set to the Interactive Brokers host.
        - IBKR_PORT: Must be set to the Interactive Brokers port.
        - IBKR_CLIENT_ID: Must be set to a unique client ID.
    - unit:
        - Simulated environment with no external dependencies.
    - integration:
        - All external integrations must be active and validated.
        - IBKR_HOST, IBKR_PORT, and IBKR_CLIENT_ID must be set.
