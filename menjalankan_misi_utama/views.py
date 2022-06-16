from django.shortcuts import redirect, render, HttpResponse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from home.views import get_session_data, is_authenticated, login

# Create your views here.
def admin_read_menjalankan_misi_utama(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_menjalankan_misi_utama = query("SELECT * FROM MENJALANKAN_MISI_UTAMA")

    data = get_session_data(request)
    data['list_menjalankan_misi_utama'] = list_menjalankan_misi_utama

    return render(request,'admin_read_menjalankan_misi_utama.html', data)

def pemain_read_menjalankan_misi_utama(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    username = request.session['username']
    list_menjalankan_misi_utama = query(f"""SELECT nama_tokoh, nama_misi, status 
    FROM MENJALANKAN_MISI_UTAMA WHERE username_pengguna = '{username}'""")

    data = get_session_data(request)
    data['list_menjalankan_misi_utama'] = list_menjalankan_misi_utama

    return render(request,'pemain_read_menjalankan_misi_utama.html', data)

@csrf_exempt
def pemain_menjalankan_misi_utama(request):
    if is_authenticated(request):
        username = request.session['username']

        if request.POST.get('NamaTokoh') != None:
            return buat_menjalankan_misi(request)

        tokoh_query = query(f"""
        SELECT nama FROM tokoh where username_pengguna = '{username}'
        """)

        misi_query = query(f"""
        SELECT nama_misi
        FROM MISI_UTAMA
        """)

        data = get_session_data(request)
        data['tokoh'] = tokoh_query
        data['misi_utama'] = misi_query

        return render(request, "menjalankan_misi.html", data)
    else:
        return login(request)

def buat_menjalankan_misi(request):
    if not is_authenticated:
        return login(request)
    else:
        username = request.session.get('username')
        nama_tokoh = request.POST.get('NamaTokoh')
        nama_misi = request.POST.get('NamaMisi')
        print(username)
        print(nama_tokoh)
        print(nama_misi)

        query(f"""
        INSERT INTO menjalankan_misi_utama
        VALUES('{username}', '{nama_tokoh}', '{nama_misi}', 'In Progress')
        """)

        return redirect('/menjalankan_misi_utama/pemain_read_menjalankan_misi_utama/')

@csrf_exempt
def pemain_update_menjalankan_misi_view(request,namaTokoh, namaMisi):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    username = request.session['username']
    list_menjalankan_misi = query(f"""SELECT nama_tokoh, nama_misi, status 
    FROM MENJALANKAN_MISI_UTAMA WHERE nama_misi = '{namaMisi}' AND nama_tokoh = '{namaTokoh}'""")

    data = get_session_data(request)
    data['list_menjalankan_misi'] = list_menjalankan_misi

    if request.method == 'POST':
        nama_tokoh= namaTokoh
        nama_misi= namaMisi
        status= request.POST.get('status')

        print(nama_tokoh)
        print(nama_misi)
        print(status)

        query(f"""
            UPDATE MENJALANKAN_MISI_UTAMA
            SET status = '{status}'
            WHERE username_pengguna = '{username}'
            AND nama_tokoh = '{nama_tokoh}'
            AND nama_misi = '{nama_misi}';
        """)
        
        return redirect('/menjalankan_misi_utama/pemain_read_menjalankan_misi_utama/')
    return render(request,'pemain_update_menjalankan_misi.html', data)
    
