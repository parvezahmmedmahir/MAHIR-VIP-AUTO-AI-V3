MARKET_PAIRS = [
    # Major Forex Pairs (Real Data Available)
    "EURUSD_OTC", "GBPUSD_OTC", "USDJPY_OTC", "AUDUSD_OTC", "USDCAD_OTC", "USDCHF_OTC",
    "NZDUSD_OTC", "EURJPY_OTC", "GBPJPY_OTC", "AUDJPY_OTC", "NZDJPY_OTC",
    "EURGBP_OTC", "EURAUD_OTC", "AUDNZD_OTC", "NZDCAD_OTC", "CADCHF_OTC", "NZDCHF_OTC", "EURSGD_OTC",
    
    # Emerging Market Currencies (Real Data Available)
    "USDMXN_OTC", "USDBRL_OTC", "USDTRY_OTC", "USDZAR_OTC", "USDINR_OTC",
    "USDPHP_OTC", "USDIDR_OTC", "USDARS_OTC", "USDCOP_OTC", "USDPKR_OTC",
    "USDEGP_OTC", "USDNGN_OTC", "USDBDT_OTC", "USDDZD_OTC",
    
    # Cryptocurrencies (Real Data Available)
    "BTCUSD_OTC", "ETHUSD_OTC", "DOGE_OTC",
    
    # Meme Coins (Real Data Available)
    "SHIBA_OTC", "PEPE_OTC", "FLOKI_OTC", "BONK_OTC",
    
    # Meme Coins (No Real Data - Simulation Only)
    "TRUMP_OTC", "DOGWIF_OTC",
    
    # Major Stocks (Real Data Available)
    "MSFT_OTC", "BOEING_OTC", "MCD_OTC", "INTC_OTC", "AXP_OTC", "FB-OTC", "JOHNSON",
    
    # Major Indices (Real Data Available)
    "SP500_OTC", "DJIUSD_OTC", "FTSGBP_OTC", "F40EUR_OTC", "UKBR_OTC",
    
    # Precious Metals (Real Data Available)
    "XAUUSD_OTC", "XAGUSD_OTC",
    
    # Other Assets (Simulation Only)
    "USCR_OTC",  # US Crude Oil - ticker unclear
]

# Strategy Configuration
STRATEGY_CONFIG = {
    "name": "Three Black Crows",
    "timeframe": 60,  # 1 minute in seconds
    "safety_margin_percent": 0.15,
    "min_payout": 0.80
}
