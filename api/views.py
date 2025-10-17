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
        # Save student to DB
        student = serializer.save()

        # Prepare WhatsApp message
        message = (
            f"Hey {student.name}, you are successfully registered for the event! 🎉\n"
            f"Your Token Number is {student.token_number}."
        )

        # Ensure number has country code (India +91 if missing)
        number = student.number
        if not number.startswith("+"):
            number = f"91{number}"  # PyWhatKit requires country code

        # Send WhatsApp asynchronously so request isn't blocked
        def send_message():
            try:
                send_whatsapp_message(number, message)
                print(f"✅ WhatsApp message typed for {student.name} ({number})")
            except Exception as e:
                print(f"❌ Error sending WhatsApp message: {e}")

        threading.Thread(target=send_message).start()


# ================= Search Student by Token =================
class StudentSearchView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    lookup_field = 'token_number'
    queryset = Student.objects.all()
