from django.urls import path


from .views import (
                    EmailAuthToken, 
                    UserAPIView, 
                    )

urlpatterns = [
    # auth urls
    path('signup/', UserAPIView.as_view(), name='signup'),
    path('login/', EmailAuthToken.as_view(), name='login'),
]