import datetime

due = '2020-08-15 23:59:00'
now = datetime.date.today()
def date_parser(due):
    date = due.split(" ")[0]
    
    date = date.split("-")

    date = datetime.date(int(date[0]),int(date[1]),int(date[2]))
    return date 

def renew_decision():
    due_date =  date_parser(due)
    remaining = due_date - now
    binod = datetime.timedelta(days=1)
    if(remaining > binod):
        print('Aro pore')
    else:
        print('Now')

renew_decision()