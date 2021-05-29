import socket
import threading
import time
import string

HOST = ""
PORT = 62435

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))
sock.listen(3)
print('online')

lobby_list = []
connections = []


class Connections:

    def __init__(self, dic, c, a):
        self.name = dic["name"]
        self.game = dic["data"]["game"]
        self.hostname = dic["data"]["hostname"]
        self.state = dic["data"]["state"]
        self.sp_pl = dic["data"]["sp_pl"]
        self.user = len(connections)
        self.recv_b = dic["data"]["recv"]
        self.lobby_address = dic["data"]["lobby address"]
        #
        # lobby, state, player_num, names in lobby_list[n]
        # s += f"address: {lobby} | state: {state} | player num: {player_num}, names: {names}\n"
        #
        # ["addres", num_pl, s]
        #
        self.get_lobby = dic["data"]["set lobby"]
        self.con = c
        self.address = a
        con_thread = threading.Thread(target=self.recv)
        con_thread.daemon = True
        con_thread.start()

    def dic2map(self, dic):
        self.name = dic["name"]
        self.game = dic["data"][""]
        self.hostname = dic["data"]["hostname"]
        self.state = dic["data"]["state"]
        self.sp_pl = dic["data"]["sp_pl"]
        self.user = dic["data"]["user"]
        self.recv_b = dic["data"]["recv"]
        self.lobby_address = dic["data"]["lobby address"]
        self.get_lobby = dic["data"]["set lobby"]
        self.reset()

    def map2dic(self):
        return {"name": self.name,
                "data": {"game": self.game, "hostname": self.hostname, "state": self.state,
                         "sp_pl": self.sp_pl, "user": self.user, "recv": self.recv_b,
                         "lobby address": self.lobby_address, "lobby list": convert_lobby_list(), "set lobby": self.get_lobby
                         }}

    def send(self):
        try:
            self.con.send(db(self.map2dic()))
        except Exception:
            del self

    def recv(self):
        try:
            while True:
                self.dic2map(bd(self.con.recv(1024)))
        except Exception:
            del self

    def reset(self):
        self.recv_b = False

    def res(self):
        while not self.recv_b:
            pass
        self.reset()


def db(dic: dict) -> bytes:
    return bytes(str(dic), "utf-8")


def bd(byt: bytes) -> dict:
    return eval(str(byt, "utf-8"))


def convert_lobby_list(i=0):
    if i:
        lobby, state, player_num, names = lobby_list[i]
        return f"address: {lobby} | state: {state} | player num: {player_num}, names: {names}\n"
    s = ""
    for lobby, state, player_num, names, _ in lobby_list:
        s += f"address: {lobby} | state: {state} | player num: {player_num}, names: {names}\n"
    return s


def jon_lobby():
    con = connections[-1]
    con.res()
    i = 0
    for lobby in lobby_list:
        if con.get_lobby == lobby[0] and lobby[1] == "up":
            lobby_list[i][3].append(con.name)
            lobby_list[i][4].append(con)
            con.lobby_address = [lobby[0], lobby[2], convert_lobby_list(i)]
            lobby_list[lobby_list.index(lobby)][2] += 1
            con.send()
        if lobby[2] == 1:
            lobby_list[lobby_list.index(lobby)][1] = "in use"
            lobby_list[lobby_list.index(lobby)][2] += 1
            lobby_list[lobby_list.index(lobby)][4][1] = con
            lobby_list[lobby_list.index(lobby)][4][0]["sp_pl"] = "X"
            lobby_list[lobby_list.index(lobby)][4][1]["sp_pl"] = "O"
            in_game(lobby_list[lobby_list.index(lobby)][4][0], con)
        i += 1


def add_lobby(addess):
    lobby_list.append([addess, "up", 0, ["", ""], []])


def match_making():
    for lobby in lobby_list:
        if lobby[2] == 2:
            lobby_list[lobby_list.index(lobby)][1] = "in use"
            con_thread = threading.Thread(target=in_game, args=(lobby_list[lobby_list.index(lobby)][4][0],
                                                                lobby_list[lobby_list.index(lobby)][4][1]))
            con_thread.daemon = True
            con_thread.start()


def in_game(con1: Connections, con2: Connections):
    con1.user = 1
    con2.user = 2
    con1.send()
    con2.send()
    con1.res()
    con2.state = con1.state
    con1.state = 0 if con1.state else 1
    con2.send()
    for i in range(0, 8):
        if con1.state == 0:
            con1.state = 0 if con1.state else 1
            con2.state = 0 if con2.state else 1

            con1.res()

            if con1.game == "fin":
                in_game(con1, con2)
            con2.game = con1.game
            con2.send()

        if con1.state == 1:
            con2.state = 0 if con2.state else 1
            con1.state = 0 if con1.state else 1

            con2.res()

            if con2.game == "fin":
                in_game(con1, con2)
            con1.game = con2.game
            con1.send()


def connections_handler():
    while True:

        c, a = sock.accept()
        dic = bd(c.recv(1024))
        add_lobby(a[0]+":"+dic["name"])
        connections.append(Connections(dic, c, a))
        print(connections[-1].map2dic())
        connections[-1].send()
        con_thread = threading.Thread(target=jon_lobby)
        con_thread.daemon = True
        con_thread.start()


connections_handler()
