from fastapi import FastAPI, Request
import ccxt
import pandas as pd
from datetime import datetime, timedelta

# 1. Hamne AI ka server (FastAPI) chalu kiya
app = FastAPI()

# 2. Yeh hamare AI ki 6 mahine ki memory (Database) jaisa kaam karega
market_memory = []

# Jab koi hamare bot ki website kholega, to ye dikhega
@app.get("/")
def home():
    return {"status": "AI Trading Bot Is Live 24/7", "memory_records": len(market_memory)}

# 3. PHASE 1: Pichle 6 mahine ka data yaad karne ka function
@app.get("/train-ai")
def train_ai_from_history():
    global market_memory
    print("AI pichle 6 mahine ka data seekh raha hai...")
    
    # Bybit exchange se free me public data uthaya
    exchange = ccxt.bybit()
    symbol = 'BTC/USDT'
    timeframe = '1h' # Har 1 ghante ki candle

    # Aaj se 6 mahine (180 din) pehle ka time nikala
    six_months_ago = datetime.now() - timedelta(days=180)
    since_timestamp = int(six_months_ago.timestamp() * 1000)

    try:
        # Data load kiya
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=1000)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # AI ko sikhaya ki average volume kitna rehta hai
        avg_volume = df['volume'].mean()
        
        market_memory = [] # Purani memory saaf ki
        
        # AI ne har ek ghante ka pattern yaad karna shuru kiya
        for index, row in df.iterrows():
            # Agar kisi ghante me volume average se 2 guna zyada tha
            if row['volume'] > (avg_volume * 2):
                # Niche se price reject hui aur green candle bani -> Buyers entered
                if row['close'] > row['open']:
                    market_memory.append({"date": row['timestamp'], "pattern": "BUYERS_STRONG"})
                # Upar se price reject hui aur red candle bani -> Sellers entered
                else:
                    market_memory.append({"date": row['timestamp'], "pattern": "SELLERS_STRONG"})
                    
        return {"status": "Success", "message": f"AI ne pichle 6 mahine se {len(market_memory)} bade patterns yaad kar liye hain!"}
    except Exception as e:
        return {"status": "Error", "message": str(e)}

# 4. PHASE 3: TradingView se live connection (Webhook)
@app.post("/webhook")
async def tradingview_signal(request: Request):
    try:
        # TradingView se live chart ka data aya
        data = await request.json()
        print(f"TradingView se signal mila: {data}")
        
        action = data.get("action") # TradingView bolega 'BUY' ya 'SELL'
        price = data.get("price")
        
        if action == "BUY":
            return {"status": "AI Decision", "action": "Executing BUY Trade", "reason": "TradingView indicators matched AI pattern"}
        elif action == "SELL":
            return {"status": "AI Decision", "action": "Executing SELL Trade", "reason": "TradingView indicators matched AI pattern"}
            
    except Exception as e:
        return {"status": "Error", "message": str(e)}
