from rest_framework import generics, status
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import User
from App.Serelizer.accountserelizer import accountserelizers, AccountSerializerRegisterSuperUser
from rest_framework.permissions import AllowAny
from django.contrib.auth.apps import AuthConfig
from rest_framework.authentication import TokenAuthentication


class register (generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = accountserelizers
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
            serializer = self.get_serializer(query, many=True)

            # id = 1
            # cobanama = User.get_username
            # serializercoba = self.get_serializer(cobanama, many=True)

            # querpas = User.objects.get(email='abdul@gmail.com')
            # checkpassword = querpas.check_password('1234')
            # checkusername = querpas.get_username()

            return Response({'data': serializer.data})
        except Exception as e:
            return JsonResponse({'message': 'Failed to fetch data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'message': 'Success: Data created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Failed to create data', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class registerao (generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = accountserelizers
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        try:
            query = self.get_queryset()
            serializer = self.get_serializer(query, many=True)

            # id = 1
            # cobanama = User.get_username
            # serializercoba = self.get_serializer(cobanama, many=True)

            # querpas = User.objects.get(email='abdul@gmail.com')
            # checkpassword = querpas.check_password('1234')
            # checkusername = querpas.get_username()

            return Response({'data': serializer.data})
        except Exception as e:
            return JsonResponse({'message': 'Failed to fetch data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response({'message': 'Success: Data created'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Failed to create data', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializerRegisterSuperUser

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': 'Failed to fetch data', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()  # This will call the create method in the serializer
            return Response({'message': 'Success: Data created', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Failed to create data', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
