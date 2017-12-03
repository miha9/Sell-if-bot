from bittrex import Bittrex
from order import Order


class BittrexOrders(Bittrex):

    # gets open buy orders, creates new order objects and returns the new uuids of orders and new_order_objects
    def get_open_buy_orders(self, uuid_orders):
        new_order_objects = []  # stores orders as objects with parameters uuid, market, buy_price, qty and qty_rem
        new_uuid_orders = []

        orders = self.get_open_orders()
        if orders['success']:
            if len(orders['result']) > 0:
                for i in range(len(orders['result'])):
                    if orders['result'][i]['OrderType'] == 'LIMIT_BUY':
                        if orders['result'][i]['OrderUuid'] not in uuid_orders:
                            uuid = orders['result'][i]['OrderUuid']
                            market = orders['result'][i]['Exchange']
                            buy_price = orders['result'][i]['PricePerUnit']
                            qty = orders['result'][i]['Quantity']
                            qty_rem = orders['result'][i]['QuantityRemaining']
                            new_order_objects.append(Order(uuid, market, buy_price, qty, qty_rem, is_open=True))
                            new_uuid_orders.append(orders['result'][i]['OrderUuid'])
                            print(market)

                else:
                    if not new_uuid_orders:
                        #print("bittrex_open_orders: No new orders")
                        return None
                    else:
                        #print(new_uuid_orders)
                        return [new_uuid_orders, new_order_objects]
            else:
                #print("bittrex_open_orders: No open orders")
                return None
        else:
            print("bittrex_open_orders: Request failed")
            return None


