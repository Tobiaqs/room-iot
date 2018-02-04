from time import sleep
from netaddr import EUI
from broadlink import rm
from binascii import hexlify

RM3Device = rm(("88.159.235.52", 60000), EUI("60-E3-27-4B-69-23"))
RM3Device.auth()

RM3Device.enter_learning()

colors = {}

while True:
    learned_cmd = RM3Device.check_data()
    if learned_cmd is not None:
        cmd = str(hexlify(learned_cmd), 'ascii')
        name = input("How'd you name this color?\n")
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