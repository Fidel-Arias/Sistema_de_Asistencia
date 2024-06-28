from django.shortcuts import render, redirect
from django.urls import reverse
from Admin.models import MaeAdministrador
from Participantes.models import MaeParticipantes
from Colaborador.models import MaeColaborador

# Create your views here.
def user_logged_in(request, pk):
    if request.method == 'POST':
        # print('Method: ', request.POST)
        codigo = request.POST.get('codigo')
        if codigo:
            try:
                participante = MaeParticipantes.objects.get(pk=codigo)
                request.session['codparticipante'] = codigo
                print('Requested codigo User: ', request.session.get('codparticipante'))
                urlDirect = '/user/'+codigo
                return redirect(urlDirect)
            except MaeParticipantes.DoesNotExist:
                return redirect(reverse('Login') + '?error=Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def admin_logged_in(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('codigo')
        if contrasenia and correo:
            try:
                admin = MaeAdministrador.objects.get(correo=correo, contrasenia=contrasenia)
                request.session['contrasenia'] = contrasenia
                urlDirect = reverse('Administrador', args=[correo, contrasenia])
                return redirect(urlDirect)
            except MaeAdministrador.DoesNotExist:
                return redirect(reverse('LoguingAdministrador') + '?error=Usuario o contraseña incorrectos')
    return redirect(reverse('LoguingAdministrador'))

def colaborador_logged_in(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasenia = request.POST.get('codigo')
        if contrasenia and correo:
            try:
                colaborador = MaeColaborador.objects.get(correo=correo, contrasenia=contrasenia)
                request.session['codcolaborador'] = contrasenia
                print('Requested codigo Colaborador: ', request.session.get('codcolaborador'))
                urlDirect = reverse('Colaborador', args=[correo, contrasenia])
                return redirect(urlDirect)
            except MaeColaborador.DoesNotExist:
                return redirect(reverse('LoguingColaborador') + '?error=Usuario o contraseña incorrectos')
    return render(request, 'loginColaborador.html')

def login(request):
    error_message = request.GET.get('error', '')
    return render(request, 'login.html', {'error': error_message})

def loginColaborador(request):
    return render(request, 'loginColaborador.html')

def loginAdmin(request):
    error_message = request.GET.get('error', '')
    return render(request, 'loginAdmin.html', {'error': error_message})

