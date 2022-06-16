from django.shortcuts import redirect, render, HttpResponse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from home.views import get_session_data, is_authenticated, login

# Create your views here.
def admin_read_misi_utama(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_misi_utama = query("""SELECT *,
    CASE WHEN nama_misi NOT IN (SELECT DISTINCT nama_misi FROM MENJALANKAN_MISI_UTAMA)
    THEN 'true' ELSE 'false' END AS delete FROM MISI_UTAMA""")

    data = get_session_data(request)
    data['list_misi_utama'] = list_misi_utama

    return render(request,'admin_read_misi_utama.html', data)

def admin_detail_misi_utama(request, nama):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_misi = query(f"SELECT * FROM MISI WHERE nama = '{nama}'")

    data = get_session_data(request)
    data['list_misi'] = list_misi

    print(list_misi)
    return render(request,'admin_detail_misi_utama.html', data)

def pemain_read_misi_utama(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    list_misi_utama = query("SELECT * FROM MISI_UTAMA")

    data = get_session_data(request)
    data['list_misi_utama'] = list_misi_utama

    return render(request,'pemain_read_misi_utama.html', data)

def pemain_detail_misi_utama(request, nama):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    list_misi = query(f"SELECT * FROM MISI WHERE nama = '{nama}'")

    data = get_session_data(request)
    data['list_misi'] = list_misi

    return render(request,'pemain_detail_misi_utama.html', data)

@csrf_exempt
def admin_create_misi_view(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    if request.method == 'POST':
        return create_misi_utama(request)

    return render(request, "admin_create_misi.html")

@csrf_exempt
def create_misi_utama(request):
    if not is_authenticated(request):
        return login(request)

    nama = request.POST.get('NamaMisiUtama')            
    efek_energi = request.POST.get('EfekEnergi')
    efek_hubungan = request.POST.get('EfekHubungan')
    efek_kelaparan = request.POST.get('EfekKelaparan')
    syarat_energi = request.POST.get('SyaratEnergi')
    syarat_hubungan = request.POST.get('SyaratHubungan')
    syarat_kelaparan = request.POST.get('SyaratKelaparan')
    completion_time = request.POST.get('CompletionTime')
    reward_koin = request.POST.get('RewardKoin')
    reward_xp = request.POST.get('RewardXP')
    deskripsi = request.POST.get ('Deskripsi')

    query_addMisi = query(f"""
    INSERT INTO misi VALUES ('{nama}', {efek_energi},{efek_hubungan}, {efek_kelaparan},
    {syarat_energi}, {syarat_hubungan}, {syarat_kelaparan},'{completion_time}',
    {reward_koin}, {reward_xp}, '{deskripsi}')
    """)
    print(query_addMisi)
    query_addMisiUtama = query(f"""
    INSERT INTO misi_utama VALUES ('{nama}')
    """)

    return redirect('/misi_utama/admin_read_misi_utama/')

def admin_delete_misi_utama(request, nama):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    query(f"DELETE FROM MISI_UTAMA WHERE NAMA_MISI = '{nama}'")
    
    return redirect('/misi_utama/admin_read_misi_utama/')

