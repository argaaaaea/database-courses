from django.shortcuts import redirect, render, HttpResponse
from utils.query import query
from django.views.decorators.csrf import csrf_exempt
from home.views import get_session_data, is_authenticated, login

# Create your views here.
def admin_read_makanan(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_makanan = query("""SELECT *, 
    CASE WHEN nama NOT IN (SELECT DISTINCT nama_makanan FROM MAKAN)
    THEN 'true' ELSE 'false' END AS delete FROM MAKANAN""")

    data = get_session_data(request)
    data['list_makanan'] = list_makanan

    return render(request,'admin_read_makanan.html', data)

def pemain_read_makanan(request):
    username = request.session["username"]

    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'admin':
        return HttpResponse("Anda bukanlah pemain")
    
    list_makanan = query(f"""SELECT * 
    FROM MAKANAN""")

    data = get_session_data(request)
    data['list_makanan'] = list_makanan

    return render(request,'pemain_read_makanan.html', data)

def admin_create_makanan_view(request):
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    if request.method == 'POST':
        return create_makanan(request)

    return render(request, "admin_create_makanan.html")

@csrf_exempt
def create_makanan(request):
    if not is_authenticated(request):
        return login(request)

    nama = request.POST.get('NamaMakanan')            
    harga = request.POST.get('harga')
    tingkat_energi = request.POST.get('TingkatEnergi')
    tingkat_kelaparan = request.POST.get('TingkatKelaparan')

    query_addMakanan = query(f"""
    INSERT INTO makanan VALUES ('{nama}', {harga},
    {tingkat_energi}, {tingkat_kelaparan})
    """)
    print(query_addMakanan)

    return redirect('/makanan/admin_read_makanan/')

def admin_delete_makanan(request, nama):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    query(f"DELETE FROM MAKANAN WHERE NAMA = '{nama}'")
    
    return redirect('/makanan/admin_read_makanan/')

@csrf_exempt
def admin_update_makanan_view(request,nama):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    list_makann = query(f"SELECT * FROM MAKANAN WHERE nama = '{nama}'")
    data = get_session_data(request)
    data['list_makann'] = list_makann

    if request.method == 'POST':
        harga = request.POST.get('harga')
        tingkat_energi= request.POST.get('TingkatEnergi')
        tingkat_kelaparan= request.POST.get('TingkatKelaparan')

        query(f"""UPDATE MAKANAN SET harga = {harga},
        tingkat_energi = {tingkat_energi}, tingkat_kelaparan = {tingkat_kelaparan}
        WHERE nama = '{nama}';""")

        return redirect('/makanan/admin_read_makanan/')
    return render(request,'admin_update_makanan.html', data)
    
