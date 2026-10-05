from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
from documents.views import document_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/research/',include("research.urls")),
    path('api/documents/',include("documents.urls")),
    path(
    "documents/",
    document_dashboard,
    name="documents-dashboard"
    ),
    path("accounts/", include("accounts.urls")),
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
