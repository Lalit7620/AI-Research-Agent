from django.urls import path

from .views import ResearchView


urlpatterns = [
    path(
        "",
        ResearchView.as_view(),
        name="research",
    ),
]