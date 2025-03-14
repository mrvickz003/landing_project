from django.urls import path
from landing.views import (
    landing,
    auth,
    bills
    )


urlpatterns = [
    path('', landing.home_view, name='home'),  # Root URL
    path('login', auth.user_login, name='login'),
    path('savebilldatas', bills.save_bill_data, name='savebilldatas'),
    path("validate-token", auth.validate_token, name="validate_token"),
]
