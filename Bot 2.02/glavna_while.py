from bittrex_open_orders import BittrexOrders
import time
#import GUI

#THIS FILE IS NOT USED ANYMORE, BUT STILL PRESENT, IN CASE ANYONE WANTS TO RUN THE WHILE LOOP

bittrex_api_key = ""
bittrex_api_secret = ""
old_time = time.time()
timeout = 5
bittrex_orders = BittrexOrders(bittrex_api_key, bittrex_api_secret)


uuid_orders = []  # stores uuids of orders that have already been transformed to objects
order_objects = []  # stores orders as objects with parameters uuid, market, buy_price, qty and qty_rem

def glavna(old_time):
    while True:
        new_time = time.time()
        if new_time - old_time > timeout:
            orders = bittrex_orders.get_open_buy_orders(
                uuid_orders)  # orders[0] are the new uuid_orders, [1] are the new order_objects

            if orders is not None:
                uuid_orders.extend(orders[0])
                order_objects.extend(orders[1])

                for order in orders[1]:
                    uuid = order._uuid
                    market = order._market
                   # GUI.MainLayout.add_order(uuid, market)

            for order_object in order_objects:
                order_object.check_if_bought(bittrex_orders)

            if True:
                print('--------------------------------------------------------------------------------')
                #gui.run()
            old_time = new_time
            #first = False