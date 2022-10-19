import market

def main():

    user=market.User()
    print("Welcome To Market".center(40,"-"))
    user.main()

    if user.user == None:
        print("Exit...")
        exit()
    else:
        product=market.Product()
        while True:
            print("transactions".center(30,"-"))
            s = input("   1 : selling transactions\n   2 : buying transactions\n   3 : balance add\n   q : exit\nSelection : ")
            if s=="q":
                print("Exit...")
                exit()
            elif s=="1":
                product.sellingTransactions(user.user["_id"])
            elif s=="2":
                product.buyingTransactions(user.user["_id"])
            elif s=="3":
                user.balanceAdd()
            else:
                print("There is no such option, try again")

main()


