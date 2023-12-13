"""
URL configuration for api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import sys

schema_view = get_schema_view(
    openapi.Info(
        title="Sua Grade UnB - API",
        default_version='v1',
        description="""
        <div>
            O Sua Grade UnB é um projeto da matéria Métodos de Desenvolvimento de Software, a qual tem como objetivo auxiliar os alunos da Universidade de Brasília a montarem suas grades horárias de maneira fácil e intuitiva. </br>
            Contribuidores: </br>
            <ul>
                <li>Arthur Ribeiro e Sousa (<a target='_blank' href='https://github.com/artrsousa1'>@artrsousa1</a>)</li>
                <li>Caio Falcão Habibe Costa (<a target='_blank' href='https://github.com/CaioHabibe'>@CaioHabibe</a>)</li>
                <li>Caio Felipe Rocha Rodrigues (<a target='_blank' href='https://github.com/caio-felipee'>@caio-felipee</a>)</li>
                <li>Gabriel Henrique Castelo Costa (<a target='_blank' href='https://github.com/GabrielCastelo-31'>@GabrielCastelo-31</a>)</li>
                <li>Henrique Camelo Quenino (<a target='_blank' href='https://github.com/henriquecq'>@henriquecq</a>)</li>
                <li>Mateus Vieira Rocha da Silva (<a target='_blank' href='https://github.com/mateusvrs'>@mateusvrs</a>)</li>
            </ul>
            </br>
            Mais especificações sobre o projeto por completo podem ser encontradas <a href='https://github.com/unb-mds/2023-2-SuaGradeUnB/'>aqui</a>.
        </div>
        """,
        contact=openapi.Contact(email="suagradeunb@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Documentation
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),

    # Views
    path('users/', include('users.urls')),
    path('courses/', include('api.urls'))
]

if 'test' in sys.argv:
    urlpatterns += [
        path('utils/', include('utils.urls'))
    ]
