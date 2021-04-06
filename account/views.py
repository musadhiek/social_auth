from django.shortcuts import render,redirect
from django.contrib import auth,messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import requests, json


# Create your views here.
def log_out(request):
    auth.logout(request)
    return redirect(login)

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return render(request,'user_page.html')
        else:
            messages.error(request, 'Incorrect username or password')
            return render(request,'login.html')   
    else:
        return render(request,'login.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        mobile = request.POST['mobile']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']
    
        # if password == confirm_password:
        user = User.objects.create_user(
            username=username,last_name=mobile, email=email, password=password, is_staff=False, is_superuser=False)
        user.save()
        auth.login(request, user)
        return render(request,'user_page.html')
        # else:
        #     return render(request, 'login.html', {'warning': 'passwords do not match'})
        
    return render(request, 'sign_up.html')
def user_page(request):
    return render(request, 'user_page.html')

def enter_otp(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        otp_id = request.session['otp_id']
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': otp_id,
                   'otp_code': otp}
        files = [
        ]
        headers = {
            'Authorization': 'Token 8df27b0ad9bd2c2e8112f5dad4db5b4d55115e95'
        }
        response = requests.request(
            "POST", url, headers=headers, data=payload, files=files)
        print(response.text.encode('utf8'))
        data = response.text.encode('utf8')
        dict = json.loads(data.decode('utf8'))
        status = dict['status']
        if status == 'success':
            print('youre login is success')

            auth.login(request, user)
            return render(request,'user_page.html')
        else:
            print("your login failed")
            return redirect(login)
    else:
        return render(request, 'enter_otp.html')


def send_otp(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        if User.objects.filter(last_name=mobile).exists():
            user = User.objects.get(last_name=mobile)
        
            mobile = str(91)+mobile
            
            url = "https://d7networks.com/api/verifier/send"
            payload = {'mobile': mobile,
                        'sender_id': 'SMSINFO',
                        'message': 'Your otp code is {code}',
                        'expiry': '9000'}
            files = [
            ]
            headers = {
                'Authorization': 'Token 8df27b0ad9bd2c2e8112f5dad4db5b4d55115e95'
            }
            response = requests.request(
                "POST", url, headers=headers, data=payload, files=files)
            print(response.text.encode('utf8'))
            data = response.text.encode('utf8')
            dict = json.loads(data.decode('utf8'))
            otp_id = dict['otp_id']
            request.session['otp_id'] = otp_id
            request.session['user_id'] = user.id
            return redirect(enter_otp)
        else:
            messages.error(request, 'This number is not registered')
            return redirect(login)
    else:
        return redirect(login)

def user_page(request):
    if not request.user.is_authenticated:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            login(request,user)
            return render(request,'user_page.html')
        else:
            user = User.objects.create_user(username=username)   
        return render(request,'user_page.html')
    else:
        return render(request,'user_page.html') 

def admin_login(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request,'dashboard.html')
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            return render(request,'dashboard.html')
        else:
            messages.error(request, "You're not allowed to access this")
            return render(request,'admin_login.html') 
    else:
        return render(request,'admin_login.html')   

def list_user(request):
    if request.user.is_authenticated and request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)
        return render(request, 'list_user.html', {'users': users})
    else:
        return redirect(admin_login)   

def delete_user(request, id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect(list_user)

def block_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = False
        user.save()
        return redirect(list_user)
    else:
        return redirect(admin_login)

def unblock_user(request, id):
    if request.user.is_authenticated and request.user.is_superuser:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        return redirect(list_user)
    else:
        return redirect(admin_login)