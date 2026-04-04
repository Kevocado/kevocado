# Hey, I'm Kevin 👋

I'm a software engineer passionate about **quantitative finance**, **algorithmic trading**, and **AI-driven automation**. I build production systems that sit at the intersection of machine learning, market data, and real-world deployment.

- 🏦 Currently building automated trading systems and prediction-market edge finders
- 🤖 Interested in agentic AI workflows, LLM-powered automation, and quant research
- 📚 CS student at the University of Illinois Urbana-Champaign
- 📫 Reach me at **sigeykevin@gmail.com**

---

<!-- TOP-REPOS-START -->

## 🏆 Featured Projects

*Auto-ranked by total commit count · updated weekly by GitHub Actions*

### 🥇 [OpenClaw-Applicant-Bot](https://github.com/Kevocado/OpenClaw-Applicant-Bot)

Autonomous job-application agent that fills and submits forms across job boards with human-in-the-loop approval for top-tier companies.

**Stack:** Python · Docker · n8n · Playwright · Gemini Pro

- Distributed architecture: VPS gateway + macOS Playwright execution node over Tailscale
- Tier-based routing: auto-submit for standard roles, Telegram gatekeeper for MBB/Big-4
- Resume & cover-letter knowledge base fed to Gemini Pro for context-aware form filling
- Google Sheets integration for real-time application tracking

*135 commits*

---

### 🥈 [SP500-Predictor](https://github.com/Kevocado/SP500-Predictor)

Prediction-market edge finder for Kalshi (SPX, QQQ, BTC, ETH) combining LightGBM ML models, multi-source sentiment analysis, and a Bloomberg-style Streamlit dashboard.

**Stack:** Python · Streamlit · LightGBM · Azure · Hugging Face

- Auto-retraining LightGBM regressors on feature drift for hourly and daily horizons
- Cloud model delivery via Hugging Face Hub; logs stored in Azure Blob Storage
- Composite sentiment scoring: Crypto Fear & Greed, VIX-derived, and price momentum
- Cross-venue arbitrage detection between Kalshi and PredictIt (>5% delta threshold)

*123 commits*

---

### 🥉 [algo-trade-hub-prod](https://github.com/Kevocado/algo-trade-hub-prod)

Production quantitative trading monorepo that discovers arbitrage edges in prediction markets using weather, macro, crypto, and sports data pipelines.

**Stack:** Python · React · Vite · Supabase · PM2

- Hybrid architecture: Python daemon on VPS writes to Supabase; React terminal UI on Vercel reads it
- Covers Kalshi weather, macro (FRED), crypto momentum, and FPL sports arbitrage engines
- PM2 process management for resilient background scanning every 30 seconds
- Strict secret split: high-clearance backend tokens vs. public VITE_ frontend config

*40 commits*

---

### 4️⃣ [Stable-Coin-Analysis](https://github.com/Kevocado/Stable-Coin-Analysis)

On-chain stablecoin analytics project studying cross-border remittance flows between Global North and South exchanges using BigQuery public blockchain data.

**Stack:** SQL (BigQuery) · Python

- Queries USDT/USDC on-chain transfer data to compare L1 vs L2 remittance costs
- Geographic exchange classification (Global North vs South) for flow analysis
- Transfer-size histogram and stablecoin-preference breakdowns by region
- Collaborative project with University of Illinois CS team

*18 commits*

---

<!-- TOP-REPOS-END -->

## 🛠 Tech I Work With

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat&logo=postgresql&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoftazure&logoColor=white)

---

## 📬 Contact & Links

| | |
|---|---|
| GitHub | [@Kevocado](https://github.com/Kevocado) |
| Email | [sigeykevin@gmail.com](mailto:sigeykevin@gmail.com) |
