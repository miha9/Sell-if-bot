from bittrex_open_orders import BittrexOrders
import time
#import GUI

bittrex_api_key = ""
bittrex_api_secret = ""
old_time = time.time()
timeout = 6
bittrex_orders = BittrexOrders(bittrex_api_key, bittrex_api_secret)

uuid_orders = []  # stores uuids of orders that have already been transformed to objects
order_objects = []  # stores orders as objects with parameters uuid, market, buy_price, qty and qty_rem


def main_loop(queue):
    #new_time = time.time()
    #if new_time - old_time > timeout:
    orders = bittrex_orders.get_open_buy_orders(uuid_orders)  # orders[0] are the new uuid_orders, [1] are the new order_objects
    #print(new_time - old_time)

    if orders is not None:
        uuid_orders.extend(orders[0])
        order_objects.extend(orders[1])
        queue_orders = []

        for order in orders[1]:
            new_order = [order._uuid, order._market]
            queue_orders.append(new_order)
        queue.put(queue_orders)


    for order_object in order_objects:
        order_object.check_if_bought(bittrex_orders)
    time.sleep(timeout)
    main_loop(5)
            #if True:
            # print('--------------------------------------------------------------------------------')
            #gui.run()
            #old_time = new_time
        #first = False