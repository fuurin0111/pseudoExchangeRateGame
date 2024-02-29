import random
import csv
from inputimeout import inputimeout, TimeoutOccurred
import numpy as np
import matplotlib.pyplot as plt


#変数の定義
data = [[-1,-1,-1]]
money = 0
pre_money = 0
buy_money = 0
rate = 0
flag = True
EMPTY = 0
RATE_SPEED = 5
selection = ""
choice = 0
rate_all = []
print("セーブするためのcsvファイルを入力してください")
url = input()

def read():
    # CSVファイルの読み込み
    with open(url, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data[EMPTY] = list(map(int, row))

def write():
    data[EMPTY][0] = money
    data[EMPTY][1] = rate
    data[EMPTY][2] = pre_money
    with open(url, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def call():
    try:
        something = inputimeout(prompt=">>", timeout=RATE_SPEED)
        return something
    except TimeoutOccurred:
        something = " "
        return something
    
def graph():
    x = np.array(range(0,len(rate_all)))
    y = np.array(rate_all)
    plt.title("Rate Chages")
    plt.xlabel("Chage Point")
    plt.ylabel("Rate")
    plt.plot(x, y, color="red", marker="o", label="Array elements")
    plt.legend()
    plt.show()

read()

if data[EMPTY] == [-1,-1,-1]:
    data[EMPTY][0] = 1000
    data[EMPTY][1] = random.randint(100,200)
    data[EMPTY][2] = 0

money = data[EMPTY][0]
rate = data[EMPTY][1]
pre_money = data[EMPTY][2]

write()

while flag:
    print(f"現在のレートは{rate}円=100プレ,手持ち金額{money}円,{pre_money}プレ")
    selection = call()
    if selection == "buy":
        print(f"何円分買いますか?({rate}円以上)")
        buy_money = int(input())
        if buy_money <= money and buy_money >= 0:
            money -= buy_money
            pre_money += round((100/rate)*buy_money)
            print(f"{buy_money}円分買いました。残り{money}円")
            write()
        else:
            print("買えませんでした")
    elif selection == "sell":
        print("何プレ分売りますか?(100プレ以上)")
        buy_money = int(input())
        if buy_money <= pre_money and buy_money >= 0:
            money += round((rate/100)*buy_money)
            pre_money -= buy_money
            print(f"{buy_money}プレ分売りました。残り{pre_money}プレ")
            write()
        else:
            print("買えませんでした")
    elif selection == "cmdg":
        graph()
    elif selection == "end":
        print("終わります")
        flag = False
    elif selection == " ":
        rate += random.randrange(-1*round(rate/2),round(rate/2))
        choice = random.randrange(0,99)
        if rate <= 5:
            print("レート急上昇")
            rate = random.randint(100,300)
            write()
        if choice <= 5:
            print("レート急上昇")
            rate += random.randint(round(rate/2),rate)
            write()
        elif choice >= 94:
            print("レート急降下")
            rate += random.randint(-1*rate+10,-1*round(rate/2)+10)
            write()
    rate_all.append(rate)

write()
graph()