from bson import ObjectId
import pymongo

class MarketDB:
    def __init__(self):
        mongodb=pymongo.MongoClient("mongodb://localhost:27017/")
        self.marketdb=mongodb["marketdb"]

class UserDB(MarketDB):
    def __init__(self):
        MarketDB.__init__(self)
        self.userdb = self.marketdb["user"]
    def userLogin(self,name,password):
        try:
            query={
                "name" : name,
                "password" : password
            }
            user = self.userdb.find_one(query)
        except:
            return False
        else:
            return user
    def userRegister(self,user):
        try:
            self.userdb.insert_one(user)
        except:
            return False
        else:
            return True
    def balanceAdd(self,userid,newbalance):
        try:
            query={
                "_id" :ObjectId(userid)
            }
            newvalues={ 
                "$set" : { 
                    "balance" : newbalance
                }
            }
            self.userdb.update_one(query,newvalues)
        except:
            return False
        else:
            return True
    def basketSelect(self,userid):
        try:
            query={
                "_id":ObjectId(userid)
            }
            user=self.userdb.find_one(query)
            userbasket=user["basket"]
        except:
            return False
        else:
            return userbasket        
    def basketAdd(self,userid,productid,unit):
        try:
            basket = self.basketSelect(userid)
            if basket!=False:
                dictt={
                    "productid":productid,
                    "unit":unit
                }
                basket.append(dictt)
            query={
                "_id":ObjectId(userid)
            }
            newvalues={
                "$set":{"basket" : basket}
            }
            s=self.userdb.update_one(query,newvalues)
        except:
            return False
        else:
            return True
    def basketDel(self,userid,productid):
        try:
            basket = self.basketSelect(userid)
            if basket!=False:
                basket=list(basket)
                for i in range(len(basket)):
                    if productid ==basket[i]["productid"]:
                        basket.pop(i)
                query={
                    "_id":ObjectId(userid)
                }
                newvalues={
                    "$set":{
                        "basket":basket
                    }
                }
                self.userdb.update_one(query,newvalues)
        except:
            return False
        else:
            return True
    def balanceUpdateAdd(self,userid,unit):
        try:
            query={
                "_id" : ObjectId(userid)
            }
            u = self.userdb.find_one(query)
            u =dict(u)
            u = int(u["balance"])
            u+=int(unit)
            newvalues={
                "$set":{
                    "balance" : u
                }
            }
            self.userdb.update_one(query,newvalues)
        except:
            pass
    def balanceUpdateDel(self,userid,tp):
        try:
            query={
                "_id" : ObjectId(userid)
            }
            u = self.userdb.find_one(query)
            u =dict(u)
            u = int(u["balance"])
            u-=int(tp)
            newvalues={
                "$set":{
                    "balance" : u,
                    "basket":[]
                }
            }
            self.userdb.update_one(query,newvalues)
        except:
            pass
    def balanceControl(self,userid,tp):
        try:
            query={
                "_id" : ObjectId(userid)
            }
            u = self.userdb.find_one(query)
            u =dict(u)
            u = int(u["balance"])
            if u>=int(tp):
                return True
            else:
                return False
        except:
            False

class ProductDB(MarketDB):
    def __init__(self):
        MarketDB.__init__(self)
        self.productdb = self.marketdb["product"]
    def productAdd(self,product):
        try:
            self.productdb.insert_one(product)
        except:
            return False
        else:
            return True
    def productDel(self,productid):
        try:
            query={
                "_id":ObjectId(productid)
            }
            self.productdb.delete_one(query)
        except:
            return False
        else:
            return True
    def productById(self,userid):
        try:
            query={
                "seller":ObjectId(userid),
            }
            filterr={
                "seller":0
            }
            products = self.productdb.find(query,filterr)
        except:
            return False
        else:
            return products
    def productSelect(self):
        try:
            products = self.productdb.find()
        except:
            return False
        else:
            return products
    def sellingControls(self,product):
        try:
            query={
                "_id": ObjectId(product["productid"])
            }
            p = self.productdb.find_one(query)
            p=dict(p)
            if int(product["unit"]) > int(p["stockAmount"]):
                return False
        except:
            return False
        else:
            return p
    def poductUpdate(self,userid,unit):
        try:
            query={
                "_id" : ObjectId(userid)
            }
            p = self.productdb.find_one(query)
            p = dict(p)
            p = int(p["stockAmount"])
            p-=int(unit)
            newvalues={
                "$set":{
                    "stockAmount":p
                }
            }
            self.productdb.update_one(query,newvalues)
        except:
            pass

class SalesDB(MarketDB):
    def __init__(self):
        MarketDB.__init__(self)
        self.salesdb = self.marketdb["sales"]
    def salesAdd(self,saleslist,tp,userid):
        try:
            import datetime
            saleslist=list(saleslist)
            salesdict={
                "products":saleslist,
                "buyer":ObjectId(userid),
                "totalPrice":float(tp),
                "datetime":datetime.datetime.now()
            }
            self.salesdb.insert_one(salesdict)
        except:
            return False
        else:
            return True