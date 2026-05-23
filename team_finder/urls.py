from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = [
    path(
        "",
        RedirectView.as_view(url="/projects/list/", permanent=False),
        name="home",
    ),
    path("projects/", include("projects.urls")),
    path("users/", include("users.urls")),
]
