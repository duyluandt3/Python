import  _thread
import time

def CounterDown(TheardName):
    count = 10
    while(0 <= count):
        print("{}, Count:{}\n".format(TheardName, count))
        count -= 1
        time.sleep(2)

def main():
    try:
        _thread.start_new_thread(CounterDown, ("Thread1",))
        _thread.start_new_thread(CounterDown, ("Thread2",))
        print("Thread is running")
    except:
        print("Error")
    while 1:
        pass


if __name__ == '__main__':main()
