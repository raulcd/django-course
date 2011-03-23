from piston.handler import BaseHandler
from piston.utils import require_mime, rc
from django.contrib.auth.models import User

class UserHandler(BaseHandler):
    # Model to tie to
    model = User
    # Allowed HTTP methods
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE',)
    # List of fields to include in response
    fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'is_superuser', 'last_login', 'date_joined', ('groups', ('id', 'name')))


    # Response implementation of GET requests
    def read(self, request, user_id=None):
        if user_id: # querying for a specific user
            if request.user.is_superuser or request.user.id == user_id:
                return User.objects.get(pk=user_id) # return a user
        elif request.user.is_superuser: # querying for all user
            return User.objects.all() # return all users
        
        return rc.FORBIDDEN


    # Response implementation of POST requests
    # Only accept application/json content type
    @require_mime('json',)
    def create(self, request):
        if not request.user.is_superuser:
            return rc.FORBIDDEN # returns HTTP 401
        # Request body
        data = request.data
        # Saving user
        user = User()
        for key in data.iterkeys():
            # Setting user field (key)
            user.__dict__[key] = data[key]
        user.save()
        
        return user
        
    
    # Response implementation of PUT requests
    # Only accept application/json content type
    @require_mime('json',)
    def update(self, request, user_id=None):
        try: 
            if not request.user.id or (request.user.id != user_id and not request.user.is_superuser):
                return rc.FORBIDDEN # returns HTTP 401
            
            # Request body
            data = request.data
            
            # Updating user
            user = User.objects.get(pk=user_id)
            for key in data.iterkeys():
                # Updating user field (key)
                user.__dict__[key] = data[key]
            user.save()
            
            return rc.ALL_OK
            
        except User.DoesNotExist:         
            return rc.NOT_FOUND # returns HTTP 404


    # Response implementation of DELETE requests
    def delete(self, request, user_id=None):
        try:
            if not request.user.id or (request.user.id != user_id and not request.user.is_superuser):
                return rc.FORBIDDEN # returns HTTP 401
            
            # Deleting user    
            user = User.objects.get(pk=user_id)
            user.delete()
            
            return rc.DELETED # returns HTTP 204
    
        except User.DoesNotExist:         
            return rc.NOT_FOUND # returns HTTP 404
