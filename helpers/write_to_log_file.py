import datetime 

def write_to_log_file(file, details):
    f = open('./logs/'+str(file)+"-"+str(datetime.date.today())+".log", "a")
    f.write(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + details + "\n")
    f.close()
    return True