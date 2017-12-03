from bittrex import Bittrex


class Order:
    def __init__(self, uuid, market, buy_price, qty, qty_rem, is_open):
        self._uuid = uuid
        self._market = market
        self._buy_price = buy_price
        self._qty = qty
        self.qty_rem = qty_rem
        self.is_open = is_open
        self.sell_params = []
        self.old_qty_rem = qty
        self.selling = False # This flag goes to True when the coin is fully bought

    def check_if_bought(self, bittrex_api):

        order = bittrex_api.get_order(self._uuid)
        self.qty_rem = order['result']['QuantityRemaining']
        self._buy_price = order['result']['PricePerUnit']
        #print(self._buy_price, self.sell_params, self._market)

        # Coin not bought
        if self.qty_rem == self.old_qty_rem:
            #print("Coin not bought! remaining:{0}".format(self.qty_rem))
            pass

        # Coin fully bought, not necessarily filled 100% immediately
        elif self.qty_rem == 0 and self.selling is False:
            self.sell_coin(self.old_qty_rem, bittrex_api)
            self.selling = True
            print('Coin fully bought')
            print(self._buy_price, self.sell_params, self._market)


        # Coin not fully bought
        elif self.qty_rem > 0 and self.qty_rem != self.old_qty_rem:
            self.sell_coin(self.old_qty_rem - self.qty_rem, bittrex_api)
            self.old_qty_rem = self.qty_rem
            print('Coin not fully bought')
            print(self._buy_price, self.sell_params, self._market)

    # sell_params set a sell order with the price buy_price*x, currently hardcoded
    def set_sell_params(self):
        self.sell_params = [[1, 1.2]]
        print('Params set')

    def sell_coin(self, sell_quantity, bittrex_api):
        print('Selling coin')
        self.set_sell_params() # this needs to be removed when making GUI, it's a function that will be linked to the confirm button
        for item in self.sell_params:
            bittrex_api.sell_limit(self._market, sell_quantity * item[0], self._buy_price * item[1])
            print("market: " + str(self._market) + "\nselling quantity: " + str(
                sell_quantity * item[0]) + "\nat price: " + str(self._buy_price * item[1]))


