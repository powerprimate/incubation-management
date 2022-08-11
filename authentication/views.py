from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import user_passes_test,login_required
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from .models import user,Application,slot
from .serializers import AdminSerializer,UserSerializer,ALSerializer
import jwt,datetime,json
key = "secret"
# Create your views here.

# User registration

@api_view(['POST'])
def Registeruserview(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    context={
        'message':'User registration successful',
        'credentials':serializer.data,
    }
    return Response(context)

# Admin registration
@api_view(['POST'])
def Registeradminview(request):
    serializer = AdminSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    context={
        'message':'Admin registration successful',
        'credentials':serializer.data,
    }
    return Response(context)





# User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
   
    content={
        'message':'This is user'
    }
    return Response(content)

# Admin
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin(request):
    content={
        'message':'This is admin'
    }
    return Response(content)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def application_list(request):
    new_application=Application.objects.filter(status='new')
    new_application_list= ALSerializer(new_application, many=True)
    
    pending_application=Application.objects.filter(status='pending')
    pending_application_list= ALSerializer(pending_application, many=True)
    context={
        'new_application_list' : new_application_list.data,
        'pending_application_list' : pending_application_list.data
    }
    return Response(context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def slot_application(request):
    serializer = ALSerializer(data=request.data,context={'request':request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    context={
        'message':'application successful',
        'credentials':serializer.data,
    }
    return Response(context)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_slot(request,slot_no,application_no):
    # application = Application.objects.get(id=application_no)
    
    if slot.objects.filter(application=application_no).exists():
        context = {
            ":-(":'you can only book one slot'
        }
        return Response(context)
    if slot.objects.filter(slot=slot_no).exists():
        context = {
            ":-(":"this slot is already booked"
        }
        return Response(context)
    else:
        application = Application.objects.get(id=application_no)
        slot.objects.create(
            user = request.user,
            application = application,
            slot = slot_no,
         )
        context={
            ";-)":"slot booked",
            "slot_number":slot_no
        }
        return Response(context)
    
    


# login
@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    
    subject = user.objects.get(email=email)
    
    if subject is None:
        raise AuthenticationFailed('User not Found!')
    
    p = check_password(password,subject.password)
    if p is False:
        raise AuthenticationFailed('Incorrect password!')
    
     
    payload = {
        'id': subject.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'int': datetime.datetime.utcnow(),
    }
    
    token = jwt.encode(payload, key, algorithm="HS256")
    
    response = Response()
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data=({
        'jwt':token
    })
    return response

# User
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, key, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed
    
    subject = user.objects.get(payload['id'])
    serializer= UserSerializer(subject)
    content={
        'message':'This is user'
    }
    return Response(serializer.data,content)


# Admin
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def admin(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, key, algorithms="HS256")
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed
    
    subject = user.objects.get(payload['id'])
    serializer= UserSerializer(subject)
    content={
        'message':'This is admin'
    }
    return Response(serializer.data,content)
