from django.shortcuts import redirect, render, HttpResponse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from home.views import get_session_data, is_authenticated, login
from datetime import datetime

# Create your views here.
def admin_read_makan(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_makan = query("SELECT * FROM MAKAN")

    data = get_session_data(request)
    data['list_makan'] = list_makan

    return render(request,'admin_read_makan.html', data)

def pemain_read_makan(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    username = request.session['username']
    list_makan = query(f"SELECT nama_tokoh, waktu, nama_makanan FROM MAKAN WHERE username_pengguna = '{username}'")
    data = get_session_data(request)
    data['list_makan'] = list_makan

    return render(request,'pemain_read_makan.html', data)

@csrf_exempt
def pemain_buat_makan(request):
    if is_authenticated(request):
        username = request.session['username']

        if request.POST.get('NamaTokoh') != None:
            return buat_makan(request)

        tokoh_query = query(f"""
        SELECT nama FROM tokoh where username_pengguna = '{username}'
        """)

        makan_query = query(f"""
        SELECT nama
        FROM MAKANAN
        """)

        data = get_session_data(request)
        data['tokoh'] = tokoh_query
        data['makanan'] = makan_query

        return render(request, "pemain_buat_makan.html", data)
    else:
        return login(request)

def buat_makan(request):
    if not is_authenticated:
        return login(request)
    else:
        username = request.session.get('username')
        nama_tokoh = request.POST.get('NamaTokoh')
        time = datetime.now()
        now = time.strftime("%d/%m/%Y %H:%M:%S")
        nama_makanan = request.POST.get('NamaMakanan')

        print(username)
        print(nama_tokoh)
        print(now)
        print(nama_makanan)

        query(f"""
        INSERT INTO makan
        VALUES('{username}', '{nama_tokoh}', '{time}', '{nama_makanan}')
        """)

        return redirect('/makan/pemain_read_makan/')
