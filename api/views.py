from rest_framework.decorators import api_view
from django.http import JsonResponse
from .models import User, Password, TwoFactorCode
from .utils import generate_unique_string, hash_password


@api_view(['POST'])
def register(request):
    missing_fields = []
    if 'username' not in request.data:
        missing_fields.append('username')
    if 'password' not in request.data:
        missing_fields.append('password')
    if len(missing_fields):
        return JsonResponse({
            'success': False,
            'message': 'Some required fields were missing.',
            'missing_fields': missing_fields
        })
    if len(request.data['username']) < 2:
        return JsonResponse({'success': False, 'message': 'Username too short.'})
    if len(request.data['password']) < 5:
        return JsonResponse({'success': False, 'message': 'Password too short.'})
    if User.objects.all().filter(username=request.data['username']).count() != 0:
        return JsonResponse({'success': False, 'message': 'Username already taken.'})
    salt = generate_unique_string(8)
    hashed_password = hash_password(request.data['password'], salt)
    user = User(
        username=request.data['username'],
        password_salt=salt,
        password_hash=hashed_password,
    )
    user.save()
    return JsonResponse({'success': True})


@api_view(['POST'])
def get_password(request):
    missing_fields = []
    if 'username' not in request.data:
        missing_fields.append('username')
    if 'password' not in request.data:
        missing_fields.append('password')
    if 'service' not in request.data:
        missing_fields.append('service')
    if 'login_username' not in request.data:
        missing_fields.append('login_username')
    if len(missing_fields):
        return JsonResponse({
            'success': False,
            'message': 'Some required fields were missing.',
            'missing_fields': missing_fields
        })
    if User.objects.all().filter(username=request.data['username']).count() == 0:
        return JsonResponse({'success': False, 'message': 'Invalid username.'})
    user = User.objects.get(username=request.data['username'])
    salt = user.password_salt
    if hash_password(request.data['password'], salt) != user.password_hash:
        return JsonResponse({'success': False, 'message': 'Incorrect password.'})
    try:
        password = Password.objects.get(
            user_id=user,
            service=request.data['service'],
            login=request.data["login_username"],
        )
    except Password.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Password not found",
        })
    return JsonResponse({
        'success': True,
        'password': password.password,
    })


@api_view(['POST'])
def add_password(request):
    missing_fields = []
    if 'username' not in request.data:
        missing_fields.append('username')
    if 'password' not in request.data:
        missing_fields.append('password')
    if 'service' not in request.data:
        missing_fields.append('service')
    if 'login_username' not in request.data:
        missing_fields.append('login_username')
    if 'login_password' not in request.data:
        missing_fields.append('password')
    if len(missing_fields):
        return JsonResponse({
            'success': False,
            'message': 'Some required fields were missing.',
            'missing_fields': missing_fields
        })
    if User.objects.all().filter(username=request.data['username']).count() == 0:
        return JsonResponse({'success': False, 'message': 'Invalid username.'})
    user = User.objects.get(username=request.data['username'])
    salt = user.password_salt
    if hash_password(request.data['password'], salt) != user.password_hash:
        return JsonResponse({'success': False, 'message': 'Incorrect password.'})
    try:
        Password.objects.get(
            user_id=user,
            service=request.data["service"],
            login=request.data["login_username"]
        )
        return JsonResponse({
            "success": False,
            "message": "Service/login combo already exists",
        })
    except Password.DoesNotExist:
        Password(
            user_id=user,
            service=request.data["service"],
            login=request.data["login_username"],
            password=request.data["login_password"]
        ).save()
    return JsonResponse({'success': True})


@api_view(['POST'])
def get_two_factor_code(request):
    missing_fields = []
    if 'username' not in request.data:
        missing_fields.append('username')
    if 'password' not in request.data:
        missing_fields.append('password')
    if 'service' not in request.data:
        missing_fields.append('service')
    if 'login_username' not in request.data:
        missing_fields.append('login_username')
    if len(missing_fields):
        return JsonResponse({
            'success': False,
            'message': 'Some required fields were missing.',
            'missing_fields': missing_fields
        })
    if User.objects.all().filter(username=request.data['username']).count() == 0:
        return JsonResponse({'success': False, 'message': 'Invalid username.'})
    user = User.objects.get(username=request.data['username'])
    salt = user.password_salt
    if hash_password(request.data['password'], salt) != user.password_hash:
        return JsonResponse({'success': False, 'message': 'Incorrect password.'})
    codes = TwoFactorCode.objects.filter(
        user_id=user,
        service=request.data["service"],
        login=request.data["login_username"],
    )
    remaining = codes.count()
    if remaining <= 1:
        return JsonResponse({
            "success": False,
            "message": "Not enough codes available",
            "remaining": remaining,
        })
    code = codes[0].code
    codes[0].delete()
    remaining -= 1
    return JsonResponse({
        'success': True,
        "code": code,
        "remaining": remaining,
    })


@api_view(['POST'])
def set_two_factor_codes(request, **kwargs):
    missing_fields = []
    if 'username' not in request.data:
        missing_fields.append('username')
    if 'password' not in request.data:
        missing_fields.append('password')
    if 'service' not in request.data:
        missing_fields.append('service')
    if 'login_username' not in request.data:
        missing_fields.append('login_username')
    if 'codes' not in request.data:
        missing_fields.append('codes')
    if len(missing_fields):
        return JsonResponse({
            'success': False,
            'message': 'Some required fields were missing.',
            'missing_fields': missing_fields
        })
    if User.objects.all().filter(username=request.data['username']).count() == 0:
        return JsonResponse({'success': False, 'message': 'Invalid username.'})
    user = User.objects.get(username=request.data['username'])
    salt = user.password_salt
    if hash_password(request.data['password'], salt) != user.password_hash:
        return JsonResponse({'success': False, 'message': 'Incorrect password.'})
    TwoFactorCode.objects.filter(
        user_id=user,
        service=request.data["service"],
        login=request.data["login_username"],
    ).delete()
    for code in request.data["codes"]:
        TwoFactorCode(
            user_id=user,
            code=code,
            login=request.data["login_username"],
            service=request.data["service"],
        ).save()
    return JsonResponse({
        'success': True,
    })
