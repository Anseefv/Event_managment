from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import*
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('pending',PendingListView,basename='pending')
router.register('profile',ProfileViewSet,basename='profile')

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/', obtain_auth_token),
    path('pending/<int:pk>/<str:decision>/', DecidingApiView.as_view()),


]+ router.urls