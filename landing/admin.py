from django.contrib import admin
from landing.models import (
    Company,
    CustomUser,
    BillDetails,
    deletedBillDetails
)

admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(BillDetails)
admin.site.register(deletedBillDetails)
