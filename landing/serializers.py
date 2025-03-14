from landing.models import BillDetails, CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "company",
            "first_name",
            "last_name",
            "email",
            "mobile_number",
            "password",
            "is_superuser",
            "is_active",
            "is_staff",
            "last_login",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillDetails
        fields = [
            "id",
            "date",
            "time",
            "cashier",
            "bill_no",
            "food_pickup",
            "payment_method",
            "menu",
            "sub_total",
            "gst_price",
            "round_off",
            "grand_total",
        ]
        read_only_fields = ["id", "cashier"]

    def to_internal_value(self, data):
        camel_case_data = {}
        for key, value in data.items():
            # Convert camelCase to snake_case
            snake_case_key = self.camel_to_snake(key)
            camel_case_data[snake_case_key] = value
        return super().to_internal_value(camel_case_data)

    def camel_to_snake(self, name):
        import re
        # Convert camelCase to snake_case using regex
        return re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
