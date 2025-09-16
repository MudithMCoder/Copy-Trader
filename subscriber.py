import sys
import pubnub.pnconfiguration as PNconfig
from pubnub.pubnub import PubNub
from pubnub.callbacks import SubscribeCallback

#---Configurations---
PUBLISH_KEY = "pub-c-56b4bb05-1e9f-4d36-8a00-b51f771a88c9"
SUBSCRIBE_KEY = "sub-c-37cc5202-f856-4457-b564-1a1c8354d6fa"
CHANNEL_NAME = "trade.broadcast.room1"

pnconfig = PNconfig.PNConfiguration()
pnconfig.publish_key = PUBLISH_KEY
pnconfig.subscribe_key = SUBSCRIBE_KEY
pnconfig.uuid = "device-01"
pubnub = PubNub(pnconfig)

#---Listener---
class MySubscribeCallback(SubscribeCallback):
    def message(self, pubnub, event):
        print(f"[{pnconfig.uuid}] Received message: {event.message}")


def recieve_message():

    #add a listener
    pubnub.add_listener(MySubscribeCallback())
    # ----Subscribe----
    pubnub.subscribe().channels([CHANNEL_NAME]).execute()
    print(f"Subscriber {pnconfig.uuid} listening on channel {CHANNEL_NAME}")


def main():
    recieve_message()

if __name__ == '__main__':
    main()