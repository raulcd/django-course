from djangorestframework.views import View
from djangorestframework.renderers import JSONRenderer
from djangorestframework.response import Response
from djangorestframework.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND,\
    HTTP_200_OK, HTTP_204_NO_CONTENT
from djangorestframework.resources import ModelResource
from django.contrib.auth.models import User, Group
from djangorestframework.parsers import JSONParser


class GroupResource(ModelResource):
    model = Group
    fields = ('id', 'name',)


class UserResource(ModelResource):
    model = User
    fields = ('id', 'username', 'first_name', 'last_name',
              'email', 'is_staff', 'is_active', 'is_superuser',
              'last_login', 'date_joined', ('groups', GroupResource))


class UserView(View):
    # Only return application/json response content
    renderers = (JSONRenderer,)
    # Only accept application/json request content
    parsers = (JSONParser,)
    resource = UserResource

    # Response implementation of GET requests
    def get(self, request, user_id):
        try:
            if request.user.is_superuser or request.user.id == user_id:
                return User.objects.get(pk=user_id)  # return a user

            return Response(status=HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)  # returns HTTP 404

    # Response implementation of PUT requests
    def put(self, request, user_id):
        try:
            if (not request.user.id) or (request.user.id != user_id and not request.user.is_superuser):
                return Response(status=HTTP_403_FORBIDDEN)  # returns HTTP 403

            # Request body
            data = self.DATA

            # Updating user
            user = User.objects.get(pk=user_id)
            for key in data.iterkeys():
                # Updating user field (key)
                user.__dict__[key] = data[key]
            user.save()

            return Response(status=HTTP_200_OK)

        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)  # returns HTTP 404

    # Response implementation of DELETE requests
    def delete(self, request, user_id):
        try:
            if (not request.user.id) or (request.user.id != user_id and not request.user.is_superuser):
                return Response(status=HTTP_403_FORBIDDEN)  # returns HTTP 403

            # Deleting user
            user = User.objects.get(pk=user_id)
            user.delete()

            return Response(status=HTTP_204_NO_CONTENT)  # returns HTTP 204

        except User.DoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)  # returns HTTP 404


class UserViewRoot(View):
    # Only return application/json response content
    renderers = (JSONRenderer,)
    # Only accept application/json request content
    parsers = (JSONParser,)
    resource = UserResource

    # Response implementation of GET requests
    def get(self, request):
        if request.user.is_superuser:
            return User.objects.all()  # return all users

        return Response(status=HTTP_403_FORBIDDEN)

    # Response implementation of POST requests
    def post(self, request):
        if not request.user.is_superuser:
            return Response(status=HTTP_403_FORBIDDEN)  # returns HTTP 403
        # Request body
        data = self.DATA
        # Saving user
        user = User()
        for key in data.iterkeys():
            # Setting user field (key)
            user.__dict__[key] = data[key]
        user.save()

        return user
