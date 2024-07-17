from django_filters.rest_framework import DjangoFilterBackend
from App.models import *
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status, generics
from App.models import Article
from django.http import JsonResponse
from rest_framework.pagination import LimitOffsetPagination
from App.Serelizer.articleserelizier import ArticelSerelizer
from django.contrib.auth.models import User
from App.utils.filter import ArticleFilter


class article (generics.ListCreateAPIView):
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    serializer_class = ArticelSerelizer
    filterset_fields = ['id', 'title', 'content']
    search_fields = ['id', 'title', 'content']

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


class articles (generics.ListCreateAPIView):
    queryset = Article.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = LimitOffsetPagination
    serializer_class = ArticelSerelizer
    SearchFilter = ['id', 'title', 'content']

    def list(self, request):
        try:
            objects = self.get_queryset()
            serelizer = self.get_serializer(data=objects, many=True)
            serelizer.is_valid()
            page = self.paginate_queryset(objects)
            if page is not None:
                pageserializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(pageserializer.data)
            return Response(serelizer.data)
        except Exception as e:
            return JsonResponse({'Error': 'No Data Matches'})

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


class articley (generics.ListCreateAPIView):
    # Metode Cacth Semua Data
    queryset = Article.objects.all()

    # Pageignation
    pagination_class = LimitOffsetPagination

    # Serializer
    serializer_class = ArticelSerelizer

    # Filter
    filter_backends = [DjangoFilterBackend]

    # Class Filter
    filterset_class = ArticleFilter

    def list(self, request):
        try:
            objects = self.get_queryset()
            serelizer = self.get_serializer(data=objects, many=True)
            serelizer.is_valid()
            page = self.paginate_queryset(objects)
            if page is not None:
                pageserializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(pageserializer.data)
            return Response(serelizer.data)
        except Exception as e:
            return JsonResponse({'Error': 'No Data Matches'})

    def create(self, request, *args, **kwargs):
        try:
            # Mendapatkan ID User
            get_userid = User.objects.get(id=request.data.get('id'))

            # create Articel
            Article(
                title=request.data.get('title'),
                image=request.File.get('image'),
                content=request.data.get('content'),
                slug=request.data.get('slug'),
                author=get_userid,
                status=request.data.get('status'),
                created_at=request.data.get('create'),
                updated_at=request.data.get('update'),
            )

            # save article
            Article.save()

            response = {
                "status": status.HTTP_200_OK,
                "message": "Article Created",
            }

            return Response(response)
        except Exception as e:

            response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Article Created : Failed",
                "data": "Null"
            }

            return Response(response)


class ArticleUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticelSerelizer
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


#################################################################################################################################
# @method_decorator(csrf_exempt, name='dispatch')
# class article(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticelSerelizer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     pagination_class = pagination.LimitOffsetPagination

#     def list(self, request):
#         objects = self.get_queryset()
#         page = self.paginate_queryset(objects)
#         serializer = self.get_serializer(page, many=True)
#         if page is not None:
#             return self.get_paginated_response(serializer.data)
#         return Response(serializer.data)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         try:
#             serializer.is_valid(raise_exception=True)
#             self.perform_create(serializer)
#             response = {
#                 "status": status.HTTP_201_CREATED,
#                 "message": "Article Created",
#                 "data": serializer.data
#             }
#             return Response(response)
#         except Exception as e:
#             response = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "message": "Article Creation Failed",
#                 "data": "Null"
#             }
#             return Response(response)
