from django.contrib.auth.models import User
from django.conf import settings
import ldap

class LDAPBackend:
    
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self,username=None,password=None):
        #check against the LDAP server
        if not self.is_valid(username,password):
            return None
        try:
            #if the user is registered in the LDAP search the User instance
            #to link the user to the session 
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            #create a User instance to link the user to the session
            user = User(username=username)
            #do not save the password of the user
            user.set_unusable_password()
            user.save()

        return user

    def get_user(self,user_id):
        #an authenticated user has a User instance in our system
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def is_valid (self,username=None,password=None):
        # do no allow empty usernames/passwords
        if username == None or password == '':
            return False
        try:
            #search the ldap for the user
            l = ldap.initialize(settings.AD_LDAP_URL)
            l.simple_bind_s(settings.AD_SEARCH_DN % (username), password)
            l.unbind_s()
            return True
        except Exception, e:
            return False
