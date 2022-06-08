from dataclasses import fields
import email
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from Aplicaciones.Inicio.models import Administrador, Area, DiaLaboral, Empleado, Empresa, FormularioDiario, FormularioSalud, ReporteDeContagio, ReporteDeFalta

class registroAdministradorForm(ModelForm):
    class Meta:
        model = Administrador
        fields = ['correo','password']


class registroAdministradorDatosEmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombregenerado']

class registroEmpleadoForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombregenerado', 'clave']

class registroEmpleado2Form(ModelForm):
    class Meta:
        model = Empleado
        fields = ['correo', 'password']


class registroEmpleado31Form(ModelForm):
    class Meta:
        model = Empleado
        fields = ['sexo', 'fechanacimiento']

        

class registroEmpleado4Form(ModelForm):
    class Meta:
        model = DiaLaboral
        fields = ['dia','horaentrada']


class registroSaludForm(ModelForm):
    class Meta:
        model = FormularioSalud
        fields = ['diabetes', 'epoc', 'asma', 'inmusupr', 'hiperten', 'vihsida', 'otracon', 'enfcardi', 'obesidad', 'insrencr', 'tabaquis', 'vacunado']

class formularioDiarioForm(ModelForm):
    class Meta:
        model = FormularioDiario
        fields = ['estaemba', 'mesesemb', 'fiebre', 'tos', 'odinogia', 'disnea', 'irritabi', 'diarrea', 'dotoraci', 'calofrios', 'cefalea', 'mialgias', 'artral', 'rinorrea', 'polipnea', 'vomito', 'dolabdo', 'conjun', 'cianosis', 'inisubis', 'conocaso', 'contaves', 'concerdo']

class reporteContagioForm(ModelForm):
    class Meta:
        model = ReporteDeContagio
        fields = ['respuesta', 'idempleado', 'nombre']
    
class reporteFaltaForm(ModelForm):
    class Meta:
        model = ReporteDeFalta
        fields = ['tipo', 'fechainiciofalta', 'fechafinfalta', 'comentario', 'idempleado', 'nombre']

class crearAreaForm(ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'descripcion', 'tipo']

class altaEmpleadosManualForm(ModelForm):
    class Meta:
        model = Empleado
        fields = ['correo']

class altaEmpleadosCSVForm(forms.Form):
    csv_upload = forms.FileField()
