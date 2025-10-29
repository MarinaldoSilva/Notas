from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/cadastrar/', include('Users.urls')),
    path('api/v1/', include('Notas.urls'))
]
