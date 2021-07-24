from datetime import datetime, timedelta
def main():
    valid = {1,2,3,4,10,11,12}
    month = '05'
    if int(month) in valid:
        print("regular")
    else:
        print("playoffs")

if __name__=="__main__":
    main()