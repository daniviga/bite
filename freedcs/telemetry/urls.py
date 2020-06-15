"""freedcs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from telemetry.views import TelemetryView, TelemetryLatest, TelemetryRange

urlpatterns = [
    path('',
         TelemetryView.as_view({'post': 'create'}),
         name='telemetry'),
    path('<str:device>/',
         TelemetryView.as_view({'get': 'list'}),
         name='device-telemetry'),
    path('<str:device>/last/',
         TelemetryLatest.as_view({'get': 'retrieve'}),
         name='device-telemetry-last'),
    path('<str:device>/<str:time_from>/',
         TelemetryRange.as_view({'get': 'list'}),
         name='device-telemetry-single'),
    path('<str:device>/<str:time_from>/<str:time_to>/',
         TelemetryRange.as_view({'get': 'list'}),
         name='device-telemetry-range'),
]
