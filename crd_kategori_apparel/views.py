from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

# Create your views here.


def create_kategori_apparel(request):
    if not is_authenticated(request):
        return login(request)

    if request.session['role'] == 'pemain':
        return HttpResponse("Hanya admin yang dapat membuat kategori apparel")

    # TODO: implement Create functionality
    if request.method == "POST":

        categoryName = request.POST["kategori"]

        query(f"""
            INSERT INTO KATEGORI_APPAREL
            VALUES('{categoryName}')
        """)

        return redirect("crd_kategori_apparel:read_kategori_apparel")

    return render(request, 'admin_create_kategori_apparel.html')


def read_kategori_apparel(request):
    if not is_authenticated(request):
        return login(request)

    list_kategori_apparel = query("SELECT * FROM KATEGORI_APPAREL")

    list_kategori_apparel_deletable = query("""
    SELECT DISTINCT nama_kategori from KATEGORI_APPAREL
    WHERE nama_kategori NOT IN (
        SELECT kategori_apparel from APPAREL
    )
    """)

    data = get_session_data(request)
    data['list_kategori_apparel'] = list_kategori_apparel
    data['list_kategori_apparel_deletable'] = list(
        map(lambda x: x[0], list_kategori_apparel_deletable))

    if request.session['role'] == "admin":
        return render(request, 'admin_read_kategori_apparel.html', data)
    else:
        return render(request, 'pemain_read_kategori_apparel.html', data)

def delete_kategori_apparel(request, category):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Hanya admin yang dapat membuat kategori apparel")

    query(f"DELETE FROM KATEGORI_APPAREL WHERE nama_kategori = '{category}'")
    
    return redirect("crd_kategori_apparel:read_kategori_apparel") 