from django.urls import path
from .views import ResearchRequestCreateView

urlpatterns = [
    path(
        "",
        ResearchRequestCreateView.as_view(),
        name="research-create"
    )
]
