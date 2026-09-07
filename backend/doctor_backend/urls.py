from django.contrib import admin
from django.urls import include, path

from data_doctor.views import dashboard


urlpatterns = [

    path("admin/",admin.site.urls),

    path("",dashboard,name="dashboard"),

    path("api/",include("data_doctor.urls")),

]