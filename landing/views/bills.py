from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from landing.serializers import BillSerializer

@api_view(['POST'])
def save_bill_data(request):
    new_bills = request.data.get("new_bills", [])
    if not new_bills:
        return Response({"error": "No bill data provided."}, status=status.HTTP_400_BAD_REQUEST)

    for bill_data in new_bills:
        bill_data = {
            "date": bill_data.get("Date"),
            "time": bill_data.get("Time"),
            "cashier": bill_data.get("Cashier"),
            "bill_no": bill_data.get("BillNo"),
            "food_pickup": bill_data.get("FoodPickup"),
            "payment_method": bill_data.get("PaymentMethod"),
            "menu": bill_data.get("Menu"),
            "sub_total": bill_data.get("SubTotal"),
            "gst_price": bill_data.get("GSTPrice"),
            "round_off": bill_data.get("RoundOff"),
            "grand_total": bill_data.get("GrandTotal"),
        }

        serializer = BillSerializer(data=bill_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Bills saved successfully!"}, status=status.HTTP_201_CREATED)
