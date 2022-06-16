from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

# Create your views here.


def create_koleksi_tokoh(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] != 'pemain':
        return HttpResponse("Hanya pemain yang dapat membuat koleksi tokoh")

    username = request.session['username']

    if request.method == "POST":

        id_koleksi = request.POST["koleksi"]
        nama_tokoh = request.POST["tokoh"]

        query(f"""
                INSERT INTO KOLEKSI_TOKOH
                VALUES('{id_koleksi}', '{username}', '{nama_tokoh}')
            """)

        return redirect("crd_koleksi_tokoh:read_koleksi_tokoh")

    list_nama_tokoh = query(f"""
        SELECT nama FROM TOKOH WHERE username_pengguna = '{username}'
    """)

    list_koleksi = query(f"""
        SELECT id, harga FROM KOLEKSI
    """)

    context = {
        "list_nama_tokoh": list_nama_tokoh,
        "list_koleksi": list_koleksi
    }

    return render(request, 'pemain_create_koleksi_tokoh.html', context)


def read_koleksi_tokoh(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == "admin":
        list_koleksi_tokoh = query("SELECT * FROM KOLEKSI_TOKOH")

        data = get_session_data(request)

        data['list_koleksi_tokoh'] = list_koleksi_tokoh
        return render(request, 'admin_read_koleksi_tokoh.html', data)
    else:
        list_koleksi_tokoh = query(
            f"SELECT * FROM KOLEKSI_TOKOH WHERE username_pengguna = '{request.session['username']}'")

        list_deletable = query(f"""
            SELECT DISTINCT id_koleksi from KOLEKSI_TOKOH
            WHERE id_koleksi NOT IN (
                SELECT id_rambut from TOKOH
                WHERE username_pengguna = '{request.session['username']}'
            ) AND id_koleksi IN (
                SELECT id_koleksi from RAMBUT
            ) 
            UNION 
            SELECT DISTINCT id_koleksi from KOLEKSI_TOKOH
            WHERE id_koleksi NOT IN (
                SELECT id_mata from TOKOH
                WHERE username_pengguna = '{request.session['username']}'
            ) AND id_koleksi IN (
                SELECT id_koleksi from MATA
            )
            UNION 
            SELECT DISTINCT id_koleksi from KOLEKSI_TOKOH
            WHERE id_koleksi NOT IN (
                SELECT id_rumah from TOKOH
                WHERE username_pengguna = '{request.session['username']}'
            ) AND id_koleksi IN (
                SELECT id_koleksi from RUMAH
            )
            UNION 
            SELECT DISTINCT id_koleksi from KOLEKSI_TOKOH
            WHERE id_koleksi NOT IN (
                SELECT id_barang from MENGGUNAKAN_BARANG
                WHERE username_pengguna = '{request.session['username']}'
            ) AND id_koleksi IN (
                SELECT id_koleksi from BARANG
            )
            UNION 
            SELECT DISTINCT id_koleksi from KOLEKSI_TOKOH
            WHERE id_koleksi NOT IN (
                SELECT id_koleksi from MENGGUNAKAN_APPAREL
                WHERE username_pengguna = '{request.session['username']}'
            ) AND id_koleksi IN (
                SELECT id_koleksi from APPAREL
            )
        """)

        data = get_session_data(request)

        data['list_koleksi_tokoh'] = list_koleksi_tokoh
        data['list_deletable'] = list(map(lambda x: x[0], list_deletable))
        
        return render(request, 'pemain_read_koleksi_tokoh.html', data)

def delete_koleksi_tokoh(request, id_koleksi):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] != "pemain":
        return HttpResponse("Hanya pemain yang dapat menghapus koleksi tokoh")

    query(f"""
        DELETE FROM KOLEKSI_TOKOH
        WHERE id_koleksi = '{id_koleksi}'
    """)

    return redirect("crd_koleksi_tokoh:read_koleksi_tokoh")