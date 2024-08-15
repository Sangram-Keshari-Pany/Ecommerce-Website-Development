from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# email message and link encode and token generation
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from authenticationapp.utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str
# sending email
from django.core.mail import EmailMessage
from django.conf import settings
# password reset
from django.utils.encoding import DjangoUnicodeDecodeError
# views
from django.views.generic import View
# authentication and login
from django.contrib.auth import authenticate,login,logout
# 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# Create your views here.
def handlesignup(request):
    if request.method=="POST":
        email=request.POST['email']
        passsword=request.POST['pass1']
        confirm_passsword=request.POST['pass2']
        if passsword!=confirm_passsword:
            messages.get_messages(request).used = True
            messages.warning(request,"Password Is Not Matching")
            return render(request,"authentication/signup.html")
        try:
            if User.objects.get(username=email):
               messages.get_messages(request).used = True
               messages.info(request,"Email Is Already Taken")
               return render (request,"authentication/signup.html")
        except Exception as identifier:
            pass
        user=User.objects.create_user(email,email,passsword)
        print(passsword)
        user.is_active=False
        email_subject='Active Your Account'
        message=render_to_string('authentication/activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        print (message)
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()
        user.save()
        messages.get_messages(request).used = True
        messages.success(request,'Activate your account check your email')
        return redirect('handlelogin')
    return render(request,"authentication/signup.html")

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user!=None and generate_token.check_token(user,token):
            user.is_active=True
            print("hiii")
            user.save()

            messages.get_messages(request).used = True
            messages.success(request,'Account Activated Sucessfully')
            return redirect('handlelogin')
        print(user)
        return render (request,'authentication/activatefail.html')
            
def handlelogin(request):
    if request.method=='POST':
        username=request.POST['email']
        userpasssword=request.POST['pass1']
        print(username,userpasssword)
        myuser=authenticate(username=username,password=userpasssword)
        print(myuser)
        if myuser is not None:
            login(request,myuser)
            messages.get_messages(request).used = True
            messages.success(request,'Login Success')
            return redirect("/")
        else:
            messages.get_messages(request).used = True
            messages.error(request,'Invalid Credentials')
            return redirect("/authentication/login")
    return render(request,"authentication/login.html")

def handlelogout(request):
    logout(request)
    messages.get_messages(request).used = True
    messages.info(request,"LogOut Success")
    return redirect('/authentication/login')

class RequestResetEmailView(View):
    def get(self,request):
        return render (request,'authentication/reset.html')
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)
        if user.exists():
            email_subject='[Reset Your Password]'
            message=render_to_string('authentication/reactivate.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()
            return render(request,'authentication/reset.html')
        

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context= {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"password link is invalid")
                return render (request,"authentication/reset.html",context)
        except DjangoUnicodeDecodeError as e:
            ...
        return render(request,"authentication/setnew.html",context)
    
    def post(self,request,uidb64,token):
        context= {
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_passwprd=request.POST['pass2']

        if password!=confirm_passwprd:
            return render(request,"authentication/setnew.html",context)
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect("/authentication/login")

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,"authentication/setnew.html",context)
        
        return render(request,"authentication/setnew.html",context)




