from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.query import query


# Create your views here.
def is_authenticated(request):
    try:
        request.session["username"]
        return True
    except KeyError:
        return False

def get_session_data(request):
    if not is_authenticated(request):
        return {}

    try:
        return {"username": request.session["username"], "role": request.session["role"]}
    except:
        return {}

def get_role(username, password):
    admin_query = query(
        f"SELECT username FROM ADMIN WHERE username = '{username}' AND password = '{password}'"
    )
    print(type(admin_query))
    if type(admin_query) == list and len(admin_query):
        return "admin"

    pemain_query = query(
        f"SELECT username FROM PEMAIN WHERE username = '{username}' AND password = '{password}'"
    )
    if type(pemain_query) == list and len(pemain_query):
        return "pemain"

    return ""

def landing_page(request):
    return render(request, "landing_page.html")

@csrf_exempt
def login(request):
    next = request.GET.get("next")
    print("memulai login")
    print(next)

    if request.method != "POST":
        print("bukan method POST")
        return login_view(request)
    
    if is_authenticated(request):
        print("terotentikasi")
        username = str(request.session["username"])
        password = str(request.session["password"])
        print(username)
        print(password)
    else:
        print("tidak terotentikasi")
        username = str(request.POST["username"])
        password = str(request.POST["password"])
        print(username)
        print(password)

    role = get_role(username, password)
    print(role)

    if role == "":
        return login_view(request)
    else:
        request.session["username"] = username
        request.session["password"] = password
        request.session["role"] = role
        request.session.set_expiry(0)
        request.session.modified = True

        if next != None and next != "None":
            return redirect(next)
        else:
            if role == "admin":
                return redirect("/admin_homepage/")
            else:
                return redirect("/pemain_homepage/")

def login_view(request):
    if is_authenticated(request):
        if str(request.session["role"]) == "admin":
            return redirect("/admin_homepage/")
        else:
            return redirect("/pemain_homepage/")

    return render(request, "login.html")

def logout(request):
    next = request.GET.get("next")

    if not is_authenticated(request):
        return redirect("/")

    request.session.flush()
    request.session.clear_expired()

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/")

def register_view(request):
    return render(request, 'register.html')

@csrf_exempt
def register(request):
    if is_authenticated(request):
        print("terotentikasi")
        if str(request.session["role"]) == "admin":
            return redirect('/admin_homepage/')
        else:
            return redirect("/pemain_homepage/")

    if request.method != "POST":
        print("bukan method post")
        return register_view(request)

    role1 = str(request.POST["role1"])
    print(role1)

    if role1 == "admin":
        return register_admin(request)
    else:
        return register_pemain(request)

@csrf_exempt
def register_admin(request):
    next = request.GET.get("next")
    body = request.POST
    print("start querying")

    username = body.get("usernameForAdmin")
    password = body.get("passwordForAdmin")

    find_akun_query = query(
        f"SELECT username FROM AKUN WHERE username = '{username}'"
    )
    if type(find_akun_query) == list:
        if len(find_akun_query) == 0:
            akun_query = query(
                f"""
                INSERT INTO akun VALUES
                ('{username}')
                """
            )
            print(akun_query)  
    result = query(
        f"""
        INSERT INTO admin VALUES
        ('{username}' , '{password}')
        """
    )

    if result < 1:
        return HttpResponse("Anda gagal melakukan registrasi!")

    request.session["username"] = username
    request.session["password"] = password
    request.session["role"] = "admin"
    request.session.set_expiry(0)
    request.session.modified = True

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/admin_homepage/")

@csrf_exempt
def register_pemain(request):
    next = request.GET.get("next")
    body = request.POST

    username = body["usernameForPemain"]
    email = body["emailForPemain"]
    password = body["passwordForPemain"]
    no_hp = body["noHpForPemain"]

    find_akun_query = query(
        f"SELECT username FROM AKUN WHERE username = '{username}'"
    )

    if type(find_akun_query) == list:
        if len(find_akun_query) == 0:
            akun_query = query(
                f"""
                INSERT INTO akun VALUES
                ('{username}')
                """
            )

    result = query(
        f"""
        INSERT INTO pemain VALUES
        ('{username}', '{email}' ,'{password}', {no_hp})
        """
    )

    print("PEMAIN:", result)

    request.session["username"] = username
    request.session["password"] = password
    request.session["role"] = "pemain"
    request.session.set_expiry(0)
    request.session.modified = True

    if next != None and next != "None":
        return redirect(next)
    else:
        return redirect("/pemain_homepage/")

def admin_homepage(request):
    if is_authenticated(request):
        print("terotentikasi")
        if request.session['role'] != 'admin':
            return HttpResponse("Role anda bukanlah admin")
        return render(request, "admin_homepage.html", get_session_data(request))
    else:
        print("tidak terotentikasi")
        return login(request)

def pemain_homepage(request):
    if is_authenticated(request):
        print("terotentikasi")
        if request.session['role'] != 'pemain':
            return HttpResponse("Role anda bukan pemain")
        username = request.session['username']
        data_query = query(f"SELECT * FROM pemain WHERE username = '{username}'")
        data = get_session_data(request)
        data["list"] = data_query


        return render(request, "pemain_homepage.html", data)
    else:
        print("tidak terotentikasi")
        return login(request)