# IBKR IT Assets Report

The below is a report of all applications, API, systems and components that may fullfill requirements of the project.
It is important to analyze this content before attempting to provide an architecture, design or implementation of the system.
# A. Integration Capabilities
•	Client Portal (Web) API
Modern RESTful API with OAuth and WebSocket support for trading, positions, balances, and real-time updates
•	Trader Workstation (TWS) API
Desktop-based API with support for Java, Python, C++, C#, Excel; enables real-time data, order entry, and account access
•	FIX API
High-performance FIX protocol for institutional traders to place orders via extranet or direct connection (no market data)
•	Market Data Feeds
Subscribe to real-time and historical data via API (WebSocket/REST) – requires exchange-specific permissions
## 🌐 IBKR API Reference URLs

Below is a list of publicly available IBKR API resources:

1. **Client Portal Web API (REST/WebSocket)**  
   Full Docs: https://ibkrguides.com/releasenotes/api/cp-web/latest-2023.htm  
   Base API URL: https://api.ibkr.com  

2. **Trader Workstation (TWS) API (Socket-based)**  
   API Overview: https://www.interactivebrokers.com/en/trading/ib-api.php  
   TWS API Guide: https://interactivebrokers.github.io/tws-api/interfaceIBApi_1_1EWrapper.html  

3. **Web API v1.0 (CP Web API)**  
   Documentation: https://www.interactivebrokers.com/campus/ibkr-api-page/cpapi-v1/  

4. **FIX API (Financial Information eXchange Protocol)**  
   FIX Info: https://www.interactivebrokers.com/en/trading/ib-api.php  

5. **Excel / RTD / ActiveX / DDE API**  
   Excel Integration Overview: https://www.interactivebrokers.com/en/trading/ib-api.php  
   Additional Docs: https://interactivebrokers.github.io/cpwebapi/  

# B. Customer-Facing Features
•	IBKR Desktop, TWS, Web & Mobile Platforms
Comprehensive suite of platforms for beginners to professionals across all devices
•	GlobalAnalyst Screener
Advanced global stock screening based on valuation, region, and metrics
•	Fundamentals Explorer
Explore 30,000+ global companies with deep financials, ESG, news and analyst insights
•	Client Portal & PortfolioAnalyst
One-stop trading, account management, performance analytics and custom reports
•	Account Funding & Onboarding
Multiple deposit/withdrawal methods, account setup guidance, demo access
