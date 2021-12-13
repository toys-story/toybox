import datetime

def logging(func):
    func_name = func.__name__
    
    def wrapper(*args, **kwargs):
        print(f"{datetime.datetime.now()}  Start {func_name}")
        res = func(*args, **kwargs)
        print(f"{datetime.datetime.now()}   End  {func_name}")
        return res

    return wrapper