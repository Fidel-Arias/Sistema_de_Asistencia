from collections import defaultdict
from django.db.models import Prefetch
from django.shortcuts import render, redirect
from django.urls import reverse
from ..decorators import administrador_login_required
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from django.db import transaction
from adminMaestros.models import AdministradorBloquecolaborador, AdministradorCongreso, AdministradorColaborador, AdministradorBloques
from Admin.models import MaeAdministrador
from Bloque.models import MaeBloque
from Colaborador.models import MaeColaborador
from BloqueColaborador.models import BloqueColaborador
from Congreso.models import MaeCongreso
from django.contrib import messages

class Registrar_Bloques_Colaborador(viewsets.ViewSet):
    @method_decorator(administrador_login_required)
    def registrar_bloques_colaboradores(self, request, pk):
        if request.method == 'POST':
            colaborador = request.POST.get('colaborador')
            bloques = request.POST.getlist('bloques')
            action = request.POST.get('action')
            congreso = AdministradorCongreso.objects.get(idadministrador=pk)

            if action == 'register':
                try:
                    if (not(BloqueColaborador.objects.filter(idcolaborador=colaborador).exists())):
                        with transaction.atomic():
                            for i in range(0, len(bloques)):
                                nuevo_bloqueColaborador = BloqueColaborador(
                                    idcolaborador=MaeColaborador.objects.get(pk=colaborador),
                                    idbloque=MaeBloque.objects.get(pk=bloques[i]),
                                    idcongreso=MaeCongreso.objects.get(pk=congreso.idcongreso)
                                )
                                nuevo_bloqueColaborador.save()
                                admin_bloqueColaborador = AdministradorBloquecolaborador(
                                    idadministrador = AdministradorCongreso.objects.get(idadministrador = pk),
                                    idbc = nuevo_bloqueColaborador
                                )
                                admin_bloqueColaborador.save()
                            messages.success(request, 'Se registró exitosamente los bloques del colaborador')
                    else:
                        messages.error(request, 'Ya existe el colaborador con sus bloques')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o a los bloques')
                except Exception as e:    
                    messages.error(request, e) #unsupported operand type(s) for +: 'int' and 'str'
                return redirect(reverse('RegistrarBloqueColaborador', kwargs={'pk':pk}))
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
                return redirect(reverse('RegistrarBloqueColaborador', kwargs={'pk':pk}))
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
                return redirect(reverse('RegistrarBloqueColaborador', kwargs={'pk':pk}))
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
                                idcongreso=MaeCongreso.objects.get(pk=congreso.idcongreso)
                            )
                            nuevo_bloqueColaborador.save()
                        messages.success(request, 'Bloques del colaborador actualizado con éxito')
                except BloqueColaborador.DoesNotExist:
                    messages.error(request, 'No se encontró al colaborador o al bloque')
                return redirect(reverse('RegistrarBloqueColaborador', kwargs={'pk':pk}))
            
        else:
            if not AdministradorColaborador.objects.filter(idadministrador=pk).exists():
                messages.warning(request, 'No hay colaboradores registrados o activos, registre al menos uno')
            elif not AdministradorBloques.objects.filter(idadministrador=pk).exists():
                messages.warning(request, 'No hay bloques registrados o activos, registre al menos uno')
                
            colaboradores_activos = MaeColaborador.objects.filter(estado='ACTIVO')
            admin_colaboradores = MaeAdministrador.objects.prefetch_related(
                Prefetch('administradorcolaborador_set', queryset=AdministradorColaborador.objects.filter(idcolaborador__in = colaboradores_activos))
            ).filter(pk=pk)
            bloquesToColaboradores = BloqueColaborador.objects.all()
            bloques = MaeBloque.objects.filter(estado='ACTIVO').order_by('pk')

            # Agrupar bloques por colaborador
            bloques_por_colaborador = defaultdict(list)
            for blcl in bloquesToColaboradores:
                bloques_por_colaborador[blcl.idcolaborador].append(blcl)
            return render(request, 'pages/bloqueColaborador.html', {
                'current_page': 'registrar_bloques_colaboradores',
                'colaboradores_activos': colaboradores_activos,
                'admin_colaboradores': admin_colaboradores, 
                'bloques_por_colaborador':dict(bloques_por_colaborador),
                'bloques': bloques,
                'pk': pk
            })