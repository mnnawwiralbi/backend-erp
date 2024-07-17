from rest_framework import generics, status
from rest_framework.response import Response
from App.models import DetailPembuatJanji
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from App.Serelizer.janjiserializer import JanjiSerializer, JanjiSerializerUpdate
from rest_framework.permissions import AllowAny


class DetailPembuatJanjiView (generics.ListCreateAPIView):
    queryset = DetailPembuatJanji.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [AllowAny]
    pagination_class = LimitOffsetPagination
    serializer_class = JanjiSerializer
    filterset_fields = ['id', 'perusahaan', 'alamat_perusahaan']
    search_fields = ['id', 'perusahaan', 'alamat_perusahaan']

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


class DetailPembuatJanjiUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetailPembuatJanji.objects.all()
    serializer_class = JanjiSerializerUpdate
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Updated",
            "data": serializer.data
        }
        return Response(response)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        response = {
            "status": status.HTTP_200_OK,
            "message": "Article Deleted",
        }
        return Response(response, status=status.HTTP_200_OK)
