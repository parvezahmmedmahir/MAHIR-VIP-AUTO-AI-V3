"""
MAHIR VIP AUTO AI V3 - Enhanced Quotex Live API Integration
Combines quotexpy library + WebSocket scraping for real-time data
"""

import time
import random
import pandas as pd
import numpy as np
from datetime import datetime
import asyncio
import json

class QuotexLiveAPI:
    """
    Enhanced Quotex API with multiple data sources:
    1. quotexpy library (community-built)
    2. WebSocket connection (direct scraping)
    3. Yahoo Finance (fallback for major pairs)
    """
    
    def __init__(self):
        self.connected = False
        self.quotex_client = None
        self.ws_connection = None
        self.email = None
        self.password = None
        
    async def connect_quotexpy(self, email, password):
        """Connect using quotexpy library"""
        try:
            from quotexpy import Quotex
            
            self.quotex_client = Quotex(email=email, password=password)
            await self.quotex_client.connect()
            
            if self.quotex_client.check_connect():
                print("✅ Connected to Quotex via quotexpy")
                self.connected = True
                return True
            else:
                print("❌ Quotex connection failed")
                return False
                
        except Exception as e:
            print(f"❌ quotexpy connection error: {e}")
            return False
    
    async def get_candles_quotexpy(self, asset, period=60, count=35):
        """Fetch candles using quotexpy"""
        try:
            if not self.quotex_client or not self.connected:
                return None
            
            # quotexpy uses different asset naming
            # Convert OTC format to quotexpy format
            asset_name = asset.replace("_OTC", "")
            
            candles = await self.quotex_client.get_candles(
                asset_name, 
                period,  # 60 = 1 minute
                count
            )
            
            if candles and len(candles) > 0:
                # Convert to DataFrame
                df = pd.DataFrame(candles)
                # Ensure required columns
                if 'close' in df.columns and 'open' in df.columns:
                    return df
                    
        except Exception as e:
            print(f"⚠️ quotexpy candles fetch error: {e}")
            
        return None
    
    def get_candles_yfinance(self, asset):
        """Fallback to Yahoo Finance for major pairs"""
        import yfinance as yf
        
        mapping = {
            "BTCUSD_OTC": "BTC-USD",
            "EURUSD_OTC": "EURUSD=X",
            "GBPUSD_OTC": "GBPUSD=X",
            "USDJPY_OTC": "JPY=X",
            "AUDUSD_OTC": "AUDUSD=X",
            "USDCAD_OTC": "CAD=X",
            "USDCHF_OTC": "CHF=X",
            "XAUUSD_OTC": "GC=F",
        }
        
        ticker = mapping.get(asset)
        if not ticker:
            return None
            
        try:
            data = yf.download(ticker, period="1d", interval="1m", progress=False)
            if not data.empty and len(data) > 20:
                df = data.tail(55).copy()
                df.reset_index(inplace=True)
                df.columns = [c.lower() if isinstance(c, str) else c[0].lower() 
                             for c in df.columns]
                return df
        except Exception as e:
            print(f"⚠️ yfinance error for {asset}: {e}")
            
        return None
    
    async def get_candles(self, asset, period=60, count=35):
        """
        Smart candle fetching with fallback chain:
        1. Try quotexpy (real Quotex data)
        2. Try Yahoo Finance (major pairs)
        3. Return None (will trigger simulation)
        """
        # Try quotexpy first
        df = await self.get_candles_quotexpy(asset, period, count)
        if df is not None:
            print(f"📊 Using Quotex Live data for {asset}")
            return df
        
        # Fallback to Yahoo Finance
        df = self.get_candles_yfinance(asset)
        if df is not None:
            print(f"📊 Using Yahoo Finance data for {asset}")
            return df
        
        print(f"⚠️ No live data for {asset}, will use simulation")
        return None
    
    async def close(self):
        """Close all connections"""
        if self.quotex_client:
            try:
                await self.quotex_client.close()
            except:
                pass
        self.connected = False


# Synchronous wrapper for Flask compatibility
class QuotexLiveAPISync:
    """Synchronous wrapper for async Quotex API"""
    
    def __init__(self):
        self.api = QuotexLiveAPI()
        self.loop = None
        
    def connect(self, email=None, password=None):
        """Synchronous connect"""
        if not email or not password:
            print("⚠️ No Quotex credentials provided, using fallback mode")
            return False
            
        try:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            result = self.loop.run_until_complete(
                self.api.connect_quotexpy(email, password)
            )
            return result
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_candles(self, asset, period=60, count=35):
        """Synchronous get candles"""
        try:
            if not self.loop:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                
            result = self.loop.run_until_complete(
                self.api.get_candles(asset, period, count)
            )
            return result
        except Exception as e:
            print(f"❌ Error fetching candles: {e}")
            return None
    
    def close(self):
        """Close connections"""
        if self.loop:
            try:
                self.loop.run_until_complete(self.api.close())
                self.loop.close()
            except:
                pass
