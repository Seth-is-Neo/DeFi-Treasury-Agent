# main.py
import time
import json
from core.rebalancer import rebalancer
from execution import dex_interface
from execution.rl_agent import apply_rl
from stable_baselines3 import PPO

class Pool:
    def __init__(self, pair, dex, chain):
        self.pair = pair
        self.dex = dex
        self.chain = chain
        self.tvl = 1_500_000
        self.volume = 50_000
        self.holders = 200
        self.rep_score = 8
        self.bayesian_score = 8
        self.lp_allocation = 50_000
        self.volatility = 0.05
        self.expected_fee = 500
        self.actual_fee = 480
        self.impermanent_loss = 20
        self.realized_profit = 450
        self.price_vs_twap = 1.0
        self.estimated_gas_cost = 20
        self.alert_flag = False

# Initialize pools
pool_data = [
    Pool("ETH/USDC", "Uniswap", "Ethereum"),
    Pool("MATIC/USDC", "SushiSwap", "Polygon"),
    Pool("HBAR/USDC", "HederaDEX", "Hedera")
]

# Load RL model if exists
try:
    rl_model = PPO.load("rl_treasury_agent")
except:
    rl_model = None

DRY_RUN = True  # Shadow mode toggle

def save_pool_data(pool_data):
    data = [vars(p) for p in pool_data]
    with open("pool_data.json", "w") as f:
        json.dump(data, f, indent=4)

# Main loop
while True:
    for pool in pool_data:
        if DRY_RUN:
            pool.price_vs_twap = 1.0

    pool_data = rebalancer(pool_data, rl_model=rl_model)

    for pool in pool_data:
        print(f"[EXECUTE] {pool.lp_allocation} allocated to {pool.pair} on {pool.dex} ({pool.chain})")
        if not DRY_RUN:
            if pool.tvl >= 1_000_000 and pool.rep_score >= 7:
                dex_interface.execute_lp(pool)
                if pool.chain == "Hedera":
                    dex_interface.settle_hedera_profit(pool, pool.realized_profit)

    save_pool_data(pool_data)
    time.sleep(5)
