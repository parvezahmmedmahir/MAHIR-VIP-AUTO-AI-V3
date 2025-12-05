import time
import random
import pandas as pd
import numpy as np
from datetime import datetime

class AssetPriceManager:
    """
    Manages the simulated price history for assets to ensure continuity and realism.
    """
    def __init__(self):
        self.price_history = {}
        
    def _initialize_asset(self, asset):
        """Initializes a random starting price and trend for an asset."""
        base_price = random.uniform(100, 1000)
        if "JPY" in asset: base_price = random.uniform(100, 150)
        elif "BTC" in asset: base_price = random.uniform(30000, 60000)
        
        self.price_history[asset] = {
            "current_price": base_price,
            "trend": random.choice([-1, 1]) * random.uniform(0.1, 0.5), # Initial trend
            "volatility": random.uniform(0.001, 0.005), # Volatility factor
            "history": [] # Keep track of last N candles for continuity
        }

    def get_next_candles(self, asset, amount=10, timeframe=60):
        if asset not in self.price_history:
            self._initialize_asset(asset)
            
        data = self.price_history[asset]
        candles = []
        
        current_time = time.time()
        
        # If we have no history, generate 'amount' candles backwards
        # If we have history, we might want to generate just one new one or refill the buffer
        # For this simple API, we will regenerate the last 'amount' candles based on the current state 
        # but adding some variation to simulate time passing if called repeatedly.
        
        # To make it feel "live", we advance the price slightly each time this is called
        current_price = data["current_price"]
        trend = data["trend"]
        volatility = data["volatility"]
        
        # Adjust trend slightly to simulate market cycles
        if random.random() < 0.1: # 10% chance to reverse or change trend strength
            trend += random.uniform(-0.1, 0.1)
            # Keep trend within reasonable bounds
            trend = max(min(trend, 1.0), -1.0)
            
        for i in range(amount):
             # Random Walk with Drift
            change_percent = np.random.normal(trend * 0.1, volatility)
            change = current_price * change_percent
            
            open_price = current_price
            close_price = current_price + change
            
            # Realistic High/Low generation
            # High is at least the max of open/close, plus some 'wick'
            # Low is at most the min of open/close, minus some 'wick'
            wick_up = abs(current_price * random.uniform(0, volatility))
            wick_down = abs(current_price * random.uniform(0, volatility))
            
            high_price = max(open_price, close_price) + wick_up
            low_price = min(open_price, close_price) - wick_down
            
            candles.append({
                "time": current_time - (amount - i) * timeframe,
                "open": open_price,
                "close": close_price,
                "high": high_price,
                "low": low_price,
                "volume": int(random.uniform(100, 5000))
            })
            
            current_price = close_price
            
        # Update state
        data["current_price"] = current_price
        data["trend"] = trend
        
        return pd.DataFrame(candles)

class QuotexAPI:
    def __init__(self):
        self.connected = False
        self.market_manager = AssetPriceManager()
        self.live_api = None
        self.use_live_api = False
        
    def connect(self, email=None, password=None):
        """
        Simple connection - No authentication required
        """
        print(f"🔌 Connecting to market data sources...")
        print("✅ System ready - Using Yahoo Finance + Simulation")
        self.connected = True
        self.use_live_api = False
        return True

    def get_ticker_from_asset(self, asset):
        """Maps OTC assets to real Yahoo Finance tickers where possible."""
        mapping = {
            # Major Forex Pairs
            "EURUSD_OTC": "EURUSD=X",
            "GBPUSD_OTC": "GBPUSD=X",
            "USDJPY_OTC": "JPY=X",
            "AUDUSD_OTC": "AUDUSD=X",
            "USDCAD_OTC": "CAD=X",
            "USDCHF_OTC": "CHF=X",
            "NZDUSD_OTC": "NZDUSD=X",
            "EURJPY_OTC": "EURJPY=X",
            "GBPJPY_OTC": "GBPJPY=X",
            "AUDJPY_OTC": "AUDJPY=X",
            "NZDJPY_OTC": "NZDJPY=X",
            "EURGBP_OTC": "EURGBP=X",
            "EURAUD_OTC": "EURAUD=X",
            "AUDNZD_OTC": "AUDNZD=X",
            "NZDCAD_OTC": "NZDCAD=X",
            "CADCHF_OTC": "CADCHF=X",
            "NZDCHF_OTC": "NZDCHF=X",
            "EURSGD_OTC": "EURSGD=X",
            
            # Emerging Market Currencies
            "USDMXN_OTC": "MXN=X",      # Mexican Peso
            "USDBRL_OTC": "BRL=X",      # Brazilian Real
            "USDTRY_OTC": "TRY=X",      # Turkish Lira
            "USDZAR_OTC": "ZAR=X",      # South African Rand
            "USDINR_OTC": "INR=X",      # Indian Rupee
            "USDPHP_OTC": "PHP=X",      # Philippine Peso
            "USDIDR_OTC": "IDR=X",      # Indonesian Rupiah
            "USDARS_OTC": "ARS=X",      # Argentine Peso
            "USDCOP_OTC": "COP=X",      # Colombian Peso
            "USDPKR_OTC": "PKR=X",      # Pakistani Rupee
            "USDEGP_OTC": "EGP=X",      # Egyptian Pound
            "USDNGN_OTC": "NGN=X",      # Nigerian Naira
            "USDBDT_OTC": "BDT=X",      # Bangladeshi Taka
            "USDDZD_OTC": "DZD=X",      # Algerian Dinar
            
            # Cryptocurrencies (Major)
            "BTCUSD_OTC": "BTC-USD",
            "ETHUSD_OTC": "ETH-USD",
            "DOGE_OTC": "DOGE-USD",
            
            # Meme Coins / Altcoins
            "SHIBA_OTC": "SHIB-USD",    # Shiba Inu
            "PEPE_OTC": "PEPE-USD",     # Pepe
            "FLOKI_OTC": "FLOKI-USD",   # Floki
            "BONK_OTC": "BONK-USD",     # Bonk
            # Note: TRUMP, DOGWIF may not have Yahoo Finance tickers
            
            # Precious Metals
            "XAUUSD_OTC": "GC=F",       # Gold Futures
            "XAGUSD_OTC": "SI=F",       # Silver Futures
            
            # Major Indices
            "SP500_OTC": "^GSPC",       # S&P 500
            "DJIUSD_OTC": "^DJI",       # Dow Jones
            "FTSGBP_OTC": "^FTSE",      # FTSE 100
            "F40EUR_OTC": "^FCHI",      # CAC 40 (France)
            "UKBR_OTC": "^BVSP",        # Brazil Bovespa
            
            # Major Stocks
            "MSFT_OTC": "MSFT",         # Microsoft
            "BOEING_OTC": "BA",         # Boeing
            "MCD_OTC": "MCD",           # McDonald's
            "INTC_OTC": "INTC",         # Intel
            "AXP_OTC": "AXP",           # American Express
            "FB-OTC": "META",           # Meta (Facebook)
            "JOHNSON": "JNJ",           # Johnson & Johnson
            # Note: USCR ticker unclear, might be US Crude Oil
        }
        return mapping.get(asset, None)

    def get_candles(self, asset, timeframe, amount=20):
        """
        Enhanced candle fetching with intelligent fallback optimized for Quotex OTC:
        1. Quotex Live API (if enabled)
        2. Yahoo Finance (for major pairs) - with retry and validation
        3. Internal Simulation (fallback with realistic data)
        """
        # Priority 1: Try Quotex Live API
        if self.use_live_api and self.live_api:
            try:
                df = self.live_api.get_candles(asset, timeframe, amount + 20)
                if df is not None and len(df) > 20:
                    print(f"📊 Using Quotex Live data for {asset}")
                    return df
            except Exception as e:
                print(f"⚠️ Live API fetch error: {e}")
        
        # Priority 2: Try Yahoo Finance with retry logic
        import yfinance as yf
        ticker = self.get_ticker_from_asset(asset)
        
        if ticker:
            # Try up to 2 times for Yahoo Finance (network issues)
            for attempt in range(2):
                try:
                    data = yf.download(
                        ticker, 
                        period="1d", 
                        interval="1m", 
                        progress=False,
                        timeout=10  # 10 second timeout
                    )
                    
                    # Validate data quality
                    if not data.empty and len(data) > 20:
                        df = data.tail(amount + 20).copy()
                        df.reset_index(inplace=True)
                        
                        # Normalize column names
                        df.columns = [c.lower() if isinstance(c, str) else c[0].lower() 
                                     for c in df.columns]
                        
                        # Validate required columns
                        required_cols = ['open', 'high', 'low', 'close', 'volume']
                        if all(col in df.columns for col in required_cols):
                            # Check for valid price data (no zeros or NaN)
                            if df['close'].notna().all() and (df['close'] > 0).all():
                                print(f"📊 Using Yahoo Finance data for {asset}")
                                return df
                        
                except Exception as e:
                    if attempt == 0:
                        print(f"⚠️ Yahoo Finance attempt {attempt + 1} failed: {e}, retrying...")
                        continue
                    else:
                        print(f"⚠️ Yahoo Finance error after {attempt + 1} attempts: {e}")
        
        # Priority 3: Fallback to enhanced simulation
        print(f"📊 Using enhanced simulation data for {asset}")
        return self.market_manager.get_next_candles(asset, amount, timeframe)

    def analyze_market(self, asset, risk_level="safe"):
        """
        Advanced market analysis optimized for Quotex OTC markets.
        Uses multiple confirmation indicators for high-quality signals.
        Modes: 'safe' (High accuracy, 85%+ confidence), 'aggressive' (More signals, 70%+ confidence)
        """
        if not self.connected:
            self.connect()
            
        # Fetch recent candles with extra buffer for indicators
        df = self.get_candles(asset, 60, 40) 
        
        # Calculate multiple technical indicators
        df['SMA_20'] = df['close'].rolling(window=20).mean()
        df['SMA_50'] = df['close'].rolling(window=50).mean() if len(df) >= 50 else df['SMA_20']
        df['EMA_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['RSI'] = self.calculate_rsi(df['close'], 14)
        
        # Calculate volatility (ATR - Average True Range)
        df['high_low'] = df['high'] - df['low']
        df['high_close'] = abs(df['high'] - df['close'].shift())
        df['low_close'] = abs(df['low'] - df['close'].shift())
        df['tr'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
        df['ATR'] = df['tr'].rolling(window=14).mean()
        
        # Volume analysis (if available)
        has_volume = 'volume' in df.columns and df['volume'].sum() > 0
        if has_volume:
            df['volume_sma'] = df['volume'].rolling(window=20).mean()
        
        # Get last 3 candles for pattern analysis
        last_3 = df.tail(3)
        closes = last_3['close'].values
        opens = last_3['open'].values
        highs = last_3['high'].values
        lows = last_3['low'].values
        
        # Current market state
        current_price = df.iloc[-1]['close']
        sma_20 = df.iloc[-1]['SMA_20']
        sma_50 = df.iloc[-1]['SMA_50']
        ema_12 = df.iloc[-1]['EMA_12']
        rsi = df.iloc[-1]['RSI']
        atr = df.iloc[-1]['ATR']
        
        # Calculate trend strength
        trend_strength = abs(current_price - sma_20) / current_price * 100
        
        # Initialize signal variables
        signal = None
        confidence = 0
        strategy_name = "Market Analysis"
        confirmations = []  # Track confirmation signals

        # === PATTERN DETECTION ===
        
        # 1. Three Black Crows (Strong Bearish Pattern)
        is_three_black_crows = all(row['close'] < row['open'] for _, row in last_3.iterrows())
        is_descending = closes[0] > closes[1] > closes[2]
        strong_bearish_pattern = is_three_black_crows and is_descending

        # 2. Three White Soldiers (Strong Bullish Pattern)
        is_three_white_soldiers = all(row['close'] > row['open'] for _, row in last_3.iterrows())
        is_ascending = closes[0] < closes[1] < closes[2]
        strong_bullish_pattern = is_three_white_soldiers and is_ascending
        
        # === SIGNAL GENERATION WITH MULTI-INDICATOR CONFIRMATION ===
        
        # SIGNAL 1: Three Black Crows (Bearish)
        if strong_bearish_pattern:
            signal = "PUT"
            strategy_name = "Three Black Crows (Bearish)"
            
            # Base confidence
            confidence = 82
            confirmations.append("Three Black Crows pattern")
            
            # Calculate pattern strength
            body_sizes = [abs(row['close'] - row['open']) for _, row in last_3.iterrows()]
            avg_body = sum(body_sizes) / len(body_sizes)
            price_drop = ((closes[0] - closes[2]) / closes[0]) * 100
            
            # Bonus: Large candle bodies (strong momentum)
            if avg_body > current_price * 0.005:
                confidence += 5
                confirmations.append("Strong bearish momentum")
            
            # Bonus: Steep price decline
            if price_drop > 0.5:
                confidence += 4
                confirmations.append("Steep price decline")
            
            # Bonus: RSI confirmation (overbought)
            if rsi > 60:
                confidence += 4
                confirmations.append("RSI overbought")
            
            # Bonus: Price below SMA (downtrend)
            if current_price < sma_20:
                confidence += 3
                confirmations.append("Below SMA trend")
            
            # Bonus: Volume confirmation (if available)
            if has_volume and df.iloc[-1]['volume'] > df.iloc[-1]['volume_sma']:
                confidence += 2
                confirmations.append("High volume")
                
            confidence = min(confidence, 98)
            
        # SIGNAL 2: Three White Soldiers (Bullish)
        elif strong_bullish_pattern:
            signal = "CALL"
            strategy_name = "Three White Soldiers (Bullish)"
            
            # Base confidence
            confidence = 82
            confirmations.append("Three White Soldiers pattern")
            
            # Calculate pattern strength
            body_sizes = [abs(row['close'] - row['open']) for _, row in last_3.iterrows()]
            avg_body = sum(body_sizes) / len(body_sizes)
            price_rise = ((closes[2] - closes[0]) / closes[0]) * 100
            
            # Bonus: Large candle bodies
            if avg_body > current_price * 0.005:
                confidence += 5
                confirmations.append("Strong bullish momentum")
            
            # Bonus: Steep price rise
            if price_rise > 0.5:
                confidence += 4
                confirmations.append("Steep price rise")
            
            # Bonus: RSI confirmation (oversold)
            if rsi < 40:
                confidence += 4
                confirmations.append("RSI oversold")
            
            # Bonus: Price above SMA (uptrend)
            if current_price > sma_20:
                confidence += 3
                confirmations.append("Above SMA trend")
            
            # Bonus: Volume confirmation
            if has_volume and df.iloc[-1]['volume'] > df.iloc[-1]['volume_sma']:
                confidence += 2
                confirmations.append("High volume")
                
            confidence = min(confidence, 98)
            
        # SIGNAL 3: RSI Extreme Reversals
        elif rsi < 25:  # Strong Oversold
            signal = "CALL"
            strategy_name = "RSI Oversold Reversal"
            confirmations.append("Extreme RSI oversold")
            
            # Base confidence from RSI extremity
            confidence = 72 + int((25 - rsi) * 2.5)
            
            # Bonus: Price near support (SMA)
            if abs(current_price - sma_20) / current_price < 0.01:
                confidence += 5
                confirmations.append("Near SMA support")
            
            # Bonus: Bullish divergence (price falling but RSI rising)
            if len(df) > 5:
                prev_rsi = df.iloc[-5]['RSI']
                prev_price = df.iloc[-5]['close']
                if rsi > prev_rsi and current_price < prev_price:
                    confidence += 6
                    confirmations.append("Bullish divergence")
            
            confidence = min(confidence, 93)
            
        elif rsi > 75:  # Strong Overbought
            signal = "PUT"
            strategy_name = "RSI Overbought Reversal"
            confirmations.append("Extreme RSI overbought")
            
            # Base confidence from RSI extremity
            confidence = 72 + int((rsi - 75) * 2.5)
            
            # Bonus: Price near resistance (SMA)
            if abs(current_price - sma_20) / current_price < 0.01:
                confidence += 5
                confirmations.append("Near SMA resistance")
            
            # Bonus: Bearish divergence
            if len(df) > 5:
                prev_rsi = df.iloc[-5]['RSI']
                prev_price = df.iloc[-5]['close']
                if rsi < prev_rsi and current_price > prev_price:
                    confidence += 6
                    confirmations.append("Bearish divergence")
            
            confidence = min(confidence, 93)
            
        # SIGNAL 4: SMA Trend Following (Aggressive mode only)
        elif risk_level == "aggressive":
            price_distance = abs(current_price - sma_20) / current_price * 100
            
            # Strong uptrend
            if current_price > sma_20 and price_distance > 0.15 and current_price > ema_12:
                signal = "CALL"
                strategy_name = "SMA Bullish Trend"
                confirmations.append("Strong uptrend")
                
                # Base confidence from trend strength
                confidence = 68 + int(price_distance * 25)
                
                # Bonus: EMA confirmation
                if ema_12 > sma_20:
                    confidence += 5
                    confirmations.append("EMA alignment")
                
                # Bonus: RSI in bullish zone
                if 40 < rsi < 70:
                    confidence += 4
                    confirmations.append("RSI bullish zone")
                
                confidence = min(confidence, 84)
                
            # Strong downtrend
            elif current_price < sma_20 and price_distance > 0.15 and current_price < ema_12:
                signal = "PUT"
                strategy_name = "SMA Bearish Trend"
                confirmations.append("Strong downtrend")
                
                # Base confidence from trend strength
                confidence = 68 + int(price_distance * 25)
                
                # Bonus: EMA confirmation
                if ema_12 < sma_20:
                    confidence += 5
                    confirmations.append("EMA alignment")
                
                # Bonus: RSI in bearish zone
                if 30 < rsi < 60:
                    confidence += 4
                    confirmations.append("RSI bearish zone")
                
                confidence = min(confidence, 84)

        # === APPLY RISK LEVEL FILTERS ===
        if risk_level == "safe":
            MIN_CONFIDENCE = 85  # Only very strong signals
            MIN_CONFIRMATIONS = 2  # At least 2 confirmations
        else:  # aggressive
            MIN_CONFIDENCE = 70  # Allow weaker signals
            MIN_CONFIRMATIONS = 1  # At least 1 confirmation
            
        # Filter by confidence and confirmations
        if confidence < MIN_CONFIDENCE or len(confirmations) < MIN_CONFIRMATIONS:
            signal = "WAIT"
            confidence = 0
            confirmations = []
            
        return {
            "asset": asset,
            "signal": signal,
            "confidence": confidence,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "strategy": strategy_name,
            "confirmations": confirmations,  # New: List of confirmation signals
            "market_status": "Real Market" if self.get_ticker_from_asset(asset) else "OTC Simulation",
            "trend_strength": round(trend_strength, 2) if signal != "WAIT" else 0,
            "rsi_value": round(rsi, 1) if signal != "WAIT" else 0
        }

    def calculate_rsi(self, prices, period=14):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Avoid division by zero
        loss = loss.replace(0, 0.00001)
        
        rs = gain / loss
        return 100 - (100 / (1 + rs))

# Singleton instance
api = QuotexAPI()
