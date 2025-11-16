# backend/api/views.py

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CR, Student
from .serializers import CRSerializer, StudentSerializer
from .utils import send_whatsapp_message
import threading

# ================= CR Signup =================
class CRSignupView(generics.CreateAPIView):
    queryset = CR.objects.all()
    serializer_class = CRSerializer


# ================= CR Login =================
class CRLoginView(generics.GenericAPIView):
    serializer_class = CRSerializer

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        try:
            cr = CR.objects.get(email=email, password=password)
            return Response({"message": "Login successful", "cr_id": cr.id}, status=200)
        except CR.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)


# ================= Add Student =================
class StudentCreateView(generics.CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):

        # 1️⃣ Save student in DB → This generates correct token_number
        student = serializer.save()

    # ensure we have the final auto-generated token
        student.refresh_from_db()

        message = (
            f"Hey {student.name}, you are successfully registered for the event! 🎉\n"
            f"Your Token Number is {student.token_number}."
        )

        number = student.number
        # normalize number: remove + if present, ensure country code present (India example)
        if number.startswith('+'):
            number = number[1:]
        if not number.startswith('91'):
            number = f"91{number}"

        # send (sync or background)
        from .utils import send_whatsapp_message
        status, resp = send_whatsapp_message(number, message)
        print("WhatsApp send status:", status, resp)

# ================= Search Student by Token =================
class StudentSearchView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    lookup_field = 'token_number'
    queryset = Student.objects.all()
