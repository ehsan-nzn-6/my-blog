from django.urls import path
from dakhlokharj import views

app_name = "dakhlokharj"
urlpatterns = [
    path("", views.DakhlOKharjListView.as_view(), name="DakhlOKharjList"),
    path("create/", views.DakhlOKharjCreateView.as_view(), name="DakhlOKharjCreate"),
    path(
        "update/<int:pk>",
        views.DakhlOKharjUpdateView.as_view(),
        name="DakhlOKharjUpdate",
    ),
    path(
        "delete/<int:pk>",
        views.DakhlOKharjDeleteView.as_view(),
        name="DakhlOKharjDelete",
    ),
]
