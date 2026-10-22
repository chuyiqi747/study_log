import  random
def scsjs() :
    x=random.randint(1,100)
    return x
def cz(x):

    i = int(input("输入你的答案（1-100）："))

    while i!=x:

        if i>x:
            print("猜大了")
        elif i<x:
            print("猜小了")
        i = int(input("继续（1-100）："))
    print("答对了")
    return 0


if __name__ == '__main__':

    x=scsjs()
    cz(x)
