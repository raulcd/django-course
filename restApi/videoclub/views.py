from models import Category, Video
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def categoriesTemplate(request):
    categories = Category.objects.all()
    return render_to_response('categories.html',{'categories': categories},
                              context_instance=RequestContext(request))
         
def videosRest(request):
    if request.method == 'GET':
        #TO-DO: devolver JSON con los videos
        print ""
    elif request.method == 'POST':
        #TO-DO: recibe un JSON con nuevo video y lo crea
        print ""