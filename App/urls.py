from django.urls import path
from App.Api.article import article, ArticleUpdateDelete
from App.Api.register import register, RegisterView
from App.Api.auth import authis, LoginSimpleJwtTokenObtain, LoginSimpleJwtRefreshToken, AuthSerializerFormEmail, AuthSerializerFormUsername
from App.Api.banner import BannerView, BannerUpdateDelete
from App.Api.service import ServiceView
from App.Api.janji import DetailPembuatJanjiView, DetailPembuatJanjiUpdateDelete
from App.Api.review import ReviewView, ReviewUpdateDelete
from App.Api.service import ServiceUpdateDelete, ServiceView
from App.Api.logout import LogoutView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from App.Api.logout import LogoutView


urlpatterns = [
    path('article/', article.as_view()),
    path('articleupdate/<int:id>/', ArticleUpdateDelete.as_view()),
    path('banner/', BannerView.as_view()),
    path('bannerupdate/<str:name>/', BannerUpdateDelete.as_view()),
    path('service/', ServiceView.as_view()),
    path('serviceupdate/<str:status>/', ServiceUpdateDelete.as_view()),
    path('detailpembuatjanji/', DetailPembuatJanjiView.as_view()),
    path('detailpembuatjanjiupdate/<int:id>/',
         DetailPembuatJanjiUpdateDelete.as_view()),
    path('review/', ReviewView.as_view()),
    path('reviewupdate/<int:id>/', ReviewUpdateDelete.as_view()),
    path('register/', RegisterView.as_view()),
    path('auth/', AuthSerializerFormEmail.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
