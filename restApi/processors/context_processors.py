from datetime import date

def today(request):
        
    return {'DATE': date.today()}
 
