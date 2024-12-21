from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('list', views.DoctorsViewset)
router.register('spacialities', views.SpacialitiesViewset)
router.register('designations', views.DesignationsViewset)
router.register('availableTime', views.AvailableTimeViewset)
router.register('reviews', views.ReviewsViewset)

urlpatterns = [
    path('', include(router.urls)), 
]