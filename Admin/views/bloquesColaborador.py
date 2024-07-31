from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from Bloque.models import MaeBloque
from Colaborador.models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from CongresoJINIS.models import MaeCongresoJinis
from django.contrib import messages

@login_required
def registrar_bloques_colaboradores(request):
    if request.method == 'POST':
        colaborador = request.POST.get('colaborador')
        bloques = request.POST.getlist('bloques')
        action = request.POST.get('action')
        idcongreso = request.POST.get('congreso')

        if idcongreso:
            selected_congreso = idcongreso
        else:
            selected_congreso = None

        if action == 'register':
            try:
                if (not(BloqueColaborador.objects.filter(idcolaborador=colaborador).exists())):
                    with transaction.atomic():
                        for i in range(0, len(bloques)):
                            nuevo_bloqueColaborador = BloqueColaborador(
                                idcolaborador=MaeColaborador.objects.get(pk=colaborador),
                                idbloque=MaeBloque.objects.get(pk=bloques[i]),
                                idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                            )
                            nuevo_bloqueColaborador.save()
                        messages.success(request, 'Se registró exitosamente los bloques del colaborador')
                else:
                    messages.error(request, 'Ya existe el colaborador con sus bloques')
            except BloqueColaborador.DoesNotExist:
                messages.error(request, 'No se encontró al colaborador o a los bloques')
            except Exception as e:    
                messages.error(request, e) #unsupported operand type(s) for +: 'int' and 'str'
            return redirect('RegistrarBloqueColaborador')
        elif action == 'delete':
            try:
                bloques_colaborador = BloqueColaborador.objects.filter(idcolaborador=colaborador)
                with transaction.atomic():
                    for bloque_colaborador in bloques_colaborador:
                        bloque_colaborador.estado = 'NO ACTIVO'
                        bloque_colaborador.save()
                messages.success(request, 'Bloque del colaborador desactivado con éxito')
            except BloqueColaborador.DoesNotExist:
                messages.error(request, 'No se encontró al colaborador o al bloque')
            except Exception as e:    
                messages.error(request, e)
            return redirect('RegistrarBloqueColaborador')
        elif action == 'activate':
            try:
                bloques_colaborador = BloqueColaborador.objects.filter(idcolaborador=colaborador)
                with transaction.atomic():
                    for bloque_colaborador in bloques_colaborador:
                        bloque_colaborador.estado = 'ACTIVO'
                        bloque_colaborador.save()
                messages.success(request, 'Bloque del colaborador activado con éxito')
            except BloqueColaborador.DoesNotExist:
                messages.error(request, 'No se encontró al colaborador o al bloque')
            except Exception:    
                messages.error(request, 'Error al activar el bloque del colaborador') #unsupported operand type(s) for +: 'int' and 'str'
            return redirect('RegistrarBloqueColaborador')
        elif action == 'edit':
            idblcl = request.POST.get('id')
            try:
                bloque_colaborador = BloqueColaborador.objects.get(pk=idblcl)
                colaborador_obj = MaeColaborador.objects.get(pk=colaborador)

                # Eliminar los bloques actuales del colaborador
                BloqueColaborador.objects.filter(idcolaborador=colaborador_obj).delete()
                # Agregar los nuevos bloques seleccionados
                with transaction.atomic():
                    # Agregar los nuevos bloques seleccionados
                    for i in range(len(bloques)):
                        nuevo_bloqueColaborador = BloqueColaborador(
                            idcolaborador=colaborador_obj,
                            idbloque=MaeBloque.objects.get(pk=bloques[i]),
                            idcongreso=MaeCongresoJinis.objects.get(pk=idcongreso)
                        )
                        nuevo_bloqueColaborador.save()
                    messages.success(request, 'Bloques del colaborador actualizado con éxito')
            except BloqueColaborador.DoesNotExist:
                messages.error(request, 'No se encontró al colaborador o al bloque')
            return redirect('RegistrarBloqueColaborador')
        
        colaboradores = MaeColaborador.objects.filter(estado='ACTIVO').order_by('pk')
        bloques = MaeBloque.objects.filter(estado='ACTIVO', idcongreso=idcongreso).order_by('pk')

        bloquesToColaboradores = BloqueColaborador.objects.filter(idcongreso=idcongreso).order_by('pk')
        congresos = MaeCongresoJinis.objects.all().order_by('pk')

        # Agrupar bloques por colaborador
        bloques_por_colaborador = defaultdict(list)
        for blcl in bloquesToColaboradores:
            bloques_por_colaborador[blcl.idcolaborador].append(blcl)
        return render(request, 'pages/bloqueColaborador.html', {
            'current_page': 'registrar_bloques_colaboradores', 
            'bloques_por_colaborador':dict(bloques_por_colaborador), 
            'colaboradores': colaboradores, 
            'bloques': bloques,
            'selected_congreso': int(selected_congreso),
            'congresos': congresos
        })
    else:
        if not MaeColaborador.objects.filter(estado='ACTIVO').exists() or not MaeColaborador.objects.filter().exists():
            messages.warning(request, 'No hay colaboradores registrados o activos, registre al menos uno')
        elif not MaeBloque.objects.filter(estado='ACTIVO').exists() or not MaeBloque.objects.filter().exists():
            messages.warning(request, 'No hay bloques registrados o activos, registre al menos uno')
            
        bloquesToColaboradores = BloqueColaborador.objects.all().order_by('pk')
        congresos = MaeCongresoJinis.objects.all().order_by('pk')

        # Agrupar bloques por colaborador
        bloques_por_colaborador = defaultdict(list)
        for blcl in bloquesToColaboradores:
            bloques_por_colaborador[blcl.idcolaborador].append(blcl)
        return render(request, 'pages/bloqueColaborador.html', {
            'current_page': 'registrar_bloques_colaboradores', 
            'bloques_por_colaborador':dict(bloques_por_colaborador), 
            'selected_congreso': None,
            'congresos':congresos
        })