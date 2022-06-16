from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_role, get_session_data, is_authenticated, login
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

# Create your views here.
@csrf_exempt
def read_pekerjaan(request):
    if not is_authenticated(request):
        return login(request)
    
    list_pekerjaan = query("SELECT * FROM pekerjaan")

    data = get_session_data(request)
    data['list_pekerjaan'] = list_pekerjaan

    if request.session['role'] == "admin":
        if request.method == 'POST':
            if request.POST.get("NamaPekerjaanUpdate") != None:
                print(request.POST.get('NamaPekerjaanUpdate'))
                request.session['Kerja'] = request.POST.get('NamaPekerjaanUpdate')
                return redirect("/pekerjaan/admin_update_pekerjaan")

            if request.POST.get("NamaPekerjaanDelete") != None:
                request.session['Kerja'] = request.POST.get('NamaPekerjaanDelete')
                return admin_delete_pekerjaan(request)
        return render(request, 'admin_read_pekerjaan.html', data)
    else:
        return render(request, 'pemain_read_pekerjaan.html', data)

@csrf_exempt
def admin_update_pekerjaan(request):
    if not is_authenticated:
        return login(request)
    
    if request.method == 'POST':
        return update_pekerjaan(request)

    data = dict()
    data['Kerja'] = request.session.get('Kerja')

    return render(request, 'admin_update_pekerjaan.html', data)

@csrf_exempt
def update_pekerjaan(request):
    if not is_authenticated:
        return login(request)

    if request.session['role'] == "pemain":
        return HttpResponse("Anda bukanlah admin")

    nama = request.session.get("Kerja")
    gaji = request.POST.get("BaseHonor")
    update_query = query(f"""
    UPDATE pekerjaan SET base_honor = {gaji} WHERE nama = '{nama}'
    """)

    return redirect("/pekerjaan/read_pekerjaan")

@csrf_exempt
def admin_delete_pekerjaan(request):
    if not is_authenticated:
        return login(request)

    nama = request.session.get("Kerja")
    update_query = query(f"""
    DELETE FROM pekerjaan WHERE nama = '{nama}'
    """)

    return redirect("/pekerjaan/read_pekerjaan")


def read_bekerja(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == "admin":
        list_bekerja = query("SELECT * FROM bekerja")
        data = get_session_data(request)
        data['list_bekerja'] = list_bekerja
        
        return render(request, "admin_read_bekerja.html", data)
        
    if request.session['role'] == "pemain":
        username = request.session['username']
        list_bekerja = query(f"SELECT * FROM bekerja WHERE username_pengguna = '{username}'")
        data = get_session_data(request)
        data['list_bekerja'] = list_bekerja
        
        return render(request, "pemain_read_bekerja.html", data)

@csrf_exempt
def admin_create_pekerjaan_view(request):
    if not is_authenticated:
        return login(request)

    if request.session.get('role') != "admin":
        return HttpResponse("Role anda bukanlah admin")

    if request.method == 'POST':
        return create_pekerjaan_baru(request)

    return render(request, "admin_create_pekerjaan.html")

@csrf_exempt
def pemain_create_bekerja_view(request):
    if not is_authenticated:
        return login(request)

    if request.session.get('role') != "pemain":
        return HttpResponse('Role anda bukanlah pemain')

    if request.method == 'POST':
        return create_mulai_bekerja(request)

    return render(request, "pemain_create_bekerja.html")

@csrf_exempt
def create_pekerjaan_baru(request):
    if not is_authenticated:
        return login(request)
    
    pekerjaan = request.POST.get('NamaPekerjaan')
    gaji = request.POST.get('BaseHonor')
    add_pekerjaan_query = query(f"""
    INSERT INTO pekerjaan VALUES('{pekerjaan}', {gaji})
    """)

    return redirect('/pekerjaan/read_pekerjaan')

@csrf_exempt
def create_mulai_bekerja(request):
    if not is_authenticated:
        return login(request)

    username = request.session.get('username')
    nama = request.POST.get('NamaTokoh')
    pekerjaan = request.POST.get('NamaPekerjaan')
    gaji = request.POST.get('BaseSalary')
    time = datetime.now()
    now = time.strftime("%d/%m/%Y %H:%M:%S")

    check_query = query(f"""
    SELECT nama FROM tokoh WHERE username_pengguna='{username}' AND nama='{nama}' AND pekerjaan='{pekerjaan}'
    """)
    print(check_query)

    if type(check_query) == list:
        if len(check_query) == 1:
            jumlah_keberangkatan_query = query(f"""
            SELECT jumlah_keberangkatan FROM bekerja WHERE username_pengguna='{username}' AND nama_tokoh='{nama}' ORDER BY jumlah_keberangkatan DESC LIMIT 1
            """)

            level_query = query(f"""
            SELECT level FROM tokoh WHERE username_pengguna='{username}' AND nama='{nama}'
            """)

            jumlah_keberangkatan = jumlah_keberangkatan_query[0][0]
            print(jumlah_keberangkatan)
            level = level_query[0][0]
            print(level)
            honor = gaji * level
            jumlah_keberangkatan = jumlah_keberangkatan + 1
            start_work_query = query(f"""
            INSERT INTO bekerja VALUES('{username}', '{nama}', '{time}', '{pekerjaan}', {jumlah_keberangkatan}, {honor})
            """)

        return redirect("/pekerjaan/read_bekerja")
