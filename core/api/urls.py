"""thesevenREST_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from .views import *

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('', StatusListSearchAPIView.as_view()),
    path('', ItemListAPIView.as_view()),
    path('create/', ItemCreateAPIView.as_view()),
    path('country/', CountryListAPI.as_view()),
    # path('<int:id>/', StatusDetailAPIView.as_view()),
    # path('<int:pk>/update/', StatusUpdateAPIView.as_view()),
    # path('<int:pk>/delete/', StatusDeleteAPIView.as_view()),

]

# 'status/api' --> List View
# 'status/api/create/' -- >Create View
# status/api/<int:id>/' -->  Detail View
# status/api/<int:id>/update' --> Update View
# status/api/<int:id>/delete' --> Delete
