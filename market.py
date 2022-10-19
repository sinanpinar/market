import database
import pandas as pd

class User:

    def __init__(self):
        self.userdb = database.UserDB()
        self.user = None

    def main(self):
        s=input("   1 : Login\n   2 : Register\nSelection : ")
        if s=="1":
            self.userLogin()
        elif s=="2":
            self.userRegister()
        else:
            print("There is no such option, try again")
    def userLogin(self):
        print("Login".center(30,"-"))
        i=1
        while i<4:
            name=input("Name : ")
            password=input("Password : ")
            s=self.userdb.userLogin(name,password)
            if s==False:
                print("You couldn't log in due to an error, try again later")
                exit()
            elif s==None:
                if i==3:
                    print("your rights have been exhausted")
                else:
                    print("No matching records found, try again.")
                    print(f"Remaining right {4-i-1}".center(30,"-"))
            else:
                self.user=s
                break
            i+=1
        
    def userRegister(self):
        print("Register".center(30,"-"))
        u=dict()
        u["name"] = input("Name     : ")
        u["eposta"] = input("Eposta   : ")
        u["password"] = input("Password : ")
        u["balance"] = 0.0
        u["basket"] = list()
        s = self.userdb.userRegister(u)
        if s==True:
            print("You Registered")
            self.userLogin()
        else:
            print("You couldn't register due to an error, try again later")
            self.userRegister()
    def balanceAdd(self):
        print("current balance : "+str(self.user["balance"]))
        b=float(input("amount to be added : "))
        newbalance = self.user["balance"]+b
        s = self.userdb.balanceAdd(self.user["_id"],newbalance)
        if s ==True:
            self.user["balance"]=newbalance
            print("Balance Added. Current balance : "+str(self.user["balance"]))
        else:
            print("Unable to add balance due to an error, try again later")

class Basket:
    def __init__(self) -> None:
        self.productdb=database.ProductDB()
        self.userdb=database.UserDB()
        self.salesdb=database.SalesDB()
    def basketSelect(self,userid):
        print("basket select".center(30,"-"))
        basket = self.userdb.basketSelect(userid)
        if basket == False:
            print("basket could not be listed due to an error, try again later")
        else:
            basket=list(basket)
            df=pd.DataFrame(basket)
            if len(df)== 0:
                print("There are currently no basket sold")
            else :
                print(df)
    def basketAdd(self,userid):
        print("add to Basket".center(30,"-"))
        productid=input("Product Id : ")
        products = self.productdb.productSelect()
        df=pd.DataFrame(products)
        df=df[df["seller"]!=userid]
        if productid in str(df["_id"].values):
            unit=input("Unit : ")
            s = self.userdb.basketAdd(userid,productid,unit)
            if s==False:
                print("The product could not be added to the cart due to an error, try again later")
            else:
                print("product added to cart")
        else:
            print("There Is No Product Sold At The Id You Entered")
            
    def basketDel(self,userid):
        print("basket delet".center(30,"-"))
        productid=input("Product Id : ")
        baskett = self.userdb.basketSelect(userid)
        df=pd.DataFrame(baskett)
        if productid in str(df["productid"].values):
            s = self.userdb.basketDel(userid,productid)
            if s==False:
                print("The product could not be deleted from the cart due to an error, try again later")
            else:
                print("product deleted to cart")
        else:
            print("There is no product in the cart with the ID you entered.")
    def salesAdd(self,userid):
        print("sales".center(30,"-"))
        basket = self.userdb.basketSelect(userid)
        if basket == False:
            print("error")
        else:
            basket=list(basket)
            if len(basket)== 0:
                print("There are currently no basket sold")
            else :
                saleslist=[]
                for i in basket:
                    s = self.productdb.sellingControls(i)
                    if s == None or s==False:
                        print("Id : "+str(i["productid"])+" (this product is missing or not sufficient)")
                    else:
                        del s["stockAmount"]
                        s["unit"] = i["unit"]
                        s["price"]=int(s["unit"])*int(s["unitPrice"])
                        saleslist.append(s)
                else:
                    df=pd.DataFrame(saleslist)
                    if len(df)!=0:
                        print(df)
                        print("Total Price : "+str(df["price"].sum()))
                        s = input("complete the purchase(y/n) : ")
                        if s=="y":
                            totalprice = df["price"].sum()
                            self.salesAddContiune(saleslist,totalprice,userid)
                        elif s=="n":
                            print("going back")
                        else :
                            print("There is no such option, try again")
                    else:
                        print("There are no items in your cart")
    def salesAddContiune(self,saleslist,tp,userid):
        s = self.userdb.balanceControl(userid,tp)
        if s ==True:
            for i in saleslist:
                self.productdb.poductUpdate(i["_id"],i["unit"])
                self.userdb.balanceUpdateAdd(i["seller"],i["price"])
            self.userdb.balanceUpdateDel(userid,tp)
            s = self.salesdb.salesAdd(saleslist,tp,userid)
            if s==True:
                print("I wish you to use the products you bought in good days. have a nice day")
            else:
                print("error")
        else:
            print("insufficient balance,go back")
 
class Product:
    def __init__(self):
        self.productdb=database.ProductDB()

    def buyingTransactions(self,userid):
        basket=Basket()
        while True:
            print("buying transactions".center(30,"-"))
            s=input("   1 : product list\n   2 : Basket list\n   3 : add to Basket\n   4 : delete to basket\n   5 : buy items in cart\n   q : turn back\nİşlem : ")
            if s=="q":
                break
            elif s=="1":
                self.productSelect(userid)
            elif s=="2":
                basket.basketSelect(userid)
            elif s=="3":
                basket.basketAdd(userid)
            elif s=="4":
                basket.basketDel(userid)
            elif s=="5":
                basket.salesAdd(userid)
            else:
                print("There is no such option, try again")
    def productSelect(self,userid):
        products=self.productdb.productSelect()
        if products == False:
            print("Products could not be listed due to an error, try again later")
        else:
            products=list(products)
            productdf=pd.DataFrame(products)
            productdf=productdf[productdf["seller"]!=userid]
            if len(productdf) == 0:
                print("There are currently no products sold")
            else :
                print(productdf)

    def sellingTransactions(self,userid):
        while True:
            print("selling transactions".center(30,"-"))
            s=input("   1 : list the products you sell\n   2 : add product\n   3 : delete product\n   q : turn back\nİşlem : ")
            if s=="q":
                break
            elif s=="1":
                self.productById(userid)
            elif s=="2":
                self.productAdd(userid)
            elif s=="3":
                self.productDel()
            else:
                print("There is no such option, try again")

    def productAdd(self,userid):
        print("add product".center(30,"-"))
        p=dict()
        p["name"]=input("Name         : ")
        p["unitPrice"]=input("Unit Price   : ")
        p["stockAmount"]=input("Stock Amount : ")
        p["seller"]=userid
        s = self.productdb.productAdd(p)
        if s==True:
            print("product added")
        else:
            print("The product could not be added as a result of an error, try again later")
    
    def productDel(self):
        print("Delete product".center(30,"-"))
        productid=input("product id to be deleted : ")
        s = self.productdb.productDel(productid)
        if s==True:
            print("product Deleted")
        else:
            print("The product could not be deleted as a result of an error, try again later")
    
    def productById(self,userid):
        print("the products you sell".center(30,"-"))
        products=self.productdb.productById(userid)
        if products == False:
            print("Products could not be listed due to an error, try again later")
        else:
            products=list(products)
            if len(products) == 0:
                print("You do not have any products for sale.")
            else :
                productdf=pd.DataFrame(products)
                print(productdf)