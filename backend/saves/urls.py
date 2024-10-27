from django.urls import path
from .views import SaveSceneView

urlpatterns = [
    path('save/', SaveSceneView.as_view(), name='save-scene'),
]