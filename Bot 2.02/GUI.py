import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.bubble import Bubble
from kivy.uix.bubble import BubbleButton
from kivy.uix.popup import Popup
from kivy.clock import Clock
from threading import Thread
from queue import Queue
import glavna
import time


class MainLayout(BoxLayout):
    queue = Queue()
    scroller = ObjectProperty()
    order_checker_running = False

    def add_order(self, uuid, market):
        my_order = MyOrder()
        my_order.start(uuid, market)
        self.scroller.add_widget(my_order)

    def open_popup(self):
        settings_popup = SettingsPopup()
        settings_popup.open()

    def toggle_check_orders_thread(self):
        if self.order_checker_running is False:
            check_orders_thread = Thread(target = self.check_orders, args=(self.queue,))
            check_orders_thread.daemon = True
            check_orders_thread.start()
            self.order_checker_running = True

            check_queue_thread = Thread(target=self.check_queue, args=(self.queue,))
            check_queue_thread.daemon = True
            check_queue_thread.start()
            print('New thread for checking orders created')

    def check_orders(self, queue):
        #Clock.schedule_interval(glavna.glavna, 5)
        print('In check_orders')
        glavna.main_loop(queue)

    def check_queue(self, queue):
        print('In check_queue')
        if not queue.empty():
            new_orders = queue.get()
            for order in new_orders:
                self.add_order(order[0], order[1])          # order[0] is uuid, order[1] is market
                time.sleep(0.1)
        time.sleep(5)
        self.check_queue(queue)

class MyOrder(BoxLayout):

    def start(self, uuid, market):
        bubble = Bubble(arrow_pos="right_mid")
        bubble.add_widget(BubbleButton(text = market))
        self.add_widget(bubble, 4)

class SettingsPopup(Popup):
    pass

class MainLayoutApp(App):

    def build(self):
        layout = MainLayout()
        #layout.start_check_orders_thread()
        #thread = Thread(target = glavna.glavna, args = (time.time(),))
        #thread.start()
        #thread.join()
        #abc = Clock.schedule_interval(glavna.glavna, 7)
        # scroll = MyScrollView()

        #  layout.add_widget(scroll)
        return layout

gui = MainLayoutApp()
gui.run()