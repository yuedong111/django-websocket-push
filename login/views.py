from django.shortcuts import render, redirect, HttpResponse, render_to_response
from .models import User, PhoneCheck
from .forms import RegisterForm, CheckPhoneForm, PasswdReform
import requests
import random
from functools import reduce
from urllib.parse import urlencode
from zhanghujiaoyi.settings import APPKEY, TPL_ID


# Create your views here.


def check_login(func):
    def wrapper(request, *args, **kwargs):
        if request.session.get("is_login", None):
            return func(request, *args, **kwargs)
        else:
            return redirect("/login")

    return wrapper


def find_file(request, file_name):
    return render(request, file_name)


def index(request):
    return render(request, "index.html")


def login(request):
    if request.session.get("is_login", None):
        return redirect("/index")
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        message = "请填写所有字段"
        if phone and password:
            try:
                user = User.objects.get(phone_number=phone)
                if user.password == password:
                    request.session["is_login"] = True
                    request.session["user_id"] = user.id
                    request.session["user_name"] = user.name
                    response = render_to_response("index.html")
                    response.set_cookie("expire","898987")
                    # response.set_cookie("path","/")
                    return response
                    # return redirect('/index/')
                else:
                    message = "密码不正确"
            except:
                message = "用户名不存在"
            return render(request, "login/login.html", {"message": message})
    return render(request, 'login/login.html')


def logout(request):
    if not request.session.get("is_login", None):
        return redirect("/index/")
    request.session.flush()
    return redirect("/index/")


def send_check_code(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "GET":
        return render(request, "login/checkcode.html")
    url = "http://v.juhe.cn/sms/send"
    temp = [random.randint(0, 9) for _ in range(6)]
    num = reduce(lambda x, y: str(x) + str(y), temp)
    tpl_value = "#code#={}".format(num)
    params = {
        "mobile": "17783886899",
        "tpl_id": TPL_ID,
        "tpl_value": tpl_value,
        "key": APPKEY,
        "dtype": "json",

    }
    params1 = urlencode(params)
    # if True:
    r = requests.get("{}?{}".format(url, params1))
    # else:
    #     r = requests.post(url, data=params)
    res = r.json()
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            message = "验证码已发送"
            if request.method == "POST":
                cf = CheckPhoneForm(request.POST)
                if cf.is_valid():
                    phone = cf.cleaned_data["phone"]
                    ph = PhoneCheck.objects.filter(phone_number=phone)
                    if ph:
                        # 为了访问id
                        # PhoneCheck.objects.update(check_number=num, id=ph.id)
                        ph.update(check_number=num)
                    else:
                        checnum = PhoneCheck.objects.create()
                        checnum.phone_number = phone
                        checnum.check_number = num
                        checnum.save()
                    return render(request, "login/register.html")
            else:
                return render(request, "login/checkcode.html")
        else:
            message = "验证码发送出错"
    else:
        message = "验证码发送请求地址出错"
    return render(request, "login/checkcode.html", locals())


def register(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "POST":
        re_form = RegisterForm(request.POST)
        message = "需要填写完整"
        if re_form.is_valid():
            username = re_form.cleaned_data["username"]
            password1 = re_form.cleaned_data['password1']
            password2 = re_form.cleaned_data['password2']
            phone = re_form.cleaned_data['phone']
            sex = re_form.cleaned_data['sex']
            check_num = re_form.cleaned_data["check_code"]
            if password1 != password2:
                message = "两次输入密码不一致"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(phone_number=phone)
                if same_email_user:
                    message = '该手机号已被注册，请使用别的手机号！'
                    return render(request, 'login/register.html', locals())
                phone_check = PhoneCheck.objects.filter(check_number=check_num, phone_number=phone)
                if not phone_check:
                    return render(request, "login/register.html", {"message": "验证码不一致"})
                new_user = User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.phone_number = phone
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')
    re_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def passwd_forget(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "GET":
        return render(request, "login/forget_passwd.html")
    url = "http://v.juhe.cn/sms/send"
    temp = [random.randint(0, 9) for _ in range(6)]
    num = reduce(lambda x, y: str(x) + str(y), temp)
    tpl_value = "#code#={}".format(num)
    params = {
        "mobile": "17783886899",
        "tpl_id": TPL_ID,
        "tpl_value": tpl_value,
        "key": APPKEY,
        "dtype": "json",

    }
    params1 = urlencode(params)
    # if True:
    r = requests.get("{}?{}".format(url, params1))
    # else:
    #     r = requests.post(url, data=params)
    res = r.json()
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            message = "验证码已发送"
            if request.method == "POST":
                cf = CheckPhoneForm(request.POST)
                if cf.is_valid():
                    phone = cf.cleaned_data["phone"]
                    ph = PhoneCheck.objects.filter(phone_number=phone)
                    if ph:
                        # 为了访问id
                        # PhoneCheck.objects.update(check_number=num, id=ph.id)
                        ph.update(check_number=num)
                        return render(request, "login/passwd_reform.html")
                    else:
                        message = "该号码没有注册过"
                        return render(request, "login/forget_passwd.html", locals())
            else:
                return render(request, "login/forget_passwd.html")
        else:
            message = "验证码发送出错"
    else:
        message = "验证码发送请求地址出错"
    return render(request, "login/forget_passwd.html", locals())


def reform_passwd(request):
    if request.session.get("is_login", None):
        return redirect("/index/")
    if request.method == "POST":
        pswd = PasswdReform(request.POST)
        message = "填写错误"
        if pswd.is_valid():
            phone = pswd.cleaned_data["phone"]
            pss1 = pswd.cleaned_data["password1"]
            pss2 = pswd.cleaned_data["password2"]
            check_code = pswd.cleaned_data["check_code"]
            ph = PhoneCheck.objects.get(phone_number=phone)
            if ph and ph.check_number == check_code:
                if pss2 != pss1:
                    message = "两次输入密码不一致"
                    return render(request, 'login/passwd_reform.html', locals())
                else:
                    same_user = User.objects.filter(phone_number=phone)
                    if not same_user:
                        message = "该手机号未注册"
                        return render(request, 'login/passwd_reform.html', locals())
                    else:
                        same_user.update(password=pss1)
                        return render(request, "login/login.html")
            else:
                message = "验证码错误"
                return render(request, "login/passwd_reform.html", locals())
    return render(request, "login/passwd_reform.html")
