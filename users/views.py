from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework import mixins
from rest_framework import viewsets


from .serializers import UserSerializer
from base.models import User


class UserAPISet(viewsets.ViewSet):
    def list(self, request):
        queryset = User.users.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response('Failed creating the user')

    def retrieve(self, request, pk=None):
        user = User.users.get(id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = User.users.get(id=pk)
        serializer = UserSerializer(data=queryset)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response('Failed updating the user')

    def partial_update(self, request, pk=None):
        queryset = User.users.get(id=pk)
        serializer = UserSerializer(data=queryset)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response('Failed updating the user')

    def destroy(self, request, pk=None):
        user = User.users.get(id=pk)
        if user is not None:
            user.delete()
            return Response('User deleted Successfulyy')
        return Response('Failed deleting the user')

    def get_permissions(self):

        if self.detail == False:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]




class UserAPIModelSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.users.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

