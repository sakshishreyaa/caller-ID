import json
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt

from .models import CustomUser,Phonebook,SpamNumbers
from .auth import generate_token,authenticate

@csrf_exempt
def register(req):

    if req.method == 'POST':
        request=json.loads(req.body)
        if not ('phone' in request and 'name' in request and 'password' in request ):
            return JsonResponse({'message':'Bad POST Parameters. Please provide all fields'})
        name = request['name']
        phone = request['phone']
        password= request['password']
        if not (phone and name and password) :
            return JsonResponse({'mesage':' fields cannot be empty value'})
        user = CustomUser.objects.filter(phone=phone).first()
        spam = SpamNumbers.objects.filter(phone=phone).first()
        extra_fields={}
        if spam:
            extra_fields = {'spam' : spam}
        if not user:
            user = CustomUser.objects.create_user(phone=phone,name=name,password=password,**extra_fields)
            Phonebook.objects.create(phone=phone,name=name,user=user)
            return JsonResponse({'mesage':'You have successfully registered!'})
        return JsonResponse({'message':'You have already registered!'})      
    else:
        raise PermissionDenied


def add_phone(request):
    pass

@csrf_exempt
def report_spam(req):
    request=json.loads(req.body)
    if req.method == "POST":
        token = req.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'message':'provide token'})
        if not authenticate(token):
            return JsonResponse({'message':'authetication failed'})
        params={}
        if not 'phone' in request :
            return JsonResponse({'message':'Bad POST Parameters. Please provide phone field'})
        params['phone'] = request['phone']

        if not params['phone']:
            return JsonResponse({'message':' phone field cannot be empty value'})

        spam = SpamNumbers.objects.filter(phone=request['phone']).first()

        if spam:
            spam.reports+=1
            spam.save()
        else:
        
            params['reports']=1
            spam = SpamNumbers.objects.create(**params)

        user  = CustomUser.objects.filter(phone=request['phone']).first()

        if user and not user.spam:
            user.spam = spam
            user.save()
            print(user)
        return JsonResponse({'message':'Spam reported!'})
    else:
        raise PermissionDenied

@csrf_exempt
def search(request):
    
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'message':'provide token'})
        if not authenticate(token):
            return JsonResponse({'message':'authetication failed'})
        if not ('phone' in request.GET or  'name' in request.GET):
            return JsonResponse({'message':'Bad POST Parameters. Please provide either phone or name field'})
        if request.GET.get('phone'):
            p = Phonebook.objects.filter(phone=request.GET['phone']).all()
        if request.GET.get('name'):
            p = Phonebook.objects.filter(name=request.GET['name']).all()
        data=[]
        for num in p:
            spam = SpamNumbers.objects.filter(phone=num.phone).first()

            if spam :
                spam = f'{spam.reports} Spam reports'
            else:
                spam = 'No spam reports'
            data.append({'phone':num.phone,'name':num.name,'spam':spam })
        return JsonResponse({'data':data})
    else:
        raise PermissionDenied


@csrf_exempt
def login(req):
    if req.method == 'POST':
        request=json.loads(req.body)
        if not ('phone' in request and 'password' in request ):
            return JsonResponse({'message':'Bad POST Parameters. Please provide all fields'})
        phone = request['phone']
        password = request['password']
        user = CustomUser.objects.filter(phone=phone).first()
        if user:
            if user.check_password(password):
                token = generate_token(phone)
                return JsonResponse({'mesage':'login success!','token':token})
            else:
               return JsonResponse({'message':'Wrong password'}) 
        return JsonResponse({'message':'Please register before login!'})      
    else:
        raise PermissionDenied