from django.db import models
from tipoDocumento.models import MaeTipodocumento
from Universidad.models import MaeUniversidad
from tipoParticipante.models import MaeTipoParticipante
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User

class MaeParticipantes(models.Model):
    codparticipante = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=10)
    apellido = models.CharField(max_length=20)
    email = models.CharField(max_length=35)
    idtipodoc = models.ForeignKey(MaeTipodocumento, models.DO_NOTHING, db_column='idtipodoc')
    iduniversidad = models.ForeignKey(MaeUniversidad, models.DO_NOTHING, db_column='iduniversidad')
    idtipo = models.ForeignKey(MaeTipoParticipante, models.DO_NOTHING, db_column='idtipo')

    class Meta:
        managed = False
        db_table = 'mae_participantes'

    def __str__(self) -> str:
        return self.codparticipante

# @receiver(post_save, sender=MaeParticipantes)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         user, created = User.objects.get_or_create(
#             username = instance.codparticipante,
#             defaults={
#                 'first_name': instance.nombre,
#                 'last_name': instance.apellido,
#                 'email': instance.email,
#             }
#         )
#         if created:
#             user.save()

















