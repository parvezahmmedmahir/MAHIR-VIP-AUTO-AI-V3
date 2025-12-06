
# MAHIR VIP AUTO AI V3 - Configuration

# Network Settings
HOST = "0.0.0.0"
PORT = 5000
DEBUG_MODE = True

# Strategy Settings
STRATEGY_CONFIG = {
    "name": "Three Black Crows / White Soldiers",
    "timeframe": 60,  # 1 minute candles
    "min_confidence": 80,
    "risk_level": "medium" # dry, safe, aggressive
}

# Supported Market Pairs (Strict Customer List)
MARKET_PAIRS = [
    "NZDCAD_OTC", "USDEGP_OTC", "USDCHF_OTC", "USDBRL_OTC", "AUDNZD_OTC",
    "BOEING_OTC", "FB-OTC", "USDPHP_OTC", "USDIDR_OTC", "USDNGN_OTC",
    "DJIUSD_OTC", "USDBDT_OTC", "USDARS_OTC", "USDMXN_OTC", "F40EUR_OTC",
    "USDTRY_OTC", "FTSGBP_OTC", "USDPKR_OTC", "USDINR_OTC", 
    "NZDCHF_OTC", "CADCHF_OTC", "NZDJPY_OTC", "USDCOP_OTC", "AUDNZD_OTC",
    "SHIBA_OTC", "PEPE_OTC", "TRUMP_OTC", "DOGWIF_OTC", "BONK_OTC",
    "FLOKI_OTC", "DOGE_OTC", "UKBR_OTC", "MSFT_OTC", "EURSGD_OTC",
    "USDDZD_OTC", "BTCUSD_OTC", "XAGUSD_OTC", "XAUUSD_OTC", "INTC_OTC", 
    "MCD_OTC", "USCR_OTC", "USDZAR_OTC", "USDCOP_OTC", "AXP_OTC",
    "NZDCHF_OTC", "JOHNSON"
]