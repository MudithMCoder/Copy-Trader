import MetaTrader5 as mt5
import json

#global variables
known_tickets = list()

def position_ticket() :
    try:
        positions = mt5.positions_get()

        if positions :
            position = positions[0]
            ticket = position.ticket

            if ticket  > 1 :
                return ticket
            else :
                return 0
    except Exception as e:
        print(e)

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


def positions_get():
    try:
        positions = mt5.positions_get()


        if positions :
            positions = positions[len(positions)-1]

            trade_data = {
                "symbol": positions.symbol,
                "volume": positions.volume,
                "sl": positions.sl,
                "tp": positions.tp,
                "trade_type": positions.type
            }

            json_data = json.dumps(trade_data)
            return json_data
    except Exception as e:
        print(e)

def main():
    if not mt5.initialize():
        print("Initialization failed")
    try:
        while True:

            if is_new_trade() :
                trade_data = positions_get()


    except KeyboardInterrupt:
        print("\nExiting program")


    mt5.shutdown()


if __name__ == '__main__':
    main()