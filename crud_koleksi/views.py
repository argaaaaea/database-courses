from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

# Create your views here.
def create_koleksi(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == "admin":
        return render(request, "admin_create_koleksi.html")
    else:
        return render(request, "pemain_create_koleksi.html")
    

def create_koleksi_rambut(request):
    if not is_authenticated(request):
        return login(request)

    if request.method == "POST":    

        id_koleksi = request.POST['id_koleksi']
        harga_jual = request.POST['harga_jual']
        tipe_rambut = request.POST['tipe_rambut']

        query(f"""
            INSERT INTO KOLEKSI VALUES ('{id_koleksi}', {harga_jual})
        """)

        query(f"""
            INSERT INTO RAMBUT VALUES ('{id_koleksi}', '{tipe_rambut}')
        """)

        return redirect("crud_koleksi:read_koleksi_rambut")
    
    last_id = query("""
            SELECT id_koleksi from RAMBUT ORDER BY id_koleksi DESC LIMIT 1
        """)[0][0]

    new_id = f"RB{str.zfill(str(int(last_id[2:]) + 1), 3)}"

    context = {
        "new_id": new_id
    }

    return render(request, "admin_create_koleksi_rambut.html", context)

def create_koleksi_mata(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.method == "POST":    

        id_koleksi = request.POST['id_koleksi']
        harga_jual = request.POST['harga_jual']
        warna = request.POST['warna']

        query(f"""
            INSERT INTO KOLEKSI VALUES ('{id_koleksi}', {harga_jual})
        """)

        query(f"""
            INSERT INTO MATA VALUES ('{id_koleksi}', '{warna}')
        """)

        return redirect("crud_koleksi:read_koleksi_mata")

    
    last_id = query("""
            SELECT id_koleksi from MATA ORDER BY id_koleksi DESC LIMIT 1
        """)[0][0]

    new_id = f"MT{str.zfill(str(int(last_id[2:]) + 1), 3)}"

    context = {
        "new_id": new_id
    }

    return render(request, "admin_create_koleksi_mata.html", context)

def create_koleksi_rumah(request):
    if not is_authenticated(request):
        return login(request)

    if request.method == "POST":    

        id_koleksi = request.POST['id_koleksi']
        nama = request.POST['nama']
        harga_jual = request.POST['harga_jual']
        harga_beli = request.POST['harga_beli']
        kapasitas_barang = request.POST['kapasitas_barang']

        query(f"""
            INSERT INTO KOLEKSI VALUES ('{id_koleksi}', {harga_jual})
        """)

        query(f"""
            INSERT INTO KOLEKSI_JUAL_BELI VALUES ('{id_koleksi}', {harga_beli}, '{nama}')
        """)

        query(f"""
            INSERT INTO RUMAH VALUES ('{id_koleksi}', {kapasitas_barang})
        """)

        return redirect("crud_koleksi:read_koleksi_rumah")

    last_id = query("""
            SELECT id_koleksi from RUMAH ORDER BY id_koleksi DESC LIMIT 1
        """)[0][0]

    new_id = f"RM{str.zfill(str(int(last_id[2:]) + 1), 3)}"

    context = {
        "new_id": new_id
    }

    return render(request, "admin_create_koleksi_rumah.html", context)

def create_koleksi_barang(request):
    if not is_authenticated(request):
        return login(request)

    if request.method == "POST":    

        id_koleksi = request.POST['id_koleksi']
        nama = request.POST['nama']
        harga_jual = request.POST['harga_jual']
        harga_beli = request.POST['harga_beli']
        tingkat_energi = request.POST['tingkat_energi']

        query(f"""
            INSERT INTO KOLEKSI VALUES ('{id_koleksi}', {harga_jual})
        """)

        query(f"""
            INSERT INTO KOLEKSI_JUAL_BELI VALUES ('{id_koleksi}', {harga_beli}, '{nama}')
        """)

        query(f"""
            INSERT INTO BARANG VALUES ('{id_koleksi}', {tingkat_energi})
        """)

        return redirect("crud_koleksi:read_koleksi_barang")

    last_id = query("""
            SELECT id_koleksi from BARANG ORDER BY id_koleksi DESC LIMIT 1
        """)[0][0]

    new_id = f"BR{str.zfill(str(int(last_id[2:]) + 1), 3)}"

    context = {
        "new_id": new_id
    }

    return render(request, "admin_create_koleksi_barang.html", context)

def create_koleksi_apparel(request):
    if not is_authenticated(request):
        return login(request)

    if request.method == "POST":    

        id_koleksi = request.POST['id_koleksi']
        nama = request.POST['nama']
        harga_jual = request.POST['harga_jual']
        harga_beli = request.POST['harga_beli']
        warna_apparel = request.POST['warna_apparel']
        nama_pekerjaan = request.POST['nama_pekerjaan']
        kategori_apparel = request.POST['kategori_apparel']

        query(f"""
            INSERT INTO KOLEKSI VALUES ('{id_koleksi}', {harga_jual})
        """)

        query(f"""
            INSERT INTO KOLEKSI_JUAL_BELI VALUES ('{id_koleksi}', {harga_beli}, '{nama}')
        """)

        query(f"""
            INSERT INTO APPAREL VALUES ('{id_koleksi}', '{warna_apparel}', '{nama_pekerjaan}', '{kategori_apparel}')
        """)

        return redirect("crud_koleksi:read_koleksi_apparel")

    last_id = query("""
            SELECT id_koleksi from APPAREL ORDER BY id_koleksi DESC LIMIT 1
        """)[0][0]

    new_id = f"AP{str.zfill(str(int(last_id[2:]) + 1), 3)}"

    kategori_apparel = query("""
        select nama_kategori from KATEGORI_APPAREL
    """)

    pekerjaan = query("""
        select nama from PEKERJAAN
    """)

    context = {
        "new_id": new_id,
        "kategori_apparel": kategori_apparel,
        "pekerjaan": pekerjaan
    }

    return render(request, "admin_create_koleksi_apparel.html", context)

def read_koleksi(request):
    if not is_authenticated(request):
        return login(request)
    if request.session['role'] == "admin":
        return render(request, "admin_read_koleksi.html")
    else:
        return render(request, "pemain_read_koleksi.html")

def read_koleksi_mata(request):
    if not is_authenticated(request):
        return login(request)
    
    list_koleksi_mata = query("SELECT * FROM KOLEKSI, MATA WHERE KOLEKSI.id = MATA.id_koleksi")

    data = get_session_data(request)
    data['list_koleksi_mata'] = list_koleksi_mata

    if request.session['role'] == "admin":
        return render(request, 'admin_read_koleksi_mata.html', data)
    else:
        return render(request, 'pemain_read_koleksi_mata.html', data)

def read_koleksi_rambut(request):
    if not is_authenticated(request):
        return login(request)
    
    list_koleksi_rambut = query("SELECT * FROM KOLEKSI, RAMBUT WHERE KOLEKSI.id = RAMBUT.id_koleksi")

    data = get_session_data(request)
    data['list_koleksi_rambut'] = list_koleksi_rambut

    if request.session['role'] == "admin":
        return render(request, 'admin_read_koleksi_rambut.html', data)
    else:
        return render(request, 'pemain_read_koleksi_rambut.html', data)

def read_koleksi_barang(request):
    if not is_authenticated(request):
        return login(request)
    
    list_koleksi_barang = query("SELECT K.id, K.harga, KJB.harga_beli, KJB.nama, B.tingkat_energi FROM KOLEKSI AS K, KOLEKSI_JUAL_BELI AS KJB, BARANG AS B WHERE K.id = B.id_koleksi AND K.id = KJB.id_koleksi")

    data = get_session_data(request)
    data['list_koleksi_barang'] = list_koleksi_barang

    if request.session['role'] == "admin":
        return render(request, 'admin_read_koleksi_barang.html', data)
    else:
        return render(request, 'pemain_read_koleksi_barang.html', data)


def read_koleksi_rumah(request):
    if not is_authenticated(request):
        return login(request)
    
    list_koleksi_rumah = query("SELECT K.id, K.harga, KJB.harga_beli, KJB.nama, R.kapasitas_barang FROM KOLEKSI AS K, KOLEKSI_JUAL_BELI AS KJB, RUMAH AS R WHERE K.id = R.id_koleksi AND K.id = KJB.id_koleksi")

    data = get_session_data(request)
    data['list_koleksi_rumah'] = list_koleksi_rumah

    if request.session['role'] == "admin":
        return render(request, 'admin_read_koleksi_rumah.html', data)
    else:
        return render(request, 'pemain_read_koleksi_rumah.html', data)

def read_koleksi_apparel(request):
    if not is_authenticated(request):
        return login(request)
    
    list_koleksi_apparel = query("SELECT K.id, K.harga, KJB.harga_beli, KJB.nama, A.warna_apparel, A.nama_pekerjaan, A.kategori_apparel FROM KOLEKSI AS K, KOLEKSI_JUAL_BELI AS KJB, APPAREL AS A WHERE K.id = A.id_koleksi AND K.id = KJB.id_koleksi")

    data = get_session_data(request)
    data['list_koleksi_apparel'] = list_koleksi_apparel

    if request.session['role'] == "admin":
        return render(request, 'admin_read_koleksi_apparel.html', data)
    else:
        return render(request, 'pemain_read_koleksi_apparel.html', data)