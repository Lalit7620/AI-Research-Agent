from django.urls import path

from .views import ResearchView,ResearchHistoryView,ResearchDetailView


urlpatterns = [
    path(
        "",
        ResearchView.as_view(),
        name="research",
    ),
    
    path(
        "history/",
        ResearchHistoryView.as_view(),
        name="research-history"
    ),
    path(
        "<int:request_id>/",
        ResearchDetailView.as_view(),
        name="research-detail"
    ),

]