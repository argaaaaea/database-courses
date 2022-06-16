from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

def read_warna_kulit(request):
    if not is_authenticated(request):
        return login(request)

    list_warna_kulit = query("""
    SELECT *,
    CASE WHEN kode NOT IN (SELECT warna_kulit FROM TOKOH) THEN 'true' ELSE 'false'
    END AS can_delete
    FROM WARNA_KULIT
    ORDER BY kode ASC;
    """)

    data = get_session_data(request)
    data['list_warna_kulit'] = list_warna_kulit

    if request.session['role'] == 'admin':
        if request.method == 'POST':
            if request.POST.get("DeleteButton") != None:
                request.session['Kode'] = request.POST.get('DeleteButton')
                return delete_warna_kulit(request)
        
        return render(request, 'admin_read_warna_kulit.html', data)

    if request.session['role'] == 'pemain':
        return render(request, 'pemain_read_warna_kulit.html', data)

def create_warna_kulit_view(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    data = get_session_data(request)

    if request.method == 'POST':
        return create_warna_kulit(request)
    
    return render(request, "create_warna_kulit.html", data)

def create_warna_kulit(request):
    if not is_authenticated(request):
        return login(request)

    kode = request.POST.get('Kode')
    add_level_query = query(f"""
    INSERT INTO WARNA_KULIT
    VALUES('{kode}')
    """)

    return redirect('/warna_kulit/read_warna_kulit/')

def delete_warna_kulit(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    kode = request.session.get("Kode")
    delete_warna_kulit_query = query(f"""
        DELETE FROM WARNA_KULIT
        WHERE kode = '{kode}'
    """)

    return redirect('/warna_kulit/read_warna_kulit/')