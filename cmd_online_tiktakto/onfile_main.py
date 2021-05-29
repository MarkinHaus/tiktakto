import os
import socket
import threading
from time import sleep


class Bot:

    def __init__(self):
        self.end_st_w_i = 0
        self.win = 0
        self.lose = 0
        self.ai_data = [["KR-", [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                        ["W--", [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                        ["L--", [0, 0, 0, 0, 0, 0, 0, 0, 0]],
                        ["W-L", [0, 0, 0, 0, 0, 0, 0, 0, 0]]]
        self.ln_num = 0

    @staticmethod
    def convert2tree(m, w=None):
        if w is None:
            w = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        mt = []
        nums = []
        i = 0
        # ('O', 'O', 'r', 'O', 'X', 'X', 'y', 'c', 'X')
        for place in m:
            if place == sp1_pl:
                mt.append(1)
                w[i] = "None"
            if place == sp2_pl:
                mt.append(2)
                w[i] = "None"
            if place != sp1_pl and place != sp2_pl:
                mt.append(0)
                nums.append(i)

            i += 1
        return mt, w, nums

    @staticmethod
    def convert4tree(mt):
        m = []
        ma = ('w', 'e', 'r', 's', 'd', 'f', 'y', 'c', 'v')
        i = 0
        for place in mt:
            if place == 0:
                m.append(ma[i])
            if place == 1:
                m.append(sp1_pl)
            if place == 2:
                m.append(sp2_pl)
            i += 1
        return m

    def predict(self, m, w, nums, s: int):
        #       (nrmale map: status, )
        mt, _, _ = self.convert2tree(m)
        self.end_st_w_i += 1
        # w e r 0 0 0 -> 0 0 0
        # s d f 0 0 0 -> 0 1 0
        # y c v 0 0 0 -> 0 0 0

        # mt= 2 2 0
        #    2 1 1
        #    0 0 1

        # w= -2 -2 0 -> -2 -2  3
        #   -2 -2 -2 -> -2 -2 -2
        #    0  0 -2 ->  2 -1 -2

        # nums= 0 6 7
        # w = [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0]
        for j in range(0, len(nums)):
            mt[nums[j]] = s
            winn = winning(mt)
            if winn[1] == 2:
                w[nums[j]] += 2
                # print("-WIN-", j, nums[j])
                # mep(self.convert4tree(mt))
                # print("nums:", nums, len(nums))
                self.win += 1
                return w
            if winn[1] == 1:
                w[nums[j]] -= 2
                self.lose += 1
                # print("-LOSE-", j, nums[j])
                # mep(self.convert4tree(mt))
                # print("nums:", nums, len(nums))
                return w
            if not winn[0]:
                # print("nums:", nums, len(nums), "| NEXT")
                num_copy = nums.copy()
                num_copy.remove(nums[j])
                if s == 2:
                    w = self.predict(self.convert4tree(mt), w, num_copy, 1)
                else:
                    w = self.predict(self.convert4tree(mt), w, num_copy, 2)
                del num_copy
            mt[nums[j]] = 0
            if len(nums) == self.ln_num:
                # mep(w)
                # mep(self.convert4tree(mt))
                # print(j, ":| j")
                # print("winn:", self.win)
                # print("lose:", self.lose)
                # print("end:", self.win - self.lose)
                #  [3536, 2984, 4920, 2992, 7776, 3760, 7408, 5368, 10736]
                #   2860  2074  2852  2114  3440  2664  2894  2842  3000
                # w 5692  5978  5842  6196  5592  7076  5986  7400  6110
                # l 2832  3904  2990  4082  2152  4412  3092  4558  3110
                self.ai_data[1][1][nums[j]] = self.win
                self.ai_data[2][1][nums[j]] = self.lose
                self.ai_data[3][1][nums[j]] = self.win - self.lose
                self.win = 0
                self.lose = 0
        return w

    def run_predict(self, bot_m):
        _, bot_w, bot_nums = self.convert2tree(bot_m)
        mask = []
        i = 0
        # print(bot_w, "bot_w")
        for item in bot_w:
            if item == "None":
                mask.append(i)
            i += 1
        self.ln_num = len(bot_nums)
        self.ai_data[0][1] = b.predict(bot_m, bot_w, bot_nums, 2)
        end = []
        bef = []
        # print(mask, "mask")
        for _, move_list in self.ai_data:
            i = 0
            move_list_copy = move_list.copy()
            # print(move_list_copy, "1")
            for __ in move_list:
                if i in mask:
                    move_list_copy.remove(move_list[i])
                i += 1
            # print(move_list_copy, "2")
            # print()
            max_ = -1
            min_ = -1
            try:
                max_ = move_list.index(max(move_list_copy))
                while max_ in mask:
                    max_ = move_list.index(max(move_list_copy))
                    move_list[max_] = max(move_list_copy) - 1
            except IndexError and ValueError:
                pass
            if max_ not in mask:
                bef.append(max_)
            else:
                if len(bot_nums) != 0:
                    bef.append(bot_nums[0])
                else:
                    bef.append(-1)
            try:
                min_ = move_list.index(min(move_list_copy))
                while min_ in mask:
                    min_ = move_list.index(min(move_list_copy))
                    move_list[min_] = min(move_list_copy) - 1
            except IndexError and ValueError:
                pass
            if min_ not in mask:
                bef.append(min_)
            else:
                if len(bot_nums) != 0:
                    bef.append(bot_nums[-1])
                else:
                    bef.append(-1)
            end.append([_, move_list])
            del move_list_copy
        return end, bef


class P2p:
    address = "127.0.0.1"  # socket.gethostname()
    port = 62435

    def __init__(self, name, address, port):
        self.address = address
        self.port = int(port)
        self.is_connected = False
        global sp1, sp2, sp1_pl, sp2_pl
        self.is_host = False
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        try:
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con = con

            con_test_thread = threading.Thread(target=self.connect)
            con_test_thread.daemon = True
            con_test_thread.start()

            for i in range(0, 20):
                sleep(0.05)

            del con_test_thread

            if not self.is_connected:
                raise ConnectionResetError

            self.user1_dict = {"name": name,
                               "data": {"game": "", "hostname": [socket.gethostname()], "state": 2,
                                        "sp_pl": sp2_pl, "user": 2, "recv": True}}
            self.send()
            self.wait = True
            sleep(0.1)
        except ConnectionResetError and Exception:
            print(f"No Host found: ")
            self.user1_dict = {"name": name,
                               "data": {"game": "", "hostname": [socket.gethostname()], "state": 1,
                                        "sp_pl": sp1_pl, "user": 1, "recv": True}}
            print(socket.gethostname()," : ", socket.gethostbyname(socket.gethostname()), self.port)
            # con.bind((self.address, P2p.port))
            con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.con = con
            con.bind(("", self.port))
            con.listen(1)
            self.is_host = True
            con_thread = threading.Thread(target=self.request)
            con_thread.daemon = True
            con_thread.start()

            self.wait = True
        self.name = name
        self.user2_dict_con = None
        self.user2_dict_address = None
        self.user2_dict = {"name": "", "data": {"game": "",
                                                "hostname": [socket.gethostname()],
                                                "state": -1,
                                                "sp_pl": sp2_pl,
                                                "user": None,
                                                "recv": False}}
        if not self.is_host:
            sp2 = name

            con_thread = threading.Thread(target=self.recv)
            con_thread.daemon = True
            con_thread.start()

        else:
            sp1 = name
            self.user1_dict["data"]["user"] = 1

    def connect(self):
        try:
            self.con.connect((self.address, self.port))
            self.is_connected = True
        except Exception:
            self.is_connected = False

    def recv(self):
        if self.is_host:
            self.wait = False
            while True:
                self.user2_dict = bd(self.user2_dict_con.recv(1024))
        else:
            self.user2_dict = bd(self.con.recv(1024))

            self.user2_dict_address = "py - server " + self.address
            self.wait = False
            while True:
                self.user2_dict = bd(self.con.recv(1024))

    def request(self):
        global sp2
        c, a = self.con.accept()
        self.user2_dict = bd(c.recv(1024))
        self.user2_dict_con = c
        self.user2_dict_address = a
        sp2 = self.user2_dict["name"]
        self.send()
        self.recv()

    def send(self):
        if self.is_host:
            self.user2_dict_con.send(db(self.user1_dict))
        else:
            self.con.send(db(self.user1_dict))

    def reset(self):
        self.user2_dict["data"]["recv"] = False


class Client:
    address = "127.0.0.1"  # socket.gethostname()
    port = 62435

    def __init__(self, name):
        self.is_connected = False
        global sp1, sp2, sp1_pl, sp2_pl
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as con:
        con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con = con
        con_test_thread = threading.Thread(target=self.connect)
        con_test_thread.daemon = True
        con_test_thread.start()
        for i in range(0, 20):
            sleep(0.05)
        del con_test_thread
        if not self.is_connected:
            print("server offline")
        self.user1_dict = {"name": name,
                           "data": {"game": "", "hostname": [socket.gethostname()], "state": "None",
                                    "sp_pl": sp2_pl, "user": None, "recv": True,
                                    "lobby address": ["", "", ""], "lobby list": "None", "set lobby": "None"}}
        self.send()
        self.wait = True
        sleep(0.1)
        self.name = name
        sp2 = name
        con_thread = threading.Thread(target=self.recv)
        con_thread.daemon = True
        con_thread.start()

    def connect(self):
        try:
            self.con.connect((self.address, self.port))
            self.is_connected = True
        except Exception:
            self.is_connected = False

    def recv(self):
        self.user1_dict = bd(self.con.recv(1024))
        self.wait = False
        while True:
            self.user1_dict = bd(self.con.recv(1024))

    def send(self):
        self.con.send(db(self.user1_dict))

    def reset(self):
        self.user1_dict["data"]["recv"] = False

    def res(self):
        while not self.user1_dict["data"]["recv"]:
            pass
        self.reset()


def Average(lst):
    return sum(lst) / len(lst)


def winning(m):
    posses = [[0, 1, 2],
              [3, 4, 5],
              [6, 7, 8],
              [0, 3, 6],
              [1, 4, 7],
              [2, 5, 8],
              [0, 4, 8],
              [6, 4, 2],
              ]

    for poss in posses:
        if m[poss[0]] == m[poss[1]] == m[poss[2]] and m[poss[0]] != 0:
            return True, m[poss[0]]
    return False, None


def main():
    global sp1, sp2, b
    sp1 = name_
    run = True
    while run:
        print("play online: 0")
        print("play local: 1")
        print("play vs bot: 2")
        print("exit: 3 or exit")
        num = imp("")
        if num == "0":
            print("connect to online server: 0")
            print("play in local network: 1")
            num1 = imp("")
            if num1 == "1":
                ip = imp("enter ip")
                port = imp("enter port")
                if not port:
                    port = P2p.port
                p = P2p(name_, ip, port)
                print("wait...")
                while p.wait:
                    pass
                print(f'name : {p.user2_dict["name"]}; address : {p.user2_dict_address} ; hostname = '
                      f'{p.user2_dict["data"]["hostname"]}')
                p.reset()
                online_local(p)
            if num1 == "0":
                client = Client(name_)
                online(client)
            else:
                main()

        if num == "1":
            sp2 = imp("sp2: enter Name:")
            normal_game()
        if num == "2":
            bot_pl = {
                "1": 1,
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
            }
            print("bot level 1 to 8")
            print("lv1 = max random")
            print("lv2 = min random")
            print("lv3 = max Wins")
            print("lv4 = min Wins")
            print("lv5 = max Lose")
            print("lv6 = min Lose")
            print("lv7 = max Wins - Lose")
            print("lv8 = min Wins - Lose")

            pl = imp("choose a bot level")

            if pl in ("1", "2", "3", "4", "5", "6", "7", "8"):
                pl = bot_pl[pl]
            else:
                print("error just 1 to 8")
                main()
            game_bot(b, pl)
        if num == "3" or num == "exit":
            exit(0)
        else:
            main()


def online(client: Client):
    joined = False
    client.res()
    while not joined:
        print(client.user1_dict["data"]["lobby list"])
        lobby_t = imp("")
        if lobby_t == "..":
            main()
        client.user1_dict["data"]["set lobby"] = lobby_t
        client.send()
        client.res()
        if client.user1_dict["data"]["lobby address"][0] == lobby_t:
            joined = True
        else:
            print("invalid lobby address pls try again or type ..")

    if joined:
        print("waiting in lobby: ")
        print(client.user1_dict["data"]["lobby address"][2])
        while client.user1_dict["data"]["lobby address"][1] < 2:
            pass
        online_game(client)
    else:
        main()


def online_game(client: Client):
    global sp1, sp2, sp1_pl, sp2_pl
    state = 0
    if client.user1_dict["data"]["user"] == 1:
        state = pick()
        client.user1_dict["data"]["state"] = 0 if state else 1
        client.send()
    if client.user1_dict["data"]["user"] == 2:
        print("Awaiting user 1")
        client.res()
        state = client.user1_dict["data"]["state"]

    game = ['w', 'e', 'r',
            's', 'd', 'f',
            'y', 'c', 'v']

    print(state)

    for zug_left in range(0, 8):
        if state == 0:
            state = 1
            test_fin = comb(game, client.user1_dict["name"], client.user1_dict["data"]["sp_pl"])
            client.user1_dict["data"]["game"] = game
            client.send()
            if test_fin(game):
                client.user1_dict["data"]["game"] = "fin"
                client.send()
                online_game(client)
            # con.user2_dict["data"]["game"] = game

        else:
            state = 0
            mep(game)
            print(f"Awaiting your turn..")
            client.res()
            game = client.user1_dict["data"]["game"]
            if check(game):
                client.user1_dict["data"]["game"] = "fin"
                client.send()
                online_game(client)

    print("undecided again?")
    if imp("play again? [yes | no] : ") == "yes":
        client.user1_dict["data"]["game"] = "fin"
        client.send()
        online_game(client)
    main()


def comb(game, s, s_pl):
    mep(game)
    user_inp(game, -1, b, f"{s} - {s_pl}:", s_pl)
    return check


def check(game):
    if winning(game)[0]:
        print("player ,", winning(game)[1], ", won")
        if imp("play again? [yes | no] : ") == "yes":
            return True
        else:
            main()
    if len(b.convert2tree(game)[2]) == 0:
        print("undecided again?")
        if imp("play again? [yes | no] : ") == "yes":
            return True
        else:
            main()
    return False


def pick():
    s = imp(f"who wants to start? [{sp1}=0 | {sp2}=1] : ")
    if s == "0":
        return 0
    if s == "1":
        return 1
    pick()
# "name": "", "con": "", "address": "", "data": {"game": "",
#                                                                          "hostname": [socket.gethostname()],
#                                                                          "state": -1,
#                                                                          "sp_pl": sp2_pl,
#                                                                          "user": None}}


def online_local(con: P2p):
    global sp1, sp2, sp1_pl, sp2_pl
    state = 0
    if con.user1_dict["data"]["user"] == 1:
        state = pick()
        con.user1_dict["data"]["state"] = 0 if state else 1
        con.send()
    if con.user1_dict["data"]["user"] == 2:
        print("Awaiting user 1")
        while not con.user2_dict["data"]["recv"]:
            pass
        con.reset()
        state = con.user2_dict["data"]["state"]

    game = ['w', 'e', 'r',
            's', 'd', 'f',
            'y', 'c', 'v']

    print(state)

    for zug_left in range(0, 8):
        if state == 0:
            state = 1
            test_fin = comb(game, con.user1_dict["name"], con.user1_dict["data"]["sp_pl"])
            con.user1_dict["data"]["game"] = game
            con.send()
            if test_fin(game):
                online_local(con)
            # con.user2_dict["data"]["game"] = game

        else:
            state = 0
            mep(game)
            print(f"Awaiting your turn..")
            while not con.user2_dict["data"]["recv"]:
                pass
            con.reset()
            game = con.user2_dict["data"]["game"]
            if check(game):
                online_local(con)

    print("undecided again?")
    if imp("play again? [yes | no] : ") == "yes":
        online_local(con)
    main()


def normal_game():
    global sp1, sp2, sp1_pl, sp2_pl
    game = ['w', 'e', 'r',
            's', 'd', 'f',
            'y', 'c', 'v']

    state = pick()

    for zug_left in range(0, 8):
        if state == 0:
            state = 1
            if comb(game, sp1, sp1_pl)(game):
                normal_game()
        else:
            state = 0
            if comb(game, sp2, sp2_pl)(game):
                normal_game()
    print("undecided again?")
    if imp("play again? [yes | no] : ") == "yes":
        normal_game()
    main()


def game_bot(b: Bot, pl):
    global sp1, sp2, sp1_pl, sp2_pl
    game = ['w', 'e', 'r',
            's', 'd', 'f',
            'y', 'c', 'v']
    sp2 = "bot"

    state = pick()

    for zug_left in range(0, 8):
        if state == 0:
            state = 1
            if comb(game, sp1, sp1_pl)(game):
                game_bot(b, pl)
        else:
            state = 0
            mep(game)
            _, bef = b.run_predict(game)
            print(bef)
            if bef[pl] != -1:
                print(bef[pl], "BOT")
                game[bef[pl]] = sp2_pl
                zug_left += 1
            else:
                print("no move found")
                undecided(b, pl)
                break

            if len(b.convert2tree(game)[2]) == 0:
                undecided(b, pl)
                break

            if winning(game)[0]:
                print("player ,", winning(game)[1], ", won")
                if imp("play again? [yes | no] : ") == "yes":
                    game_bot(b, pl)
                main()

    undecided(b, pl)


def user_inp(game, pl, b, user, sp_pl):
    not_acc = True
    while not_acc:
        game_c = game.copy()
        user_imp = imp(f"user input as {user}: ")
        if user_imp in ('w', 'e', 'r', 's', 'd', 'f', 'y', 'c', 'v', "exit", "again", ".."):
            if user_imp == "exit":
                print("bye")
                exit(0)
            if user_imp == "again":
                if pl != -1:
                    game_bot(b, pl)
                if pl == -1:
                    normal_game()
                if pl == -2:
                    # TODO online game
                    pass
            if user_imp == "..":
                main()
            if user_imp in game_c:
                _, weight, _ = b.convert2tree(game)
                place = game_c.index(user_imp)
                if weight[place] != "None":
                    game[place] = sp_pl
                    not_acc = False
                    del game_c
            else:
                print("only the following fields are free:")
                if sp1_pl in game_c:
                    game_c.remove(sp1_pl)
                if sp2_pl in game_c:
                    game_c.remove(sp2_pl)
                print(game_c, "\n")
        else:
            print("only the following entries are allowed:")
            print(('w', 'e', 'r', 's', 'd', 'f', 'y', 'c', 'v', "exit", "again", ".."), "\n")
    return game


def undecided(b, pl):
    print("undecided again?")
    if imp("play again? [yes | no] : ") == "yes":
        game_bot(b, pl)
    main()


def mep(m):
    print(f'\n#{sp1}#vs#{sp2}#\n#######\n {m[0]} {m[1]} {m[2]} \n {m[3]} {m[4]} {m[5]} \n {m[6]} {m[7]} {m[8]}'
          f'\n#######')
    return m


def db(dic: dict) -> bytes:
    return bytes(str(dic), "utf-8")


def bd(byt: bytes) -> dict:
    return eval(str(byt, "utf-8"))


def imp(s) -> str:
    return input(f"{s}\n-> ")


if __name__ == '__main__':
    # con = P2p(imp("pls enter ur name"))
    sp1 = "sp1"  # con.name
    sp2 = "sp2"  # con.user2_dict["name"]
    sp1_pl, sp2_pl = "O", "X"
    # w e r
    # s d f
    # y c v
    # m = ('w', 'e', 'r',
    #      's', 'O', 'f',
    #      'y', 'c', 'v')
    name_ = imp("Name:")
    b = Bot()
    main()

    # normal_game()
    # game_bot(b, 7)
    # mt, w, nums = b.convert2tree(m)
    # print("m:", mep(m))
    # print("mt: ", mep(mt))
    # print("w: ", mep(w))
    # print("nums:", nums)
    # print("-------------------------")
    # x, bef = b.run_predict(m)
#
# if x:
#     for t, x_ in x:
#         print(x_, "END| ", t)
#         print("BEST:", x_.index(max(x_)))
#         print("WORST:", x_.index(min(x_)))
# print("steps:", b.end_st_w_i)
# print(bef)
