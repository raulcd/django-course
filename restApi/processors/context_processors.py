from datetime import date

def today(request):
        
    return {'today': date.today()}
 
