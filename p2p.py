#!/usr/bin/env python3

import socket
import  _thread
from threading import Thread
from time import sleep
from sys import exit, argv

class Conn:
    def __init__(self, dip, sport=5001, dport=5002):
        self.sport, self.dip, self.dport = sport, dip, dport
        self.connected = False
        self.senderInit()
        self.recieverInit()
        self.send("FLAG_SYN")
        self.punchHole = Thread(target=self.keepAlive, daemon=True)
        self.punchHole.start()
        self.listener = Thread(target=self.recieve, daemon=True)
        self.listener.start()

    def senderInit(self):
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sender.bind(("0.0.0.0", self.dport))
    def recieverInit(self):
        self.reciever = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.reciever.bind(("0.0.0.0", self.sport))
    def keepAlive(self, interval = 30):
        ka_packet = "0"
        while True:
            self.reciever.sendto(ka_packet.encode(), (self.dip, self.dport))
            sleep(30)
    def recieve(self):
        while True:
            msg = self.reciever.recv(1024)
            if len(msg) > 0:
                if msg == b"FLAG_SYN":
                    if self.connected == False:
                        self.connected = True
                        self.display("\n\t<========== Connection Established ==========>")
                        self.send("FLAG_SYN")
                elif msg == b"FLAG_FIN":
                    self.display("\n\t<========== Connection Terminated =========>")
                    _thread.interrupt_main()
                    _thread.exit()
                else:
                    self.display(msg.decode())
    def send(self, msg):
        self.sender.sendto(msg.encode(), (self.dip, self.sport)) 

    def display(self, msg):
        print("\033[92m"+msg+"\033[0m")

    def close(self):
        self.send("FLAG_FIN")
        self.connected = False
        self.display("\n\t<==========   Chat Terminated   ==========>")

if __name__ == "__main__":
    if len(argv) >1:
        dip = argv[1]
    else:
        dip = input("\tEnter the ip of your friend: ")

    conn = Conn(dip)
    print(f"\n\t  connecting to {dip} ...\033[5m.\033[0m\n")
    try:
        while True:
            msg = input()
            conn.send(msg)
    except KeyboardInterrupt:
        conn.close()
        exit()
    else:
        print("!!--Something went wrong--!!")

