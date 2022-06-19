# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from asyncio.constants import ACCEPT_RETRY_DELAY
from secrets import choice
from django.db import models

from COVID_WATCHER import settings


class Administrador(models.Model):
    idadmin = models.AutoField(db_column='idAdmin', primary_key=True)  # Field name made lowercase.
    correo = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'administrador'


class Empresa(models.Model):
    idempresa = models.AutoField(db_column='idEmpresa', primary_key=True)  # Field name made lowercase.
    nombregenerado = models.CharField(db_column='nombreGenerado', max_length=50, blank=True, null=True, unique=True)  # Field name made lowercase.
    idadmin = models.ForeignKey(Administrador, on_delete=models.CASCADE, db_column='idAdmin', blank=True, null=True, unique=False)  # Field name made lowercase.
    clave = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'


class Area(models.Model):
    idarea = models.AutoField(db_column='idArea', primary_key=True)  # Field name made lowercase.
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.CharField(db_column='tipo', max_length=50)  # Field name made lowercase.
    nombre = models.CharField(db_column='nombre', max_length=50)  # Field name made lowercase.
    idempresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='idEmpresa')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'area'

class DatosAlgoritmo(models.Model):
    idreg = models.AutoField(db_column='idReg', primary_key=True)  # Field name made lowercase.
    casospos = models.IntegerField(db_column='casospos')  # Field name made lowercase.
    casosneg = models.IntegerField(db_column='casosneg')  # Field name made lowercase.
    idarea = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='idArea')  # Field name made lowercase.
    fecha = models.DateField(db_column='fecha')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datos_algoritmo'

class Empleado(models.Model):
    idempleado = models.AutoField(db_column='idEmpleado', primary_key=True)  # Field name made lowercase.
    correo = models.CharField(max_length=50, blank=True, null=True, unique=True)
    password = models.CharField(max_length=50, blank=True, null=True)
    fechanacimiento = models.DateField(db_column='fechaNacimiento', blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(max_length=50, blank=True, null=True)
    idempresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='idEmpresa', blank=True, null=True)  # Field name made lowercase.
    idarea = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='idArea', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'empleado'

    def __str__(self):
        return str(self.idempleado)


class DiaLaboral(models.Model):
    iddialaboral = models.AutoField(db_column='idDiaLaboral', primary_key=True)  # Field name made lowercase.
    dia = models.CharField(max_length=100, blank=True, null=True)
    idempleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    horaentrada = models.TimeField(db_column='horaEntrada', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'dia_laboral'



class FormularioDiario(models.Model):
    idformulariodiario = models.AutoField(db_column='idFormularioDiario', primary_key=True)  # Field name made lowercase.
    idempleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    fechahora = models.DateTimeField()
    estaemba = models.CharField(max_length=50)
    mesesemb = models.CharField(max_length=50)
    fiebre = models.CharField(max_length=50)
    tos = models.CharField(max_length=50)
    odinogia = models.CharField(max_length=50)
    disnea = models.CharField(max_length=50)
    irritabi = models.CharField(max_length=50)
    diarrea = models.CharField(max_length=50)
    dotoraci = models.CharField(max_length=50)
    calofrios = models.CharField(max_length=50)
    cefalea = models.CharField(max_length=50)
    mialgias = models.CharField(max_length=50)
    artral = models.CharField(max_length=50)
    rinorrea = models.CharField(max_length=50)
    polipnea = models.CharField(max_length=50)
    vomito = models.CharField(max_length=50)
    dolabdo = models.CharField(max_length=50)
    conjun = models.CharField(max_length=50)
    cianosis = models.CharField(max_length=50)
    inisubis = models.CharField(max_length=50)
    conocaso = models.CharField(max_length=50)
    contaves = models.CharField(max_length=50)
    concerdo = models.CharField(max_length=50)


    class Meta:
        managed = False
        db_table = 'formulario_diario'

class FormularioSalud(models.Model):
    idformulariosalud = models.AutoField(db_column='idFormulario_salud', primary_key=True)  # Field name made lowercase.
    diabetes = models.CharField(max_length=50)
    epoc = models.CharField(max_length=50)
    asma = models.CharField(max_length=50)
    inmusupr = models.CharField(max_length=50)
    hiperten = models.CharField(max_length=50)
    vihsida = models.CharField(max_length=50)
    otracon = models.CharField(max_length=50)
    enfcardi = models.CharField(max_length=50)
    obesidad = models.CharField(max_length=50)
    insrencr = models.CharField(max_length=50)
    tabaquis = models.CharField(max_length=50)
    vacunado = models.CharField(max_length=50)
    idempleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'formulario_salud'



class ReporteDeContagio(models.Model):
    idreportedecontagio = models.IntegerField(db_column='idReporteDeContagio', primary_key=True)  # Field name made lowercase.
    respuesta = models.CharField(max_length=300, blank=True, null=True)
    idempleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    fechahora = models.DateTimeField()
    idarea = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='idArea', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reporte_de_contagio'


class ReporteDeFalta(models.Model):
    idreportedefalta = models.AutoField(db_column='idReporteDeFalta', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(max_length=50, blank=True, null=True)
    fechainiciofalta = models.DateField(db_column='fechaInicioFalta', blank=True, null=True)  # Field name made lowercase.
    fechafinfalta = models.DateField(db_column='fechaFinFalta', blank=True, null=True)  # Field name made lowercase.
    comentario = models.CharField(max_length=300, blank=True, null=True)
    idempleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, db_column='idEmpleado', blank=True, null=True)  # Field name made lowercase.
    fechahora = models.DateTimeField()
    idarea = models.ForeignKey(Area, on_delete=models.CASCADE, db_column='idArea', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reporte_de_falta'
    
    def __str__(self):
        return self.tipo