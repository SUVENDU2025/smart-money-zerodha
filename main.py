from kiteconnect import KiteConnect
import requests
import time
import logging
import os
from datetime import datetime

# Telegram Bot Configuration
TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"

# Zerodha API Credentials
API_KEY = "cr7m80yyp4lsny3b"
ACCESS_TOKEN = "rqIk1AFNM0x6ntXg67VUkXr2wef3cxFI"

kite = KiteConnect(api_key=API_KEY)
kite.set_access_token(ACCESS_TOKEN)

# Telegram alert function
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram Error:", e)

# Smart money logic
def scan_strikes():
    instruments = kite.instruments("NSE")
    indexes = ["NIFTY", "BANKNIFTY"]

    for index in indexes:
        try:
            quote = kite.ltp(f"NSE:{index}")[f"NSE:{index}"]['last_price']
            atm = round(quote / 100) * 100
            strikes = [atm - 100, atm, atm + 100]

            for strike in strikes:
                for option_type in ['CE', 'PE']:
                    symbol = f"{index}25JUL{strike}{option_type}"
                    try:
                        data = kite.ltp(f"NFO:{symbol}")
                        price = data[f"NFO:{symbol}"]["last_price"]
                        oi = kite.quote(f"NFO:{symbol}")["NFO:" + symbol]["oi"]
                        volume = kite.quote(f"NFO:{symbol}")["NFO:" + symbol]["volume"]
                        
                        if 30 <= price <= 50:
                            msg = f"📡 Smart Money Alert [{index}]\nStrike: {strike}{option_type}\nPrice: ₹{price}\nOI: {oi}\nVol: {volume}\n⏱ {datetime.now().strftime('%H:%M:%S')}"
                            send_telegram_message(msg)
                    except:
                        pass
        except Exception as e:
            print(f"Error with {index}: {e}")

# Main loop
if __name__ == "__main__":
    while True:
        scan_strikes()
        time.sleep(600)  # Run every 10 minutes
