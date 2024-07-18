from rest_framework import generics, status
from rest_framework.response import Response
from App.models import ReviewUser
from rest_framework.filters import SearchFilter, OrderingFilter
from App.Serelizer.reviewserializer import ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

class ReviewView (generics.ListCreateAPIView):
    queryset = ReviewUser.objects.all()
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    serializer_class = ReviewSerializer
    filterset_fields = ['id', 'name', 'content']
    search_fields = ['id', 'name', 'content']

    def create(self, request, *args, **kwargs):
        # try:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Created",
            "data": serializer.data
        }
        return Response(response)
        # except Exception as e:
        #     response = {
        #         "status": status.HTTP_400_BAD_REQUEST,
        #         "message": "Article Created : Failed",
        #         "data": "Null"
        #     }
        #     return Response(response)


class ReviewUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReviewUser.objects.all()
    serializer_class = ReviewSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.image.delete()
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Updated",
            "data": serializer.data
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.image.delete()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Deleted",
        }
        return Response(response, status=status.HTTP_200_OK)
