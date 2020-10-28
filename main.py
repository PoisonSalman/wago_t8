from typing import Type

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from pyModbusTCP.client import ModbusClient
import time
from kivymd.toast import toast
import threading

kv = Builder.load_file("screen.kv")

toggle = True

def build():
    return kv

class MainWindow(Screen):
    container = ObjectProperty(None)
    label_text = StringProperty()
    data_list = ListProperty([])
    name_x = StringProperty(' ')
    first_read_label_text = StringProperty(' ')
    second_read_label_text = StringProperty(' ')
    image_source = StringProperty(' ')


    def update_info(self):
        self.name_x = self.ids.first_input_id2.text
        a_name = self.name_x
        save_data(self, a_name)
        return(a_name)

    def butondan_gelen(self, gelen):
        name_x=MainWindow.update_info(self)

        if gelen == True:
            state.state_on(self,name_x)
        if gelen == False:
            state.state_off(self,name_x)


class state:

        def state_on(self, name_x):
            SERVER_HOST = name_x
            SERVER_PORT = 502
            c = ModbusClient()
            c.host(SERVER_HOST)
            c.port(SERVER_PORT)
            c.open()

            is_ok = c.write_single_coil(32768, True)
            bits = c.read_holding_registers(32768)

            if bits:
                self.first_read_label_text = str('Acik')
                self.image_source = "sf_yesil.png"
            else:
                self.first_read_label_text = str('cannotread')

        def state_off(self, name_x):
            SERVER_HOST = name_x
            SERVER_PORT = 502
            c = ModbusClient()
            c.host(SERVER_HOST)
            c.port(SERVER_PORT)
            c.open()
            is_ok = c.write_single_coil(32768, False)
            if is_ok:
                self.first_read_label_text = str('kapali')
                self.image_source = "sf0.png"
            else:
                self.first_read_label_text = str('failed')


def save_data(self, name_x):
    SERVER_HOST = name_x
    SERVER_PORT = 502
    c = ModbusClient()
    c.host(SERVER_HOST)
    c.port(SERVER_PORT)

    if not c.is_open():
        if not c.open():
            toast("failed")
    if c.is_open():
        toast("connected")


class TestApp(App):

    def build(self):
        return MainWindow()


if __name__ == "__main__":
    TestApp().run()


'''class TestApp(App):
    def build_main(self):
        return MainWindow()
    def background(self):
        while True:
            SERVER_HOST = '192.168.1.4'
            SERVER_PORT = 502
            c = ModbusClient()
            c.host(SERVER_HOST)
            c.port(SERVER_PORT)
            bits = c.read_holding_registers(32768)
            if bits == True:
                self.image_source = "sf0.png"
            else:
                self.image_source = "sf_yesil.png"
            time.sleep(0.5)

if __name__ == "__main__":

    self = MainWindow()
    b = threading.Thread(name='background', target=TestApp.background, args=(self,))
    f = threading.Thread(name='build_main', target=TestApp.build_main, args=(self,))
    f.start()
    b.start()'''





