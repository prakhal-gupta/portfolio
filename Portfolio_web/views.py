import json
from django.http  import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
import re,os
from django.core.mail import send_mail
from datetime import datetime

def User_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_condition  = "[a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,3}$"
        match   = re.search(email_condition,data['email_c'])
        if (not match):
            mes = { 'error': 'Invalid Email !'}
            return JsonResponse(mes,status=403,safe=False)

        else:
            new_room=Customer_Message(**data)
            new_room.save()
            x = datetime.now()
            y = str(x)
            send_mail(
                'Portfolio Message',
                'Hi Prakhal'
                '\n\nI ' +data['name_c']+ ' just saw your portfolio and wants to get in touch with you.Attaching detail for the same...'
                '\n\nMobile Number : '+data['mobile_c'] + 
                '\nEmail : '+data['email_c'] + 
                '\nSubject : '+data['subject_c'] + 
                '\nMessage : '+data['message_c'] +
                '\nTimeStamp : ' + y ,
                'prakhaldjangotest@gmail.com',
                ['Prakhal.2125it1045@kiet.edu'],
                fail_silently=False,
            )
            mes = {'message': 'Message sent Successfully!!'}
            return JsonResponse(mes,status=200,safe=False)


def Admin_registration(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email_condition  = "[a-zA-Z0-9\-\_\.]+@[a-zA-Z0-9]{2,}\.[a-zA-Z0-9]{2,3}$"
        match   = re.search(email_condition,data['email'])
        if (not match):
            mes = { 'error': 'Invalid Email !'}
            return JsonResponse(mes,status=403,safe=False)

        if (User.objects.filter(email = data['email'])):
            mes = {'error': 'Email Already Exists!!'}
            return JsonResponse(mes,status=403,safe=False)
        else:
            new_user=User.objects.create_user(**data)
            new_user.save()
            mes = {'message': 'Admin Registered Successfully!!'}
            return JsonResponse(mes,status=200,safe=False)    


def Admin_login(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        Username_l = data['username']
        Password_l = data['password']
        if (not Username_l):
            mes = {  'message': 'Username Required!!'}
            return JsonResponse(mes,status=403,safe=False)

        if (not Password_l):
            mes = { 'message': 'Password Required !'}
            return JsonResponse(mes,status=403,safe=False)

        if(User.objects.filter(username=Username_l).exists()):         
            user = authenticate(request,username=Username_l, password=Password_l)
            Email_l = User.objects.get(username=Username_l).email
            if user is not None: 
                login(request, user)
                send_mail(
                    'Portfolio Database Login Alert',
                        'Hi ' + Username_l +
                        '\n\nYou just loggedin into your Portfolio Database account.'
                        '\n\nRegards,'
                        '\nPrakhal Portfolio Module' ,
                    'prakhaldjangotest@gmail.com',
                    [Email_l],
                    fail_silently=False,
                )
                mes = {  'message' :'Login Successful !'}
                return JsonResponse(mes,status=200,safe=False)
            else:
                mes ={  'message':'Wrong Credentials !'}
                return JsonResponse(mes,status=403,safe=False)
        else:
                mes ={  'message':'Invalid User !'}
                return JsonResponse(mes,status=403,safe=False)
            

def Admin_dash(request):
    if request.method == 'GET':
        if request.user.is_authenticated:

            USer = User.objects.filter(username=request.user)
            Admin_d = list(USer.values('first_name','last_name','username','email'))[0]
            Message     = Customer_Message.objects.all()
            Message_d   = list(Message.values('id','name_c','mobile_c','email_c','subject_c','message_c','response_a','Timestamp'))
            mes = { 
                "Admin" : Admin_d,
                "Content" : Message_d
                }
 
            return JsonResponse(mes,status=200,safe=False)
        else:
            mes = { "error"   :"Unauthorised Access !"}
            return JsonResponse(mes,status=401,safe=False) 


def Response_key(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
                data = json.loads(request.body)
                Id_d          = data['id']
                Response = Customer_Message.objects.get(id=Id_d).response_a

                mes = { 'message' : Response} 
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!!"}
            return JsonResponse(mes,status=401,safe=False) 

def Response_Update(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
                data = json.loads(request.body)
                ID_d       = data['id']
                response_u     = data['response_ad']
                if (not response_u):
                    mes = {  'message': 'Response Required!!'}
                    return JsonResponse(mes,status=403,safe=False)

                Customer = Customer_Message.objects.get(id=ID_d)
                Customer.response_a = response_u
                Customer.save(update_fields=['response_a'])
                Email_l = Customer.email_c
                Name_l  = Customer.name_c
                send_mail(
                            "Prakhal's Portfolio Response",
                            'Hi '+ Name_l+
                            '\nHere is an update from Prakhal Gupta on your request.'
                            '\n\n' + response_u +
                            '\n\nRegards,'
                            '\nPrakhal Gupta',
                            'prakhaldjangotest@gmail.com',
                            [Email_l],
                            fail_silently=False,
                        )
                mes = { 'message' : "Response Updated !"} 
                return JsonResponse(mes,status=200,safe=False)

        else:
            mes = {  "error"   :"Unauthorised Access!"}
            return JsonResponse(mes,status=401,safe=False) 


def Logout(request):
    
    if request.user.is_authenticated:
        logout(request)
        mes = { 'message' :"Logout Sucessfull!"}
        return JsonResponse(mes,status=200,safe=False)

    else:
        mes = {  "error":"Unauthorised Access!"}
        return JsonResponse(mes,status=401,safe=False)

