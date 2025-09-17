import json
import MetaTrader5 as mt5
import pubnub.pnconfiguration as PNconfig
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

from main import known_tickets

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

def is_new_trade():
    global known_tickets

    try:
        positions = mt5.positions_get()
        if positions is None :
            return False
        current_ticket = [pos.ticket for pos in positions]
        new_tickets = [x for x in current_ticket if x not in known_tickets]

        known_tickets = current_ticket

        return len(new_tickets) > 0

    except Exception as e:
        print(e)

def opentrade(data):
    data = json.loads(data)
    symbol = data["symbol"]

    price =mt5.symbol_info_tick(symbol).ask if data['type'] == "mt5.ORDER_TYPE_BUY" \
        else mt5.symbol_info_tick(symbol).bid
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": data['volume'],
        "type" : mt5.ORDER_TYPE_BUY if data['type'] == "mt5.ORDER_TYPE_BUY" else mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl" : data['sl'],
        "tp" : data['tp'],
        "deviation" : 10,
        "comment": "Python Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)


def main():
    # add a listener
    pubnub.add_listener(MySubscribeCallback())
    # ----Subscribe----
    pubnub.subscribe().channels(CHANNEL_NAME).execute()

    if not mt5.initialize():
        print("MT5 not initialized")

    try:
        while True:
            if trade_details is not None and is_new_trade():
                opentrade(trade_details)


    except KeyboardInterrupt:
        print("Exiting...")
    mt5.shutdown()


if __name__ == '__main__':
    main()