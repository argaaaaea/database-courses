from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def admin_read_barang(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_menggunakan_barang = query("""
    SELECT * 
    FROM menggunakan_barang, koleksi_jual_beli
    WHERE menggunakan_barang.id_barang = koleksi_jual_beli.id_koleksi
    """)

    data = get_session_data(request)
    data['list_menggunakan_barang'] = list_menggunakan_barang

    return render(request, 'admin_read_barang.html', data)

def pemain_read_barang(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")

    username = request.session['username']
    list_menggunakan_barang = query(f"""
    SELECT nama_tokoh, nama, waktu
    FROM menggunakan_barang, koleksi_jual_beli 
    WHERE username_pengguna = '{username}' AND menggunakan_barang.id_barang = koleksi_jual_beli.id_koleksi
    """)

    data = get_session_data(request)
    data['list_menggunakan_barang'] = list_menggunakan_barang

    return render(request, 'pemain_read_barang.html', data)

@csrf_exempt
def pemain_menggunakan_barang(request):
    if is_authenticated(request):
        username = request.session['username']

        if request.POST.get('Nama') != None:
            return menggunakan_barang(request)

        tokoh_query = query(f"""
        SELECT nama FROM tokoh where username_pengguna = '{username}'
        """)

        barang_query = query(f"""
        SELECT id_koleksi
        FROM koleksi_tokoh
        WHERE username_pengguna = '{username}'
        """)

        print(barang_query)

        data = get_session_data(request)
        data['tokoh'] = tokoh_query
        data['barang'] = barang_query

        return render(request, "menggunakan_barang.html", data)
    else:
        return login(request)

def menggunakan_barang(request):
    if not is_authenticated:
        return login(request)
    else:
        username = request.session.get('username')
        nama_real = request.POST.get("Nama")
        nama_query = query(f"""
        SELECT nama FROM tokoh WHERE username_pengguna = '{username}' AND nama LIKE '%{nama_real}%'
        """)
        nama = nama_query[0][0]
        time = datetime.now()
        now = time.strftime("%d/%m/%Y %H:%M:%S")
        barang = request.POST.get('Barang')
        print(now)

        menggunakan_barang_query = query(f"""
        INSERT INTO menggunakan_barang
        VALUES('{username}', '{nama}', '{time}', '{barang}')
        """)

        return redirect('/barang/pemain_read_barang')