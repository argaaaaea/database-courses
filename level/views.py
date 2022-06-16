from django.shortcuts import render, HttpResponse, redirect
from utils.query import query
from home.views import get_session_data, is_authenticated, login

def read_level(request):
    if not is_authenticated(request):
        return login(request)

    list_level = query("""
    SELECT *,
    CASE WHEN level NOT IN (SELECT level FROM TOKOH) THEN 'true' ELSE 'false'
    END AS can_delete
    FROM LEVEL
    ORDER BY level ASC;
    """)

    data = get_session_data(request)
    data['list_level'] = list_level

    if request.session['role'] == 'admin':
        if request.method == 'POST':
            if request.POST.get("DeleteButton") != None:
                request.session['Level'] = request.POST.get('DeleteButton')
                return delete_level(request)
        
        return render(request, 'admin_read_level.html', data)

    if request.session['role'] == 'pemain':
        return render(request, 'pemain_read_level.html', data)

def create_level_view(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    data = get_session_data(request)

    if request.method == 'POST':
        return create_level(request)
    
    return render(request, "create_level.html", data)

def create_level(request):
    if not is_authenticated(request):
        return login(request)

    level = request.POST.get('Level')
    xp = request.POST.get('XP')
    add_level_query = query(f"""
    INSERT INTO LEVEL
    VALUES({level}, {xp})
    """)

    return redirect('/level/read_level/')

def update_level_view(request, level, xp):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")

    data = get_session_data(request)
    data['level'] = level
    data['xp'] = xp

    if request.method == 'POST':
        return update_level(request)

    return render(request, 'update_level.html', data)

def update_level(request):
    if not is_authenticated(request):
        return login(request)

    level = request.POST.get('Level')
    xp = request.POST.get('XP')

    update_level_query = query(f"""
        UPDATE LEVEL
        SET xp = {xp}
        WHERE level = {level}
    """)

    return redirect('/level/read_level/')

def delete_level(request):
    if not is_authenticated(request):
        return login(request)
    
    if request.session['role'] == 'pemain':
        return HttpResponse("Anda bukanlah admin")
    
    level = request.session.get("Level")
    delete_warna_kulit_query = query(f"""
        DELETE FROM LEVEL
        WHERE level = '{level}'
    """)

    return redirect('/level/read_level/')