from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import UserModel
from .tokens import email_token_generator
from .utils import send_verification_email
from django.http import JsonResponse,HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
import datetime
from datetime import timedelta
import jwt


# User Registration View
class RegisterView(APIView):
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        print(f"Received registration request: {request.data}")

        if not name or not email or not password:
            return JsonResponse({'message': 'All fields are required', 'status': 400})


        if UserModel.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists', 'status': 400})

    
        user = UserModel.objects.create(
            name=name,
            email=email,
            password=make_password(password),
            is_active=False  ,
            is_admin=False,
        )

        print(f"User created: {user}")
        token = email_token_generator.make_token(user)
        print(f"Generated token: {token}")
        verification_url = send_verification_email(user, request, token)

        return JsonResponse({
            'message': 'User registered successfully. Please check your email to verify your account.',
            'status': 200
        })


# Email Verification View
class VerifyEmailView(APIView):
    def get(self, request):
        print(f"Received email verification request: {request.query_params}")
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')

        try:
            user = UserModel.objects.get(id=uid)

            if email_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return HttpResponse(
                    '<h1>Email verified successfully!</h1><p>You can now log in.</p>'
                )
            else:
                return JsonResponse({'message': 'Invalid or expired token', 'status': 400})

        except UserModel.DoesNotExist:
            return JsonResponse({'message': 'User not found', 'status': 404})


# User Login View
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = UserModel.objects.get(email=email)

            # Check if the user is active (email verified)
            if not user.is_active:
                return JsonResponse({'message': 'Email not verified', 'status':403})

            # Verify the password
            if check_password(password, user.password):
                payload = {
                    'id': user.id,
                    'email': user.email,
                    'exp': datetime.datetime.now() + timedelta(days=1),
                    'iat': datetime.datetime.now(),
                }
                token = jwt.encode(payload, 'bcg_online_assessment', algorithm='HS256')

                #update last login time
                user.last_login = datetime.datetime.now()
                user.save()


                
                
                return JsonResponse({
                    'message': 'Login successful',
                    'token': token,
                    'exp': datetime.datetime.now() + timedelta(days=1),
                    'user': {
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'permissions': user.permissions,
                        'is_admin': user.is_admin,
                    },
                   
                 'status':200})

            else:
                return JsonResponse({'message': 'Invalid credentials', 'status':401})

        except UserModel.DoesNotExist:
            return JsonResponse({'message': 'User not found', 'status': 404})
        


class AddPermissions(APIView):
    def post(self, request):
        email = request.data.get('email')
        permissions = request.data.get('permissions')

        try:
            user = UserModel.objects.get(email=email)
            permissions = user.permissions
            new_permissions = request.data.get('permissions')
            permissions.extend(new_permissions)
            user.permissions = permissions
            user.save()
            return JsonResponse({'message': 'Permissions added successfully', 'status': 200})
        except UserModel.DoesNotExist:
            return JsonResponse({'message': 'User not found', 'status': 404})

