from rest_framework import generics, status
from rest_framework.response import Response
from App.models import Banner
from rest_framework.filters import SearchFilter, OrderingFilter
from App.Serelizer.bannerserializer import BannerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination


class BannerView (generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    serializer_class = BannerSerializer
    filterset_fields = ['id', 'name', 'description']
    search_fields = ['id', 'name', 'description']

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = {
                "status": status.HTTP_200_OK,
                "message": "Article Created",
                "data": serializer.data
            }
            return Response(response)
        except Exception as e:
            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Article Created : Failed",
                "data": "Null"
            }
            return Response(response)


class BannerUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'name'

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
