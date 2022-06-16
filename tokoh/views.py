from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def admin_read_tokoh(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    if request.POST.get('NamaTokoh') != None:
        request.session['NamaTokoh'] = request.POST.get('NamaTokoh')
        return admin_detail_page(request)
    
    list_tokoh = query("SELECT * FROM tokoh")

    data = get_session_data(request)
    data['list_tokoh'] = list_tokoh
    print(data['list_tokoh'])

    return render(request, 'admin_read_tokoh.html', data)

def pemain_read_tokoh(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse('Anda bukanlah pemain')

    print(request.POST.get("Nama"))
    if request.POST.get("NamaTokoh") != None:
        request.session['NamaTokoh'] = request.POST.get('NamaTokoh')
        return redirect('/tokoh/pemain_detail_page')

    if request.POST.get("Nama") != None:
        request.session['Nama'] = request.POST.get('Nama')
        return redirect('/tokoh/pemain_update_tokoh')

    username = request.session['username']
    list_tokoh_pemain = query(f"SELECT * FROM tokoh WHERE username_pengguna = '{username}'")

    data = get_session_data(request)
    data['list_tokoh'] = list_tokoh_pemain

    return render(request, 'pemain_read_tokoh.html', data)

@csrf_exempt
def pemain_create_tokoh(request):
    print("here")
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'admin':
        return HttpResponse('Anda bukanlah pemain')

    print(request.POST.get('NamaTokoh'))
    if request.POST.get("NamaTokoh") != None:
        return create_tokoh(request)

    warna_kulit_query = query(f"""
    SELECT kode FROM warna_kulit
    """)
    print(warna_kulit_query)

    pekerjaan_query = query(f"""
    SELECT nama FROM pekerjaan
    """)
    print(pekerjaan_query)

    data = get_session_data(request)
    data['warna_kulit'] = warna_kulit_query
    data['pekerjaan'] = pekerjaan_query

    return render(request, "pemain_create_tokoh.html", data)

@csrf_exempt
def create_tokoh(request):
    if not is_authenticated(request):
        return login(request)

    username = request.session['username']

    nama = request.POST.get('NamaTokoh')
    jenis_kelamin = request.POST.get('jenisKelaminTokoh')
    warna_kulit = request.POST.get('WarnaKulit')
    pekerjaan = request.POST.get('Pekerjaan')

    find_tokoh_pemain = query(f"SELECT nama FROM tokoh WHERE username_pengguna = '{username}' AND nama = '{nama}'")
    if (type(find_tokoh_pemain)) == list:
        if len(find_tokoh_pemain) == 0:
            tokoh_query = query(f"""
            SELECT CreateTokoh('{username}', '{nama}', '{jenis_kelamin}', '{warna_kulit}', '{pekerjaan}')
            """)
            return redirect('/tokoh/pemain_read_tokoh')
            #the create tokoh is not done yet
    return render(request, 'pemain_create_tokoh.html')

def admin_read_warna_kulit(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    list_warna_kulit = query("SELECT * FROM warna_kulit")

    data = get_session_data(request)
    data['list_warna_kulit'] = list_warna_kulit
    data['idy'] = 0

    return render(request, 'html for read warna kulit', data)

def pemain_read_warna_kulit(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")

    list_warna_kulit = query("SELECT * FROM warna_kulit")

    data = get_session_data(request)
    data['list_warna_kulit'] = list_warna_kulit
    data['idy'] = 0
    
    return render(request, "html for pemain read warna kulit", data)

def admin_detail_page(request):
    if is_authenticated(request):
        print("terotentikasi")

        nama_tokoh = request.session.get('NamaTokoh')
        data_query = query(f"SELECT * FROM tokoh WHERE nama LIKE '%{nama_tokoh}%'")
        data = get_session_data(request)
        data["list"] = data_query
        print(data['list'])
        print(data)


        return render(request, "admin_detail_page.html", data)
    else:
        print("tidak terotentikasi")
        return login(request)

def pemain_detail_page(request):
    if is_authenticated(request):
        print("terotentikasi")

        nama_tokoh = request.session.get('NamaTokoh')
        username = request.session.get("username")
        data_query = query(f"SELECT * FROM tokoh WHERE  username_pengguna ='{username}' AND nama LIKE '%{nama_tokoh}%'")
        print(data_query)
        data = get_session_data(request)
        data["list"] = data_query
        print(data_query)


        return render(request, "admin_detail_page.html", data)
    else:
        print("tidak terotentikasi")
        return login(request)

@csrf_exempt
def pemain_update_tokoh(request):
    if is_authenticated(request):
        username = request.session['username']
        nama_tokoh = request.session['Nama']

        if request.POST.get('rambut') != None:
            return update_tokoh(request, nama_tokoh)

        data_query = query(f"SELECT nama FROM tokoh WHERE nama LIKE '%{nama_tokoh}%'")
        print(data_query[0][0])

        id_rambut_query = query(f"""
        SELECT id_koleksi FROM rambut
        """)

        id_mata_query = query(f"""
        SELECT id_koleksi FROM mata
        """)

        id_rumah_query = query(f"""
        SELECT id_koleksi FROM rumah
        """)

        data = get_session_data(request)
        data['nama'] = data_query
        data['id_rambut'] = id_rambut_query
        data['id_mata'] = id_mata_query
        data['id_rumah'] = id_rumah_query
        return render(request, "pemain_update_tokoh.html", data)
    else:
        return login(request)

@csrf_exempt
def update_tokoh(request, nama_tokoh):
    body = request.POST
    username = request.session['username']
    nama_query = query(f"""
    SELECT nama FROM tokoh WHERE username_pengguna = '{username}' AND nama LIKE '%{nama_tokoh}%'
    """)
    nama = str(nama_query[0][0])
    print(nama)

    rambut = body.get("rambut")
    mata = body.get("mata")
    rumah = body.get("rumah")

    update_query = query(f"""
    SELECT UpdateTokoh('{username}', '{nama}', '{rambut}', '{mata}', '{rumah}')
    """)
    print(update_query)

    return redirect("/tokoh/pemain_read_tokoh")
