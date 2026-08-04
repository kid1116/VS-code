class Car:
    wheel=4

    def __init__(self, c_brand, c_name, c_price):
        self.brand = c_brand
        self.name = c_name
        self.price = c_price

    def running(self):
         print(f"{self.brand} {self.name} is running.")

    def total_price(self,discount,rate):
        """
        计算总价格
        """
        return self.price*discount+self.price*rate

c1=Car("XiaoMi","Su7",250000)
c1.name="Yu7" 
c1.running()
print(c1.wheel)
   