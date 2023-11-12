from django.contrib import admin
from django.urls import path, include

import car_dealer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('car_dealer.urls')),
]
