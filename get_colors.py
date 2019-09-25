from time import sleep
from netaddr import EUI
from broadlink import rm
from binascii import hexlify

RM3Device = rm(("192.168.178.130", 80), EUI("B4:43:0D:FC:05:CE"), 0x27c2)
RM3Device.auth()

RM3Device.enter_learning()

colors = {}

while True:
    learned_cmd = RM3Device.check_data()
    if learned_cmd is not None:
        cmd = str(hexlify(learned_cmd), 'ascii')
        name = input("How'd you name this command?\n")
        if name == "done":
            print()
            print()
            print(colors)
            print()
            print()
            exit()
        colors[name] = cmd
        RM3Device.enter_learning()
    sleep(0.1)
