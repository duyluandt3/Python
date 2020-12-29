# Get many value without define in init

class Car:
    def __init__(self, **kwargs):
        self._Data = kwargs

    # Get data
    def GetCarName(self):
        return self._Data["Name"]
    def GetModel(self):
        return self._Data["Type"]
    def GetPrice(self):
        return self._Data["Price"]

def main():
    Car1 = Car(Name="Toyota", Type="Inova", Price = "1000000")
    print(Car1.GetCarName())
    print(Car1.GetModel())
    print(Car1.GetPrice())

if __name__ == '__main__':main()
