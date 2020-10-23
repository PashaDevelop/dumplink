from django.urls import path
from .views import dump, restore, remove


urlpatterns = [
    path('dump/', dump),
    path('restore/', restore),
    path('remove/<uuid:param_id>/', remove)
]