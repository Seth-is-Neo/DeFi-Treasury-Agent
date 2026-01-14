# AI Treasury Agent (Shadow Mode)

This repository contains a **Python-based AI Treasury Agent** for multi-chain DeFi liquidity management.  

It supports:

- Shadow-mode LP allocations for Ethereum, Polygon, and Hedera.
- Multi-chain Bayesian + RL-based decision making.
- Live dashboard with scores, LP allocations, ROI, impermanent loss, and fees.
- Fully autonomous JSON-based data sharing between engine and dashboard.

---

## **Getting Started**

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd ai_treasury

# Create virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run the dashboard
python -m dashboard.dashboard


#Open your browser at http://127.0.0.1:8050 to view the dashboard.

# Run the shadow-mode engine

#In a second terminal:

venv\Scripts\activate
python main.py


#main.py updates pool_data.json every 5 seconds.

#Dashboard reads the file automatically to show live LP allocations and scores.

#Commands and Usage

#Change shadow mode toggle in main.py:

DRY_RUN = True   # True = shadow mode, False = live execution


#Modify pools in main.py:

pool_data = [Pool("ETH/USDC","Uniswap","Ethereum"), ...]


#Dashboard filters:

Chain dropdown: All / Ethereum / Polygon / Hedera

DEX dropdown: All / Uniswap / SushiSwap / HederaDEX
