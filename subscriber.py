import json
import MetaTrader5 as mt5
import pubnub.pnconfiguration as PNconfig
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback
import time


#---Configurations---
PUBLISH_KEY = "pub-c-56b4bb05-1e9f-4d36-8a00-b51f771a88c9"
SUBSCRIBE_KEY = "sub-c-37cc5202-f856-4457-b564-1a1c8354d6fa"
CHANNEL_NAME = "trade.broadcast.room1"

pnconfig = PNconfig.PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY
pnconfig.uuid = "device-01"
pubnub = PubNub(pnconfig)

trade_details = None
known_tickets = list()
#---Listener---
class MySubscribeCallback(SubscribeCallback):
    def message(self,pubnub,event):
        global trade_details
        trade_details = event.message
        print(f"[{pnconfig.uuid}] Received message: {event.message}")
        self.opentrade(trade_details)

    def opentrade(self,data):
        data = json.loads(data)
        symbol = data["symbol"]

        price = mt5.symbol_info_tick(symbol).ask if data['type'] == "mt5.ORDER_TYPE_BUY" \
            else mt5.symbol_info_tick(symbol).bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": data['volume'],
            "type": mt5.ORDER_TYPE_BUY if data['type'] == "mt5.ORDER_TYPE_BUY" else mt5.ORDER_TYPE_SELL,
            "price": price,
            "sl": data['sl'],
            "tp": data['tp'],
            "deviation": 10,
            "comment": "Python Order",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        print(result)


def main():
    if not mt5.initialize():
        print("MT5 not initialized")
    # add a listener
    pubnub.add_listener(MySubscribeCallback())
    # ----Subscribe----
    pubnub.subscribe().channels(CHANNEL_NAME).execute()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")

    mt5.shutdown()

if __name__ == '__main__':
    main()