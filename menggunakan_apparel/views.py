from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

def admin_read_menggunakan_apparel(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_menggunakan_apparel = query("""
    SELECT MA.username_pengguna, MA.nama_tokoh, KJB.nama, A.warna_apparel, A.nama_pekerjaan, A.kategori_apparel
    FROM MENGGUNAKAN_APPAREL MA, KOLEKSI_JUAL_BELI KJB, APPAREL A
    WHERE MA.id_koleksi = KJB.id_koleksi
    AND MA.id_koleksi = A.id_koleksi
    ORDER BY MA.username_pengguna ASC, MA.nama_tokoh ASC;
    """)

    data = get_session_data(request)
    data['list_menggunakan_apparel'] = list_menggunakan_apparel

    return render(request, 'admin_read_menggunakan_apparel.html', data)

def pemain_read_menggunakan_apparel(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")

    username = request.session['username']
    list_menggunakan_apparel = query(f"""
    SELECT MA.nama_tokoh, KJB.nama, A.warna_apparel, A.nama_pekerjaan, A.kategori_apparel, MA.id_koleksi
    FROM MENGGUNAKAN_APPAREL MA, KOLEKSI_JUAL_BELI KJB, APPAREL A
    WHERE MA.id_koleksi = KJB.id_koleksi
    AND MA.id_koleksi = A.id_koleksi
    AND MA.username_pengguna = '{username}'
    ORDER BY MA.nama_tokoh ASC;
    """)

    data = get_session_data(request)
    data['list_menggunakan_apparel'] = list_menggunakan_apparel

    if request.method == 'POST':
        if request.POST.get("DeleteButton") != None:
            request.session['Values'] = request.POST.get('DeleteButton')
            return delete_menggunakan_apparel(request)

    return render(request, 'pemain_read_menggunakan_apparel.html', data)

def create_menggunakan_apparel_view(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")

    if request.POST.get('NamaTokoh') != None:
        if request.POST.get('Apparel') != None:
            return create_menggunakan_apparel(request)

    username = request.session['username']
    tokoh_query = query(f"""
    SELECT nama
    FROM TOKOH
    WHERE username_pengguna = '{username}'
    ORDER BY nama ASC;
    """)
    apparel_query = query(f"""
    SELECT KT.id_koleksi
    FROM KOLEKSI_TOKOH KT, APPAREL A
    WHERE KT.username_pengguna = '{username}' AND KT.id_koleksi = A.id_koleksi
    ORDER BY id_koleksi ASC;
    """)

    data = get_session_data(request)
    data['nama_tokoh'] = tokoh_query
    data['apparel'] = apparel_query

    return render(request, 'create_menggunakan_apparel.html', data)

def create_menggunakan_apparel(request):
    if not is_authenticated(request):
        return login(request)
    
    username = request.session['username']
    nama_tokoh = request.POST.get("NamaTokoh")
    id_koleksi = request.POST.get("Apparel")
    create_menggunakan_apparel_query = query(f"""
    INSERT INTO MENGGUNAKAN_APPAREL
    VALUES('{username}', '{nama_tokoh}', '{id_koleksi}')
    """)

    return redirect('/menggunakan_apparel/pemain_read_menggunakan_apparel/')

def delete_menggunakan_apparel(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")

    values = request.session.get("Values")
    values_list = values.split(", ")

    username_pengguna = values_list[0]
    nama_tokoh = values_list[1]
    id_koleksi = values_list[2]
    delete_menggunakan_apparel_query = query(f"""
        DELETE FROM MENGGUNAKAN_APPAREL
        WHERE username_pengguna = '{username_pengguna}'
        AND nama_tokoh = '{nama_tokoh}'
        AND id_koleksi = '{id_koleksi}'
    """)

    return redirect('/menggunakan_apparel/pemain_read_menggunakan_apparel/')