import fileinput
import io
from itertools import chain
from multiprocessing import context
from pipes import Template
from pydoc import describe
import random
import re
import string
import os
from typing_extensions import Required
from urllib.parse import urlencode
from django.http import HttpRequest, HttpResponse
import datetime
#from datetime import datetime, timezone
from django.template import RequestContext, Template, Context
from django.template.loader import get_template
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from sklearn.multioutput import ClassifierChain
from Aplicaciones.Inicio.forms import altaEmpleadosCSVForm, altaEmpleadosManualForm, crearAreaForm, formularioDiarioForm, registroAdministradorDatosEmpresaForm, registroAdministradorForm, registroEmpleado2Form, registroEmpleado31Form, registroEmpleado4Form, registroEmpleadoForm, registroSaludForm, reporteContagioForm, reporteFaltaForm
from .models import *
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from reportlab.pdfgen import canvas
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from reportlab.lib.utils import ImageReader 
from django.db import transaction




# Create your views here.


def inicioMain(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    else:
        return render(request, 'Inicio.html', {})


def inicioAcerca(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    else:
        return render(request, 'acercaDe.html', {})

def guiaUsuario(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    else:
        return render(request, 'guiaUsuario.html', {})

def registroMain(request):
    request.session["registro"] = 1
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        return render(request, 'registroMain.html', {})
    else:
        return redirect('/')

def registroEmpleadoIntro(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        return render(request, 'registroEmpleadoIntro.html')
    else:
        return redirect('/')

def registroEmpleadoIntro2(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        if request.method == 'POST':
            return redirect('registroEmpleado')
        return render(request, 'registroEmpleadoIntro2.html')
    else:
        return redirect('/')

@transaction.atomic
def registroEmpleado(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        if request.method == 'POST':
            nombregenerado = request.POST.get('nombregenerado')
            clave = request.POST.get('clave')           
            try:
                user = Empresa.objects.get(nombregenerado=nombregenerado,clave=clave)
                print("Usuario:", user)
                return redirect('registroEmpleado2')

            except Empresa.DoesNotExist as e:
                messages.success(request, 'Nombre de empresa o clave incorrecta, inténtelo de nuevo')
        return render(request, 'registroEmpleadoEmpresa.html')
    else:
        return redirect('/')

@transaction.atomic
def registroEmpleado2(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        if request.method == 'POST':
            password = request.POST.get('password')
            correo = request.POST.get('correo')

            try:
                user = Empleado.objects.get(correo = correo)
                print(user.correo)
                if user.password:
                    print (user.password)
                    messages.success(request, 'Correo ya registrado, ingrese otro correo registrado por la empresa.')
                else:
                    user.password = password
                    user.save()
                    base_url = reverse('registroEmpleado3')
                    query_string = urlencode({'correo': correo})
                    url = '{}?{}'.format(base_url, query_string)
                    return redirect(url)
            except Empleado.DoesNotExist as e:
                messages.success(request, 'Correo no encontrado, inténtelo de nuevo')

        else:
            form = registroEmpleado2Form()
        
        context = {'form' : form}
        return render(request, 'registroEmpleado.html', context)
    else:
        return redirect('/')

@transaction.atomic
def registroEmpleado3(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        idempaux = request.GET.get('correo')
        if request.method == 'POST':
            form2 = registroEmpleado31Form(request.POST)
            if form2.is_valid():
                empid = Empleado.objects.get(correo = idempaux)
                cd2 = form2.cleaned_data
                empid.sexo = cd2['sexo']
                empid.fechanacimiento = cd2['fechanacimiento']
                empid.save()
                base_url = reverse('registroEmpleado4')
                query_string = urlencode({'correo': empid.correo})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
        else:
            form2 = registroEmpleado31Form()
        
        context = {'form2': form2}
        return render(request, 'registroEmpleadoDatos.html', context)
    else:
        return redirect('/')

@transaction.atomic
def registroEmpleado4(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        idempaux = request.GET.get('correo')
        if request.method == 'POST':
            form = registroEmpleado4Form(request.POST)
            dias = request.POST.getlist('dia')
            if form.is_valid():
                empid = Empleado.objects.get(correo = idempaux)
                cd = form.cleaned_data
                fnform = DiaLaboral()
                fnform.dia = dias
                fnform.horaentrada = cd['horaentrada'] 
                fnform.idempleado = empid
                fnform.save()
                base_url = reverse('registroEmpleado5')
                query_string = urlencode({'correo': empid.correo})
                url = '{}?{}'.format(base_url, query_string)
                #messages.success(request, f'Usuario creado')
                return redirect(url)
            else:
                print(form.errors)
        else:
            form = registroEmpleado4Form()
        
        context = {'form' : form}
        return render(request, 'registroEmpleadoHorarios.html', context)
    else:
        return redirect('/')

@transaction.atomic
def registroEmpleado5(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        idempaux = request.GET.get('correo')
        if request.method == 'POST':
            form = registroSaludForm(request.POST)
            if form.is_valid():
                empid = Empleado.objects.get(correo = idempaux)
                cd = form.cleaned_data
                fnform = FormularioSalud(diabetes = cd['diabetes'], epoc = cd['epoc'], asma = cd['asma'], inmusupr = cd['inmusupr'], hiperten = cd['hiperten'], vihsida = cd['vihsida'], otracon = cd['otracon'], enfcardi = cd['enfcardi'], obesidad = cd['obesidad'], insrencr = cd['insrencr'], tabaquis = cd['tabaquis'], vacunado = cd['vacunado'], idempleado = empid)
                fnform.save()
                messages.success(request, f'Usuario creado')
                return redirect('registro')
            else:
                print(form.errors)
        else:
            form = registroSaludForm()
        
        context = {'form' : form}
        return render(request, 'registroSalud.html', context)
    else:
        return redirect('/')

def inicioSesion(request):
    request.session["login"] = 1
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "login" in request.session:
        if request.method == 'POST':
                correo = request.POST.get('correo')
                password = request.POST.get('password')           
                try:
                    user = Empleado.objects.get(correo=correo,password=password)
                    print("Usuario:", user.idempleado)
                    request.session['idempleado']=user.idempleado
                    return redirect('menuEmpleado')
                        
                except Empleado.DoesNotExist as e:
                    try:
                        user = Administrador.objects.get(correo=correo,password=password)
                        print("Usuario:", user.idadmin)
                        request.session['idadmin']=user.idadmin
                        return redirect('menuAdmin')
                    except Administrador.DoesNotExist as e:
                        messages.success(request, 'Nombre de usuario o contraseña incorrecta, inténtelo de nuevo')
        
        return render(request, 'inicioSesion.html')
    else:
        return redirect('/')

def cierreSesion(request):
    if "idempleado" in request.session:
        del request.session['idempleado']
        return render(request, 'Inicio.html', {})
    elif "idadmin" in request.session:
        del request.session['idadmin']
        return render(request, 'Inicio.html', {})
    else:   
        return render(request, 'Inicio.html', {})

def registroAdministradorIntro(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        return render(request, 'registroAdministradorIntro.html')
    else:
        return redirect('/')

def registroAdministradorIntro2(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        if request.method == 'POST':
            return redirect('registroAdministrador')
        return render(request, 'registroAdministradorIntro2.html')
    else:
        return redirect('/')

@transaction.atomic
def registroAdministrador(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        if request.method == 'POST':
            administrador = registroAdministradorForm(request.POST)
            if administrador.is_valid():
                cd = administrador.cleaned_data
                adform = Administrador(correo = cd['correo'], password = cd['password'])
                adform.save()
                base_url = reverse('registroAdministradorDatos')
                query_string = urlencode({'correo': adform.correo})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
            else:
                print(administrador.errors)
        else:
            administrador = registroAdministradorForm()
        
        context = {'form' : administrador}
        return render(request, 'registroAdministrador.html', context)
    else:
        return redirect('/')

@transaction.atomic
def registroAdministradorDatos(request):
    if "idempleado" in request.session:
        return redirect('menuEmpleado')
    elif "idadmin" in request.session:
        return redirect('menuAdmin')
    elif "registro" in request.session:
        idadminaux = request.GET.get('correo')
        if request.method == 'POST':
            empresa = registroAdministradorDatosEmpresaForm(request.POST)
            if empresa.is_valid():
                adminid = Administrador.objects.get(correo = idadminaux)
                cd2 = empresa.cleaned_data
                clave=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
                adformDE = Empresa(nombregenerado = cd2['nombregenerado'], clave=clave, idadmin=adminid)
                messages.success(request, f'Usuario creado')
                adformDE.save()
                return redirect('registro')
            else:
                print(empresa.errors)
        else:
            empresa = registroAdministradorDatosEmpresaForm(request.POST)
        
        context = {'form2' : empresa}
        return render(request, 'registroAdministradorDatos.html', context)
    else:
        return redirect('/')

def menuEmpleado(request):
    try:
        idempaux = request.session["idempleado"]
        empid = FormularioSalud.objects.get(idempleado = idempaux)
        empnom = Empleado.objects.get(idempleado = idempaux)
        divi=re.split("@",empnom.correo)
        empnom=divi[0]
        emparea = Empleado.objects.select_related('idarea','idarea__idempresa').filter(idempleado = idempaux)
        nombarea = emparea[0].idarea.nombre
        emprenom = emparea[0].idarea.idempresa.nombregenerado
    except KeyError:
        return redirect('/')
    return render(request, 'menuEmpleado.html', {"empid": empid, 'empnom':empnom, 'nombarea':nombarea, 'emprenom':emprenom})

def menuAdmin(request):
    try:
        idadminaux = request.session["idadmin"]
        adminemp = Empresa.objects.get(idadmin = idadminaux)
        nomemp= adminemp.nombregenerado
        adminnom = Administrador.objects.get(idadmin = idadminaux)
        divi=re.split("@",adminnom.correo)
        adminnom=divi[0]
        adminid = Area.objects.filter(idempresa = adminemp)  
    except KeyError:
        return redirect('/') 
    return render(request, 'menuAdmin.html', {"adminid": adminid, 'adminnom':adminnom, 'nomemp':nomemp})

@transaction.atomic
def formularioDiario(request):
    try:
        idempaux = request.session["idempleado"]
        if request.method == 'POST':
            try:
                FormularioDiario.objects.get(idempleado = idempaux, fechahora__date = datetime.datetime.now().strftime('%Y-%m-%d'))
                messages.success(request, f'Ya registraste tu respuesta del dia.')
                return redirect('menuEmpleado')
            except FormularioDiario.DoesNotExist:
                form = formularioDiarioForm(request.POST)
                if form.is_valid():
                    empid = Empleado.objects.get(idempleado = idempaux)
                    cd = form.cleaned_data
                    fnform = FormularioDiario(estaemba = cd['estaemba'], mesesemb = cd['mesesemb'], fiebre = cd['fiebre'], tos = cd['tos'], odinogia = cd['odinogia'], disnea = cd['disnea'], irritabi = cd['irritabi'], diarrea = cd['diarrea'], dotoraci = cd['dotoraci'], calofrios = cd['calofrios'], cefalea = cd['cefalea'], mialgias = cd['mialgias'], artral = cd['artral'], rinorrea = cd['rinorrea'], polipnea = cd['polipnea'], vomito = cd['vomito'], dolabdo = cd['dolabdo'], conjun = cd['conjun'], cianosis = cd['cianosis'], inisubis = cd['inisubis'], conocaso = cd['conocaso'], contaves = cd['contaves'], concerdo = cd['concerdo'], idempleado = empid)
                    fnform.save()
                    messages.success(request, f'Respuesta registrada, ¡muchas gracias!')
                    return redirect('menuEmpleado')
                else:
                    print(form.errors)
        else:
            form = formularioDiarioForm()
    except KeyError:
        return redirect('/') 
    return render(request, 'formularioDiario.html', {})

@transaction.atomic
def reporteContagio(request):
    try:
        idempaux = request.session["idempleado"]
        if request.method == 'POST':
            form = reporteContagioForm(request.POST)
            if form.is_valid():
                empid = Empleado.objects.get(idempleado = idempaux)
                cd = form.cleaned_data
                fnform = ReporteDeContagio(respuesta = cd['respuesta'], idempleado = empid, nombre = cd['nombre'], idarea = empid.idarea)
                fnform.save()
                messages.success(request, f'Respuesta registrada, ¡muchas gracias!')
                return redirect('menuEmpleado')
            else:
                print(form.errors)
        else:
            form = reporteContagioForm()
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaCOVID.html', {})

@transaction.atomic
def reporteFalta(request):
    try:
        idempaux = request.session["idempleado"]
        if request.method == 'POST':
            form = reporteFaltaForm(request.POST)
            if form.is_valid():
                empid = Empleado.objects.get(idempleado = idempaux)
                cd = form.cleaned_data
                fnform = ReporteDeFalta(tipo = cd['tipo'], fechainiciofalta = cd['fechainiciofalta'], fechafinfalta = cd['fechafinfalta'], comentario = cd['comentario'], nombre = cd['nombre'], idempleado = empid, idarea = empid.idarea)
                fnform.save()
                messages.success(request, f'Respuesta registrada, ¡muchas gracias!')
                return redirect('menuEmpleado')
            else:
                print(form.errors)
        else:
            form = reporteFaltaForm()
    except KeyError:
        return redirect('/')   
    return render(request, 'alertaFalta.html', {})

@transaction.atomic
def cambiarDatos(request):
    try:
        idempaux = request.session["idempleado"]
        if request.method == 'POST':
            empid = FormularioSalud.objects.get(idempleado = idempaux)
            if request.POST.get('diabetes'):
                empid.diabetes = request.POST.get('diabetes')
            if request.POST.get('epoc'):
                empid.epoc = request.POST.get('epoc')
            if request.POST.get('asma'): 
                empid.asma = request.POST.get('asma') 
            if request.POST.get('inmusupr'):
                empid.inmusupr = request.POST.get('inmusupr') 
            if request.POST.get('hiperten'):
                empid.hiperten = request.POST.get('hiperten') 
            if request.POST.get('vihsida'):
                empid.vihsida = request.POST.get('vihsida') 
            if request.POST.get('otracon'):
                empid.otracon = request.POST.get('otracon') 
            if request.POST.get('enfcardi'):
                empid.enfcardi = request.POST.get('enfcardi') 
            if request.POST.get('obesidad'):
                empid.obesidad = request.POST.get('obesidad') 
            if request.POST.get('insrencr'):
                empid.insrencr = request.POST.get('insrencr') 
            if request.POST.get('tabaquis'):
                empid.tabaquis = request.POST.get('tabaquis')
            if request.POST.get('conanima'):
                empid.conanima = request.POST.get('conanima')
            if request.POST.get('vacunado'):
                empid.vacunado = request.POST.get('vacunado')
            empid.save()
            messages.success(request, f'Cambios realizados')
            return redirect('menuEmpleado')
    except KeyError:
        return redirect('/')   
    context = {}
    return render(request, 'registroSaludModif.html', context)

@transaction.atomic
def crearArea(request):
    try:
        idadminaux = request.session["idadmin"]
        if request.method == 'POST':
            form = crearAreaForm(request.POST)
            if form.is_valid():
                adminid = Empresa.objects.get(idadmin = idadminaux)
                cd = form.cleaned_data
                fnform = Area(nombre = cd['nombre'], idempresa = adminid, descripcion = cd['descripcion'], tipo = cd['tipo'])
                fnform.save()
                messages.success(request, f'Area creada')
                return redirect('menuAdmin')
            else:
                print(form.errors)
        else:
            form = crearAreaForm()
    except KeyError:
        return redirect('/')  
    return render(request, 'crearArea.html', {})

@transaction.atomic
def altaEmpleadosManual(request):
    try:
        idadminaux = request.GET.get('id')
        idadminsesion = request.session["idadmin"]
        if request.method == 'POST':
            form = altaEmpleadosManualForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                empresa = Empresa.objects.get(idadmin = idadminsesion)
                areafn = Area.objects.get(idarea = idadminaux)
                fnform = Empleado(correo = cd['correo'], idempresa = empresa, idarea = areafn)
                fnform.save()
                empid = Empleado.objects.get(correo = cd['correo'])
                correoin = cd['correo']
                adminemp = Empresa.objects.get(idadmin = idadminsesion)
                nombre = adminemp.nombregenerado
                clave = adminemp.clave
                send_mail(
                    'Datos de acceso a COVID Watcher',
                    'Estimado usuario: \nA continuacion se encuentran adjuntos los datos de acceso.\nNombre de la empresa: '+ nombre + '\nClave de la empresa: '+ clave,
                    settings.EMAIL_HOST_USER,
                    [correoin],
                    fail_silently=False
                )
                messages.success(request, f'Usuarios dados de alta')
                return render(request, 'altaEmpleadosManual.html')
            else:
                print(form.errors)
        else:
            form = altaEmpleadosManualForm()
    except KeyError:
        return redirect('/')  
    return render(request, 'altaEmpleadosManual.html', {})

@transaction.atomic
def altaEmpleadosCSV(request):
    try:
        idadminaux = request.GET.get('id')
        idadminsesion = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminsesion)
        areafn = Area.objects.get(idarea = idadminaux)
        print(idadminaux)
        if request.method == 'POST':
            form = altaEmpleadosCSVForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_upload']
                if not csv_file.name.endswith('.csv'):
                    messages.warning(request, 'Tipo de archivo incorrecto')
                    return render(request, 'altaEmpleadosCSV.html')
                file_data = csv_file.read().decode("utf-8")
                csv_data = file_data.split("\n")
                for x in csv_data:
                    if x == '':
                        print("Espacio en blanco")
                    else:
                        fields = x.split(",")
                        created = Empleado.objects.update_or_create(
                            correo = fields[0], idempresa = empresa, idarea = areafn
                        )
                        adminid = Empleado.objects.get(correo = fields[0])
                        adminid.correo=adminid.correo.replace('\r', '')
                        empArea = Area.objects.get(idarea=idadminaux)
                        adminid.save()

                        correoin = adminid.correo
                        idadminsesion = request.session["idadmin"]
                        adminemp = Empresa.objects.get(idadmin = idadminsesion)
                        nombre = adminemp.nombregenerado
                        clave = adminemp.clave

                        send_mail(
                            'Datos de acceso a COVID Watcher',
                            'Estimado usuario: \nA continuacion se encuentran adjuntos los datos de acceso.\nNombre de la empresa: '+ nombre + '\nClave de la empresa: '+ clave,
                            settings.EMAIL_HOST_USER,
                            [correoin],
                            fail_silently=False
                        )

                messages.success(request, f'Usuarios dados de alta')
                return redirect('menuAdmin')
            else:
                print(form.errors)
        else:
            form = altaEmpleadosCSVForm()
    except KeyError:
        return redirect('/')   
    
    return render(request, 'altaEmpleadosCSV.html')

@transaction.atomic
def altaEmpleados(request):
    try:
        idadminsesion = request.session["idadmin"]
        if request.GET.get('id'):
            idadminaux = request.GET.get('id')
        context = {'idadminaux' : idadminaux}
    except KeyError:
        return redirect('/') 
    return render(request, 'altaEmpleados.html', context)

def alertaFaltasReporte(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora')
        for reportes in adminreport:
            reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
            reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
            reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaFaltasReporte.html', {'adminreport':adminreport})

def alertaFaltasReportePDF(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=hello.pdf'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize='A4')
        p.setLineWidth(.3)
        p.setFont('Helvetica', 22)
        p.drawString(30,750,'COVID Watcher')
        p.setFont('Helvetica', 12)
        p.drawString(30,735,'Reporte de faltas')
        p.drawString(30,720,'')
        p.setFont('Helvetica-Bold', 12)
        fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
        p.drawString(480,750,fechahoy)
        aux=720
        for reportes in adminreport:
            reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
            reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
            reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,aux-15,'Tipo: '+reportes.tipo)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-30,'Nombre: '+reportes.nombre)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-45,'Correo: '+reportes.idempleado.correo)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-60,'Area: '+reportes.idarea.nombre)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-75,'Fecha de inicio de falta: '+reportes.fechainiciofalta)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-90,'Fecha de fin de falta: '+reportes.fechafinfalta)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-105,'Comentario adicional: '+reportes.comentario)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-120,'Fecha de emision: '+reportes.fechahora)
            aux-=135
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    except KeyError:
        return redirect('/') 

def alertaFaltasReporteDia(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        if request.method == 'POST':
            fecha = request.POST.get('fechafiltro')
            if fecha == '':
                messages.error(request, f'Por favor elija una fecha')
                return redirect('alertaFaltasReporteDia')
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(fechahora__date=fecha,idarea__idempresa=empresa).order_by('-fechahora')
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
            request.session['fecha'] = fecha
        else: 
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora__day')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaFaltasReporteDia.html', {'adminreport':adminreport})

def alertaFaltasReporteDiaPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fecha = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(fechahora__date=fecha,idarea__idempresa=empresa).order_by('-fechahora')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=hello.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de faltas del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            aux=720
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Tipo: '+reportes.tipo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,'Nombre: '+reportes.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-45,'Correo: '+reportes.idempleado.correo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Area: '+reportes.idarea.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Fecha de inicio de falta: '+reportes.fechainiciofalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-90,'Fecha de fin de falta: '+reportes.fechafinfalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-105,'Comentario adicional: '+reportes.comentario)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-120,'Fecha de emision: '+reportes.fechahora)
                aux-=135
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('alertaFaltasReporteDia')
        return response
    except KeyError:
        return redirect('/') 

def alertaFaltasReporteMes(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        if request.method == 'POST':
            fecha = request.POST.get('fechafiltro')
            if fecha == '':
                messages.error(request, f'Por favor elija una fecha')
                return redirect('alertaFaltasReporteMes')
            fechames=fecha[-2:]
            fechaaño=fecha[0:4]
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(fechahora__month=fechames, fechahora__year=fechaaño, idarea__idempresa=empresa).order_by('-fechahora')
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
            request.session['fecha'] = fecha
        else:
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora__month')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaFaltasReporteMes.html', {'adminreport':adminreport})

def alertaFaltasReporteMesPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fecha = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            fechames=fecha[-2:]
            fechaaño=fecha[0:4]
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(fechahora__month=fechames, fechahora__year=fechaaño, idarea__idempresa=empresa).order_by('-fechahora')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=hello.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de faltas del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            aux=720
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Tipo: '+reportes.tipo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,'Nombre: '+reportes.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-45,'Correo: '+reportes.idempleado.correo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Area: '+reportes.idarea.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Fecha de inicio de falta: '+reportes.fechainiciofalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-90,'Fecha de fin de falta: '+reportes.fechafinfalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-105,'Comentario adicional: '+reportes.comentario)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-120,'Fecha de emision: '+reportes.fechahora)
                aux-=135
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('alertaFaltasReporteMes')
        return response
    except KeyError:
        return redirect('/') 

def alertaFaltasReporteTipo(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        if request.method == 'POST':
            tipoaux = request.POST.get('tipo')
            print(tipoaux)
            if tipoaux == 'Seleccione una opcion':
                messages.error(request, f'Por favor elija un tipo')
                return redirect('alertaFaltasReporteTipo')
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(tipo=tipoaux,idarea__idempresa=empresa).order_by('-fechahora')
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
            request.session['tipoaux'] = tipoaux
        else:
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaFaltasReporteTipo.html', {'adminreport':adminreport})

def alertaFaltasReporteTipoPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'tipoaux' in request.session:
            tipoaux = request.session["tipoaux"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            adminreport = ReporteDeFalta.objects.select_related('idempleado','idarea').filter(tipo=tipoaux,idarea__idempresa=empresa).order_by('-fechahora')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=hello.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de faltas de '+tipoaux)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            aux=720
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                reportes.fechainiciofalta=reportes.fechainiciofalta.strftime('%m/%d/%Y')
                reportes.fechafinfalta=reportes.fechafinfalta.strftime('%m/%d/%Y')
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Tipo: '+reportes.tipo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,'Nombre: '+reportes.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-45,'Correo: '+reportes.idempleado.correo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Area: '+reportes.idarea.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Fecha de inicio de falta: '+reportes.fechainiciofalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-90,'Fecha de fin de falta: '+reportes.fechafinfalta)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-105,'Comentario adicional: '+reportes.comentario)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-120,'Fecha de emision: '+reportes.fechahora)
                aux-=135
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['tipoaux']
        else:
            messages.error(request, f'Por favor elija un tipo')
            return redirect('alertaFaltasReporteTipo')
        return response
    except KeyError:
        return redirect('/') 

def alertaCOVIDReporte(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora')
        for reportes in adminreport:
            reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaCOVIDReporte.html', {'adminreport':adminreport})

def alertaCOVIDReportePDF(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=hello.pdf'
        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize='A4')
        p.setLineWidth(.3)
        p.setFont('Helvetica', 22)
        p.drawString(30,750,'COVID Watcher')
        p.setFont('Helvetica', 12)
        p.drawString(30,735,'Reporte de posibles contagios')
        p.drawString(30,720,'')
        p.setFont('Helvetica-Bold', 12)
        fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
        p.drawString(480,750,fechahoy)
        aux=720
        for reportes in adminreport:
            reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,aux-15,'Nombre: '+reportes.nombre)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-30,'Correo: '+reportes.idempleado.correo)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-45,'Area: '+reportes.idarea.nombre)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-60,'Fecha de emision: '+reportes.fechahora)
            p.setFont('Helvetica', 10)
            p.drawString(30,aux-75,'Comentario: '+reportes.respuesta)
            aux-=90
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    except KeyError:
        return redirect('/') 

def alertaCOVIDReporteDia(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        if request.method == 'POST':
            fecha = request.POST.get('fechafiltro')
            if fecha == '':
                messages.error(request, f'Por favor elija una fecha')
                return redirect('alertaCOVIDReporteDia')
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(fechahora__date=fecha,idarea__idempresa=empresa).order_by('-fechahora')
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
            request.session['fecha'] = fecha
        else: 
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora__day')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaCOVIDReporteDia.html', {'adminreport':adminreport})

def alertaCOVIDReporteDiaPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fecha = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(fechahora__date=fecha,idarea__idempresa=empresa).order_by('-fechahora')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=hello.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de posibles contagios del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            aux=720
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Nombre: '+reportes.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,'Correo: '+reportes.idempleado.correo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-45,'Area: '+reportes.idarea.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Fecha de emision: '+reportes.fechahora)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Comentario: '+reportes.respuesta)
                aux-=90
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('alertaCOVIDReporteDia')
        return response
    except KeyError:
        return redirect('/') 

def alertaCOVIDReporteMes(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        if request.method == 'POST':
            fecha = request.POST.get('fechafiltro')
            if fecha == '':
                messages.error(request, f'Por favor elija una fecha')
                return redirect('alertaCOVIDReporteMes')
            fechames=fecha[-2:]
            fechaaño=fecha[0:4]
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(fechahora__month=fechames, fechahora__year=fechaaño, idarea__idempresa=empresa).order_by('-fechahora')
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
            request.session['fecha'] = fecha
        else:
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(idarea__idempresa=empresa).order_by('-fechahora__month')
    except KeyError:
        return redirect('/') 
    return render(request, 'alertaCOVIDReporteMes.html', {'adminreport':adminreport})

def alertaCOVIDReporteMesPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fecha = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            fechames=fecha[-2:]
            fechaaño=fecha[0:4]
            adminreport = ReporteDeContagio.objects.select_related('idempleado','idarea').filter(fechahora__month=fechames, fechahora__year=fechaaño, idarea__idempresa=empresa).order_by('-fechahora')
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=hello.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de posibles contagios del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            aux=720
            for reportes in adminreport:
                reportes.fechahora=reportes.fechahora.strftime('%m/%d/%Y, %H:%M %p')
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Nombre: '+reportes.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,'Correo: '+reportes.idempleado.correo)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-45,'Area: '+reportes.idarea.nombre)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Fecha de emision: '+reportes.fechahora)
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Comentario: '+reportes.respuesta)
                aux-=90
            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('alertaCOVIDReporteMes')
        return response
    except KeyError:
        return redirect('/') 

@transaction.atomic
def procDatos(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        dataset = pd.read_csv('C:\\Users\\crist\\Documents\\COVID_WATCHER\\sintomasID3.csv', encoding='latin-1')
        X = dataset.iloc[:, [0,1,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]].values
        y = dataset.iloc[:, -1].values

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)

        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        classifier.fit(X_train, y_train)

        y_pred = classifier.predict(X_test)
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)
        #print(cm)
        fecha=datetime.date.today()
        emp = Empleado.objects.filter(idempresa=empresa)
        empn = Empleado.objects.filter(idempresa=empresa).count()
        empnofaux = 0
        for emps in emp:
            try:
                FormularioDiario.objects.get(idempleado=emps.idempleado, fechahora__date=fecha)
            except FormularioDiario.DoesNotExist:
                empnofaux+=1 
        print(empnofaux)
        arean = Area.objects.filter(idempresa=empresa).count()
        arealist = Area.objects.filter(idempresa=empresa)
        lista = [[] for i in range(empn)]
        temp = [[] for i in range(empn)]
        respos = []
        resneg = []
        resgen = []
        areas = []
        areafn = []
        arealistfn = []
        arealistnomb = []
        empnoform = [[] for i in range(empnofaux)]
        arearesgen = [[] for i in range(arean)]
        x = 0
        p = 0
        for elem in emp:
            if not FormularioDiario.objects.select_related('idempleado').filter(fechahora__date=fecha, idempleado__idempresa=empresa, idempleado = elem):
                empnoform[p].append(elem.correo)
                empnoform[p].append(elem.idarea.nombre)
                horarios = DiaLaboral.objects.get(idempleado = elem.idempleado)
                horarios.dia = str(horarios.dia)[1:-1]
                horarios.dia = horarios.dia.replace("'","")
                empnoform[p].append(horarios.dia)
                empnoform[p].append(horarios.horaentrada)
                p+=1
                continue
            else:
                datos1 = FormularioDiario.objects.select_related('idempleado').filter(fechahora__date=fecha, idempleado__idempresa=empresa, idempleado = elem)
                for dato in datos1:
                    today = datetime.date.today()
                    edad = today.year - dato.idempleado.fechanacimiento.year - ((today.month, today.day) < (dato.idempleado.fechanacimiento.month, dato.idempleado.fechanacimiento.day))
                    lista[x].append(dato.idempleado.sexo)
                    lista[x].append(edad)
                    lista[x].append(dato.estaemba)
                    lista[x].append(dato.mesesemb)
                    lista[x].append(dato.fiebre)
                    lista[x].append(dato.tos)
                    lista[x].append(dato.odinogia)
                    lista[x].append(dato.disnea)
                    lista[x].append(dato.irritabi)
                    lista[x].append(dato.diarrea)
                    lista[x].append(dato.dotoraci)
                    lista[x].append(dato.calofrios)
                    lista[x].append(dato.cefalea)
                    lista[x].append(dato.mialgias)
                    lista[x].append(dato.artral)
                    lista[x].append(dato.rinorrea)
                    lista[x].append(dato.polipnea)
                    lista[x].append(dato.vomito)
                    lista[x].append(dato.dolabdo)
                    lista[x].append(dato.conjun)
                    lista[x].append(dato.cianosis)
                    lista[x].append(dato.inisubis)
                    lista[x].append(dato.conocaso)
                    lista[x].append(dato.contaves)
                    lista[x].append(dato.concerdo)
                    areas.append(dato.idempleado.idarea)
                datos2 = FormularioSalud.objects.select_related('idempleado').filter(idempleado__idempresa=empresa, idempleado = elem)
                for dato2 in datos2:
                    lista[x].append(dato2.diabetes)
                    lista[x].append(dato2.epoc)
                    lista[x].append(dato2.asma)
                    lista[x].append(dato2.inmusupr)
                    lista[x].append(dato2.hiperten)
                    lista[x].append(dato2.vihsida)
                    lista[x].append(dato2.otracon)
                    lista[x].append(dato2.enfcardi)
                    lista[x].append(dato2.obesidad)
                    lista[x].append(dato2.insrencr)
                    lista[x].append(dato2.tabaquis)
                    lista[x].append(dato2.vacunado)

                for i in lista[x]:
                    
                    if i == 'Si':
                        temp[x].append(int(1))
                    else:
                        if i=='No':
                            temp[x].append(int(0))
                        else:
                            if i=='Masculino':
                                temp[x].append(int(1))
                            else:
                                if i=='Femenino':
                                    temp[x].append(int(0))
                                else:
                                    temp[x].append(int(-1))
            
                temp[x][1]=int(lista[x][1])
                if temp[x][2]==1:
                    temp[x][3]=int(lista[x][3])


                tempfn = np.array(temp[x])
                tempfn=tempfn.reshape(1,37)
                tempfn = sc.transform(tempfn)
                fin = classifier.predict(tempfn)
                #print(fin)
                if fin == 0:
                    #print("Negativo")
                    resneg.append(1)
                    resgen.append(0)
                    #areafn.append()
                else:
                    #print("Positivo")
                    respos.append(1)
                    resgen.append(1)
                

                x+=1
        if empnoform:
            messages.error(request, str(int(len(empnoform)))+' empleados no han contestado el formulario diario.')
        print(empnoform)

        y = 0
        for i in areas:
            areafn.append(areas[y].idarea)
            y+=1
        w = 0

        for ar in arealist:
            arealistfn.append(ar.idarea)
            arealistnomb.append(ar.nombre)
            w+=1
        
        z = 0
        c = 0
        
        for r in arearesgen:
            for s in areafn:
                if s == arealistfn[c]:
                    arearesgen[c].append(resgen[z])
                z+=1
            z=0
            c+=1
        


        print(arean)
        print(resgen)   
        print(arealistfn)    
        print(areafn)
        print(arearesgen)
        posarea = []
        poscatter = []
        nombscatter = []
        b = 0
        datosareas = [[] for i in range(arean)]
        for i in arearesgen:
            poscount = arearesgen[b].count(1)
            datosareas[b].append(poscount)
            posarea.append(poscount)
            negcount = arearesgen[b].count(0)
            datosareas[b].append(negcount)
            totalcont = poscount+negcount
            if(totalcont == 0):
                datosareas[b].append(0)
                datosareas[b].append(0)
                datosareas[b].append(arealist[b].nombre)
                try:
                    datalg = DatosAlgoritmo.objects.get(idarea = arealist[b], fecha = datetime.datetime.today(), idarea__idempresa = empresa)
                    datalg.casospos = poscount 
                    datalg.casosneg=negcount
                    datalg.save()
                except DatosAlgoritmo.DoesNotExist:
                    datosalg = DatosAlgoritmo(casospos=poscount, casosneg=negcount, idarea=arealist[b], fecha = datetime.datetime.today())
                    datosalg.save()
                b+=1
                continue
            datosareas[b].append(totalcont)
            porpos = (poscount/totalcont)*100
            porpos=round(porpos, 2)
            datosareas[b].append(porpos)
            datosareas[b].append(arealist[b].nombre)
            try:
                datalgfn = DatosAlgoritmo.objects.get(idarea = arealist[b], fecha = datetime.datetime.today(), idarea__idempresa = empresa)
                datalgfn.casospos=poscount
                datalgfn.casosneg=negcount
                datalgfn.save()
            except DatosAlgoritmo.DoesNotExist:
                datosalg = DatosAlgoritmo(casospos=poscount, casosneg=negcount, idarea=arealist[b], fecha = datetime.datetime.today())
                datosalg.save()
            b+=1
        #print(datosareas)
        numneg=len(resneg)
        numpos=len(respos)
        posaux = 0
        postec = 0
        poscom = 0
        posfin = 0
        posseg = 0
        poscon = 0
        posadm = 0
        datostipos = []
        datostiposnom = []
        datostiposfn = []

        try:
            tipo=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.today(), idarea__idempresa = empresa)
            for dato in tipo:
                if dato.idarea.tipo == 'Tecnicas':
                    postec = postec + dato.casospos
                elif dato.idarea.tipo == 'Comerciales':
                    poscom = poscom + dato.casospos
                elif dato.idarea.tipo == 'Financieras':
                    posfin = posfin + dato.casospos
                elif dato.idarea.tipo == 'Seguridad':
                    posseg = posseg + dato.casospos
                elif dato.idarea.tipo == 'Contables':
                    poscon = poscon + dato.casospos
                elif dato.idarea.tipo == 'Administrativas':
                    posadm = posadm + dato.casospos
            datostipos.append(postec)
            datostipos.append(poscom)
            datostipos.append(posfin)
            datostipos.append(posseg)
            datostipos.append(poscon)
            datostipos.append(posadm)
            datostiposnom.append("Tecnicas")
            datostiposnom.append("Comerciales")
            datostiposnom.append("Financieras")
            datostiposnom.append("Seguridad")
            datostiposnom.append("Contables")
            datostiposnom.append("Administrativas")
            if datostipos.index(max(datostipos))==0:
                datostiposfn.append("Tecnicas")
                datostiposfn.append(postec)
            elif datostipos.index(max(datostipos))==1:
                datostiposfn.append("Comerciales")
                datostiposfn.append(poscom)
            elif datostipos.index(max(datostipos))==2:
                datostiposfn.append("Financieras")
                datostiposfn.append(posfin)
            elif datostipos.index(max(datostipos))==3:
                datostiposfn.append("Seguridad")
                datostiposfn.append(posseg)
            elif datostipos.index(max(datostipos))==4:
                datostiposfn.append("Contables")
                datostiposfn.append(poscon)
            elif datostipos.index(max(datostipos))==5:
                datostiposfn.append("Administrativas")
                datostiposfn.append(posadm)

            if datostipos.index(min(datostipos))==0:
                datostiposfn.append("Tecnicas")
                datostiposfn.append(postec)
            elif datostipos.index(min(datostipos))==1:
                datostiposfn.append("Comerciales")
                datostiposfn.append(poscom)
            elif datostipos.index(min(datostipos))==2:
                datostiposfn.append("Financieras")
                datostiposfn.append(posfin)
            elif datostipos.index(min(datostipos))==3:
                datostiposfn.append("Seguridad")
                datostiposfn.append(posseg)
            elif datostipos.index(min(datostipos))==4:
                datostiposfn.append("Contables")
                datostiposfn.append(poscon)
            elif datostipos.index(min(datostipos))==5:
                datostiposfn.append("Administrativas")
                datostiposfn.append(posadm)
        except DatosAlgoritmo.DoesNotExist:
            print("ERROR") 

        print(datostipos)
        print(datostiposfn)
        
        try:
            for i in range(7):
                ayer=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.today()- datetime.timedelta(days = i), idarea__idempresa = empresa)
                for dato in ayer:
                    posaux = posaux + dato.casospos
                fechaform=(datetime.datetime.today()-datetime.timedelta(days = i)).strftime('%d/%m')
                nombscatter.append(fechaform)
                poscatter.append(posaux)
                posaux=0
        except DatosAlgoritmo.DoesNotExist:
            print("ERROR") 
        auxfor=0
        posmonth=[]
        nombmonth=[]
        try:
            mesalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.now().month, idarea__idempresa = empresa).order_by('idreg')
            for i in mesalg:
                posaux = posaux + i.casospos
                auxfor+=1
                if auxfor==arean:
                    posmonth.append(posaux)
                    fechaform=i.fecha.strftime('%d/%m/%Y')
                    nombmonth.append(fechaform)
                    posaux=0
                    auxfor=0
                
                
                
        except DatosAlgoritmo.DoesNotExist:
            print("ERROR") 
        
    except KeyError:
        return redirect('/') 
    
    return render(request, 'resultadosAlg.html', {'numneg':numneg, 'numpos':numpos, 'datosareas':datosareas, 'posarea':posarea,'arealistnomb':arealistnomb, 'poscatter':poscatter, 'nombscatter':nombscatter, 'posmonth':posmonth, 'nombmonth':nombmonth, 'datostiposfn':datostiposfn, 'datostipos':datostipos, 'datostiposnom':datostiposnom, 'empnoform':empnoform})


def historialRes(request):
    try:
        idadminaux = request.session["idadmin"]
    except KeyError:
        return redirect('/') 
    return render(request, 'historialRes.html')

def historialResDia(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        arean = Area.objects.filter(idempresa=empresa).count()
        arealist = Area.objects.filter(idempresa=empresa)
        emp = Empleado.objects.filter(idempresa=empresa)
        print(arean)
        arealistfn = []
        arealistnomb = []
        totalemppos = 0
        totalempneg = 0
        nombscatter=[]
        poscatter=[]
        posmonth=[]
        nombmonth=[]
        datosareas = [[] for i in range(arean)]
        posarea=[]
        b = 0
        posaux=0
        datossi=0

        postec = 0
        poscom = 0
        posfin = 0
        posseg = 0
        poscon = 0
        posadm = 0
        datostipos = []
        datostiposnom = []
        datostiposfn = []
        empnofaux = 0
        empnoform = []
        



        if request.method == 'POST':
            fechaget = request.POST.get('fechafiltro')
            if fechaget == '' or not DatosAlgoritmo.objects.filter(fecha = datetime.datetime.strptime(fechaget, '%Y-%m-%d'), idarea__idempresa = empresa):
                messages.error(request, f'Por favor elija una fecha valida.')
                return redirect('historialResDia')

            for emps in emp:
                try:
                    FormularioDiario.objects.get(idempleado=emps.idempleado, fechahora__date=datetime.datetime.strptime(fechaget, '%Y-%m-%d'))
                except FormularioDiario.DoesNotExist:
                    empnofaux+=1 
            empnoform = [[] for i in range(empnofaux)]

            p=0
            for elem in emp:
                if not FormularioDiario.objects.select_related('idempleado').filter(fechahora__date=datetime.datetime.strptime(fechaget, '%Y-%m-%d'), idempleado__idempresa=empresa, idempleado = elem):
                    empnoform[p].append(elem.correo)
                    empnoform[p].append(elem.idarea.nombre)
                    horarios = DiaLaboral.objects.get(idempleado = elem.idempleado)
                    horarios.dia = str(horarios.dia)[1:-1]
                    horarios.dia = horarios.dia.replace("'","")
                    empnoform[p].append(horarios.dia)
                    empnoform[p].append(horarios.horaentrada)
                    p+=1

            for ar in arealist:
                arealistfn.append(ar.idarea)
                arealistnomb.append(ar.nombre)
                resalg = DatosAlgoritmo.objects.filter(idarea=ar.idarea, fecha=fechaget, idarea__idempresa = empresa).order_by('idreg')
                for n in resalg:
                    print(n)
                    totalemppos+=n.casospos
                    totalempneg+=n.casosneg
            try:
                for i in range(7):
                    ayer=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fechaget, '%Y-%m-%d') - datetime.timedelta(days = i), idarea__idempresa = empresa)
                    for x in ayer:
                        posaux += x.casospos
                    fechaform=(datetime.datetime.strptime(fechaget, '%Y-%m-%d')-datetime.timedelta(days = i)).strftime('%d/%m')
                    nombscatter.append(fechaform)
                    poscatter.append(posaux)
                    posaux=0
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            
            auxfor=0
            try:
                mesalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m-%d').month, idarea__idempresa = empresa).order_by('idreg')
                #print(mesalg)
                for i in mesalg:
                    posaux = posaux + i.casospos
                    auxfor+=1
                    if auxfor==arean:
                        posmonth.append(posaux)
                        fechaform=i.fecha.strftime('%d/%m/%Y')
                        nombmonth.append(fechaform)
                        posaux=0
                        auxfor=0                        
                    
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            b=0
            print(arealistfn)
            for r in arealistfn:
                
                if DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fechaget, '%Y-%m-%d'), idarea__idempresa = empresa, idarea=r).order_by('idreg').exists():
                    resalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fechaget, '%Y-%m-%d'), idarea__idempresa = empresa, idarea=r).order_by('idreg')
                    print(resalg)
                    for area in resalg:
                        datosareas[b].append(area.idarea.nombre)
                        datosareas[b].append(area.casospos)
                        datosareas[b].append(area.casosneg)
                        totalcont = area.casospos+area.casosneg
                        if(totalcont == 0):
                            datosareas[b].append(0)
                            continue
                        porpos = (area.casospos/totalcont)*100
                        porpos=round(porpos, 2)
                        datosareas[b].append(porpos)
                    posarea.append(resalg[0].casospos)
                    b+=1
                else:
                    continue
            
            request.session['fecha'] = fechaget
            print(posarea)
            print(arealistnomb)
            datossi=1


            try:
                tipo=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fechaget, '%Y-%m-%d'), idarea__idempresa = empresa)
                for dato in tipo:
                    if dato.idarea.tipo == 'Tecnicas':
                        postec = postec + dato.casospos
                    elif dato.idarea.tipo == 'Comerciales':
                        poscom = poscom + dato.casospos
                    elif dato.idarea.tipo == 'Financieras':
                        posfin = posfin + dato.casospos
                    elif dato.idarea.tipo == 'Seguridad':
                        posseg = posseg + dato.casospos
                    elif dato.idarea.tipo == 'Contables':
                        poscon = poscon + dato.casospos
                    elif dato.idarea.tipo == 'Administrativas':
                        posadm = posadm + dato.casospos
                datostipos.append(postec)
                datostipos.append(poscom)
                datostipos.append(posfin)
                datostipos.append(posseg)
                datostipos.append(poscon)
                datostipos.append(posadm)
                datostiposnom.append("Tecnicas")
                datostiposnom.append("Comerciales")
                datostiposnom.append("Financieras")
                datostiposnom.append("Seguridad")
                datostiposnom.append("Contables")
                datostiposnom.append("Administrativas")
                if datostipos.index(max(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(max(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(max(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(max(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(max(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(max(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)

                if datostipos.index(min(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(min(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(min(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(min(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(min(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(min(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
        
    except KeyError:
        return redirect('/') 


    return render(request, 'historialResDia.html', {'totalemppos':totalemppos, 'totalempneg':totalempneg, 'datosareas':datosareas, 'posarea':posarea,'arealistnomb':arealistnomb, 'nombscatter':nombscatter, 'poscatter':poscatter, 'posmonth':posmonth, 'nombmonth':nombmonth, 'datossi':datossi, 'datostiposfn':datostiposfn, 'datostipos':datostipos, 'datostiposnom':datostiposnom, 'empnoform':empnoform})

def historialResDiaPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fecha = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            arean = Area.objects.filter(idempresa=empresa).count()
            arealist = Area.objects.filter(idempresa=empresa)
            emp = Empleado.objects.filter(idempresa=empresa)
            arealistfn = []
            arealistnomb = []
            totalemppos = 0
            totalempneg = 0
            nombscatter=[]
            poscatter=[]
            posmonth=[]
            nombmonth=[]
            datosareas = [[] for i in range(arean)]
            posarea=[]
            b = 0
            posaux=0

            postec = 0
            poscom = 0
            posfin = 0
            posseg = 0
            poscon = 0
            posadm = 0
            datostipos = []
            datostiposnom = []
            datostiposfn = []
            empnofaux = 0
            empnoform = []

            for emps in emp:
                try:
                    FormularioDiario.objects.get(idempleado=emps.idempleado, fechahora__date=datetime.datetime.strptime(fecha, '%Y-%m-%d'))
                except FormularioDiario.DoesNotExist:
                    empnofaux+=1 
            empnoform = [[] for i in range(empnofaux)]

            p=0
            for elem in emp:
                if not FormularioDiario.objects.select_related('idempleado').filter(fechahora__date=datetime.datetime.strptime(fecha, '%Y-%m-%d'), idempleado__idempresa=empresa, idempleado = elem):
                    empnoform[p].append(elem.correo)
                    empnoform[p].append(elem.idarea.nombre)
                    horarios = DiaLaboral.objects.get(idempleado = elem.idempleado)
                    horarios.dia = str(horarios.dia)[1:-1]
                    horarios.dia = horarios.dia.replace("'","")
                    empnoform[p].append(horarios.dia)
                    empnoform[p].append(horarios.horaentrada)
                    p+=1


            try:
                tipo=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = fecha, idarea__idempresa = empresa)
                for dato in tipo:
                    if dato.idarea.tipo == 'Tecnicas':
                        postec = postec + dato.casospos
                    elif dato.idarea.tipo == 'Comerciales':
                        poscom = poscom + dato.casospos
                    elif dato.idarea.tipo == 'Financieras':
                        posfin = posfin + dato.casospos
                    elif dato.idarea.tipo == 'Seguridad':
                        posseg = posseg + dato.casospos
                    elif dato.idarea.tipo == 'Contables':
                        poscon = poscon + dato.casospos
                    elif dato.idarea.tipo == 'Administrativas':
                        posadm = posadm + dato.casospos
                datostipos.append(postec)
                datostipos.append(poscom)
                datostipos.append(posfin)
                datostipos.append(posseg)
                datostipos.append(poscon)
                datostipos.append(posadm)
                datostiposnom.append("Tecnicas")
                datostiposnom.append("Comerciales")
                datostiposnom.append("Financieras")
                datostiposnom.append("Seguridad")
                datostiposnom.append("Contables")
                datostiposnom.append("Administrativas")
                if datostipos.index(max(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(max(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(max(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(max(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(max(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(max(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)

                if datostipos.index(min(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(min(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(min(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(min(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(min(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(min(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 


            for ar in arealist:
                arealistfn.append(ar.idarea)
                arealistnomb.append(ar.nombre)
                resalg = DatosAlgoritmo.objects.filter(idarea=ar.idarea, fecha=fecha, idarea__idempresa = empresa).order_by('idreg')
                for n in resalg:
                    totalemppos+=n.casospos
                    totalempneg+=n.casosneg
            try:
                for i in range(7):
                    ayer=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d') - datetime.timedelta(days = i), idarea__idempresa = empresa)
                    for x in ayer:
                        posaux += x.casospos
                    fechaform=(datetime.datetime.strptime(fecha, '%Y-%m-%d')-datetime.timedelta(days = i)).strftime('%d/%m')
                    nombscatter.append(fechaform)
                    poscatter.append(posaux)
                    posaux=0
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
                
            auxfor=0
            try:
                mesalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fecha, '%Y-%m-%d').month, idarea__idempresa = empresa).order_by('idreg')
                for i in mesalg:
                    posaux = posaux + i.casospos
                    auxfor+=1
                    if auxfor==arean:
                        posmonth.append(posaux)
                        fechaform=i.fecha.strftime('%d/%m/%Y')
                        nombmonth.append(fechaform)
                        posaux=0
                        auxfor=0                        
                        
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            b=0
            for r in arealistfn:
                resalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha = datetime.datetime.strptime(fecha, '%Y-%m-%d'), idarea__idempresa = empresa, idarea=r).order_by('idreg')
                #print(resalg)
                for area in resalg:
                    datosareas[b].append(area.idarea.nombre)
                    datosareas[b].append(area.casospos)
                    datosareas[b].append(area.casosneg)
                    totalcont = area.casospos+area.casosneg
                    if(totalcont == 0):
                        datosareas[b].append(0)
                        continue
                    porpos = (area.casospos/totalcont)*100
                    porpos=round(porpos, 2)
                    datosareas[b].append(porpos)
                posarea.append(resalg[0].casospos)
                b+=1
            print(datosareas)
            

            fig, ax = plt.subplots()
            ax.set_ylabel('Casos positivos')
            ax.set_title('Posibles casos positivos de COVID-19 en los ultimos 7 dias.')
            plt.bar(nombscatter, poscatter)
            ax.invert_xaxis()
            data = io.BytesIO()
            plt.savefig(data, format='png')
            data.seek(0)
            fig2, ax2 = plt.subplots()
            ax2.set_ylabel('Casos positivos')
            ax2.set_title('Posibles casos positivos del mes en curso.')
            plt.bar(nombmonth, posmonth)
            data2 = io.BytesIO()
            plt.savefig(data2, format='png')
            data2.seek(0)
            fig3, ax3 = plt.subplots()
            plt.pie(posarea, labels=arealistnomb, autopct='%1.1f%%')
            ax3.axis('equal')
            plt.title('Posibles casos positivos por area.')
            plt.legend()
            data3 = io.BytesIO()
            plt.savefig(data3, format='png')
            data3.seek(0)
            fig4, ax4 = plt.subplots()
            plt.pie(datostipos, labels=datostiposnom, autopct='%1.1f%%')
            ax4.axis('equal')
            plt.title('Posibles casos positivos por tipo de actividad.')
            plt.legend()
            data4 = io.BytesIO()
            plt.savefig(data4, format='png')
            data4.seek(0)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=ReporteAnalisis.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)

            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Datos generales')
            p.drawString(30,690,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,675,'Casos negativos de la empresa: '+str(totalempneg))
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,660,'Casos positivos de la empresa: '+str(totalemppos))
            p.drawString(30,645,'')
            Image = ImageReader(data)
            p.drawImage(Image, 100, 350, width=400, height=300)
            p.drawString(30,335,'')
            Image2 = ImageReader(data2)
            p.drawImage(Image2, 100, 50, width=400, height=300)
            p.showPage()
            
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Areas')
            p.drawString(30,690,'')
            aux=690
            for areas in datosareas:
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,areas[0]+':')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,str(areas[3])+'% de los empleados del area son posibles portadores.')
                p.drawString(30,aux-45,'')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,'Casos positivos: '+str(areas[1]))
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Casos negativos: '+str(areas[2]))
                aux-=90
            Image3 = ImageReader(data3)
            p.drawImage(Image3, 100, 70, width=350, height=250)

            p.showPage()
            
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Areas')
            p.drawString(30,690,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,675,'Tipo de actividad con mayor numero de posibles contagios:')
            p.setFont('Helvetica', 10)
            p.drawString(30,660,datostiposfn[0])
            p.drawString(30,645,'')
            p.setFont('Helvetica', 10)
            p.drawString(30,630,'Casos positivos: '+str(datostiposfn[1]))
            p.drawString(30,615,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,600,'Tipo de actividad con menor numero de posibles contagios:')
            p.setFont('Helvetica', 10)
            p.drawString(30,585,datostiposfn[2])
            p.drawString(30,570,'')
            p.setFont('Helvetica', 10)
            p.drawString(30,555,'Casos positivos: '+str(datostiposfn[3]))
            Image4 = ImageReader(data4)
            p.drawImage(Image4, 100, 50, width=400, height=300)

            p.showPage()
            
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fecha)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Empleados que no respondieron el formulario diario')
            p.drawString(30,690,'')
            aux=690
            for emps in empnoform:
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,'Correo:')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,emps[0])
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-45,'Area:')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-60,emps[1])
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-75,'Dias laborales:')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-90,emps[2])
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-105,'Hora de entrada:')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-120,str(emps[3]))
                aux-=135
            

            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('historialResDia')
        return response
    except KeyError:
        return redirect('/') 

def historialResMes(request):
    try:
        idadminaux = request.session["idadmin"]
        empresa = Empresa.objects.get(idadmin = idadminaux)
        arean = Area.objects.filter(idempresa=empresa).count()
        arealist = Area.objects.filter(idempresa=empresa)
        #print(arean)
        arealistfn = []
        arealistnomb = []
        totalemppos = 0
        totalempneg = 0
        posmonth=[]
        nombmonth=[]
        datosareas = [[] for i in range(arean)]
        posarea=[]
        b = 0
        posaux=0
        datossi=0

        postec = 0
        poscom = 0
        posfin = 0
        posseg = 0
        poscon = 0
        posadm = 0
        datostipos = []
        datostiposnom = []
        datostiposfn = [] 


        if request.method == 'POST':
            fechaget = request.POST.get('fechafiltro')
            if fechaget == '' or not DatosAlgoritmo.objects.filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa):
                messages.error(request, f'Por favor elija una fecha valida.')
                return redirect('historialResMes')
            for ar in arealist:
                arealistfn.append(ar.idarea)
                arealistnomb.append(ar.nombre)
                resalg = DatosAlgoritmo.objects.filter(idarea=ar.idarea, fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa).order_by('idreg')
                for n in resalg:
                    #print(n)
                    totalemppos+=n.casospos
                    totalempneg+=n.casosneg
            

            try:
                tipo=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa)
                for dato in tipo:
                    if dato.idarea.tipo == 'Tecnicas':
                        postec = postec + dato.casospos
                    elif dato.idarea.tipo == 'Comerciales':
                        poscom = poscom + dato.casospos
                    elif dato.idarea.tipo == 'Financieras':
                        posfin = posfin + dato.casospos
                    elif dato.idarea.tipo == 'Seguridad':
                        posseg = posseg + dato.casospos
                    elif dato.idarea.tipo == 'Contables':
                        poscon = poscon + dato.casospos
                    elif dato.idarea.tipo == 'Administrativas':
                        posadm = posadm + dato.casospos
                datostipos.append(postec)
                datostipos.append(poscom)
                datostipos.append(posfin)
                datostipos.append(posseg)
                datostipos.append(poscon)
                datostipos.append(posadm)
                datostiposnom.append("Tecnicas")
                datostiposnom.append("Comerciales")
                datostiposnom.append("Financieras")
                datostiposnom.append("Seguridad")
                datostiposnom.append("Contables")
                datostiposnom.append("Administrativas")
                if datostipos.index(max(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(max(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(max(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(max(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(max(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(max(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)

                if datostipos.index(min(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(min(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(min(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(min(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(min(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(min(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            
            auxfor=0
            #print(datetime.datetime.strftime(fechaget, '%M'))
            try:
                mesalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa).order_by('idreg')
                #print(mesalg)
                for i in mesalg:
                    posaux = posaux + i.casospos
                    auxfor+=1
                    if auxfor==arean:
                        posmonth.append(posaux)
                        fechaform=i.fecha.strftime('%d/%m/%Y')
                        nombmonth.append(fechaform)
                        posaux=0
                        auxfor=0
                #print(posmonth)
                #print(nombmonth)
                    
                    
                    
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            b=0
            poscount = 0
            negcount = 0
            for r in arealistfn:
                resalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa, idarea=r).order_by('idreg')
                #print(resalg)
                for area in resalg:
                    #datosareas[b].append(area.idarea.nombre)
                    poscount += area.casospos
                    negcount += area.casosneg
                totalcont = poscount+negcount
                if(totalcont == 0):
                    datosareas[b].append(0)
                    datosareas[b].append(0)
                    datosareas[b].append(0)
                    posarea.append(poscount)
                    datosareas[b].append(resalg[0].idarea.nombre)
                    b+=1
                    continue
                porpos = (poscount/totalcont)*100
                porpos=round(porpos, 2)
                datosareas[b].append(porpos)
                datosareas[b].append(poscount)
                datosareas[b].append(negcount)
                posarea.append(poscount)
                datosareas[b].append(resalg[0].idarea.nombre)
                #print(b)
                b+=1
            
            request.session['fecha'] = fechaget
            #print(posarea)
            #print(arealistnomb)
            print(datosareas)
            datossi=1
        #else: 
            #messages.error(request, f'Por favor elija una fecha')
    
    except KeyError:
        return redirect('/') 

    return render(request, 'historialResMes.html', {'totalemppos':totalemppos, 'totalempneg':totalempneg, 'datosareas':datosareas, 'posarea':posarea,'arealistnomb':arealistnomb, 'posmonth':posmonth, 'nombmonth':nombmonth, 'datossi':datossi, 'datostiposfn':datostiposfn, 'datostipos':datostipos, 'datostiposnom':datostiposnom})

def historialResMesPDF(request):
    try:
        idadminaux = request.session["idadmin"]
        if 'fecha' in request.session:
            fechaget = request.session["fecha"]
            empresa = Empresa.objects.get(idadmin = idadminaux)
            arean = Area.objects.filter(idempresa=empresa).count()
            arealist = Area.objects.filter(idempresa=empresa)
            arealistfn = []
            arealistnomb = []
            totalemppos = 0
            totalempneg = 0
            posmonth=[]
            nombmonth=[]
            datosareas = [[] for i in range(arean)]
            posarea=[]
            b = 0
            posaux=0
            postec = 0
            poscom = 0
            posfin = 0
            posseg = 0
            poscon = 0
            posadm = 0
            datostipos = []
            datostiposnom = []
            datostiposfn = [] 

            for ar in arealist:
                arealistfn.append(ar.idarea)
                arealistnomb.append(ar.nombre)
                resalg = DatosAlgoritmo.objects.filter(idarea=ar.idarea, fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa).order_by('idreg')
                for n in resalg:
                    totalemppos+=n.casospos
                    totalempneg+=n.casosneg
                
            auxfor=0

            try:
                tipo=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa)
                for dato in tipo:
                    if dato.idarea.tipo == 'Tecnicas':
                        postec = postec + dato.casospos
                    elif dato.idarea.tipo == 'Comerciales':
                        poscom = poscom + dato.casospos
                    elif dato.idarea.tipo == 'Financieras':
                        posfin = posfin + dato.casospos
                    elif dato.idarea.tipo == 'Seguridad':
                        posseg = posseg + dato.casospos
                    elif dato.idarea.tipo == 'Contables':
                        poscon = poscon + dato.casospos
                    elif dato.idarea.tipo == 'Administrativas':
                        posadm = posadm + dato.casospos
                datostipos.append(postec)
                datostipos.append(poscom)
                datostipos.append(posfin)
                datostipos.append(posseg)
                datostipos.append(poscon)
                datostipos.append(posadm)
                datostiposnom.append("Tecnicas")
                datostiposnom.append("Comerciales")
                datostiposnom.append("Financieras")
                datostiposnom.append("Seguridad")
                datostiposnom.append("Contables")
                datostiposnom.append("Administrativas")
                if datostipos.index(max(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(max(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(max(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(max(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(max(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(max(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)

                if datostipos.index(min(datostipos))==0:
                    datostiposfn.append("Tecnicas")
                    datostiposfn.append(postec)
                elif datostipos.index(min(datostipos))==1:
                    datostiposfn.append("Comerciales")
                    datostiposfn.append(poscom)
                elif datostipos.index(min(datostipos))==2:
                    datostiposfn.append("Financieras")
                    datostiposfn.append(posfin)
                elif datostipos.index(min(datostipos))==3:
                    datostiposfn.append("Seguridad")
                    datostiposfn.append(posseg)
                elif datostipos.index(min(datostipos))==4:
                    datostiposfn.append("Contables")
                    datostiposfn.append(poscon)
                elif datostipos.index(min(datostipos))==5:
                    datostiposfn.append("Administrativas")
                    datostiposfn.append(posadm)
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 

            try:
                mesalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa).order_by('idreg')
                for i in mesalg:
                    posaux = posaux + i.casospos
                    auxfor+=1
                    if auxfor==arean:
                        posmonth.append(posaux)
                        fechaform=i.fecha.strftime('%d/%m/%Y')
                        nombmonth.append(fechaform)
                        posaux=0
                        auxfor=0                
            except DatosAlgoritmo.DoesNotExist:
                print("ERROR") 
            b=0
            poscount = 0
            negcount = 0
            for r in arealistfn:
                resalg=DatosAlgoritmo.objects.select_related('idarea').filter(fecha__month = datetime.datetime.strptime(fechaget, '%Y-%m').month, idarea__idempresa = empresa, idarea=r).order_by('idreg')
                #print(resalg)
                for area in resalg:
                    poscount += area.casospos
                    negcount += area.casosneg
                totalcont = poscount+negcount
                if(totalcont == 0):
                    datosareas[b].append(0)
                    datosareas[b].append(0)
                    datosareas[b].append(0)
                    posarea.append(poscount)
                    datosareas[b].append(resalg[0].idarea.nombre)
                    b+=1
                    continue
                porpos = (poscount/totalcont)*100
                porpos=round(porpos, 2)
                datosareas[b].append(porpos)
                datosareas[b].append(poscount)
                datosareas[b].append(negcount)
                posarea.append(poscount)
                datosareas[b].append(resalg[0].idarea.nombre)
                b+=1
            fig, ax = plt.subplots()
            ax.set_ylabel('Casos positivos')
            ax.set_title('Posibles casos positivos del mes en curso.')
            plt.bar(nombmonth, posmonth)
            data = io.BytesIO()
            plt.savefig(data, format='png')
            data.seek(0)
            fig3, ax3 = plt.subplots()
            plt.pie(posarea, labels=arealistnomb, autopct='%1.1f%%')
            ax3.axis('equal')
            plt.title('Posibles casos positivos por area.')
            plt.legend()
            data3 = io.BytesIO()
            plt.savefig(data3, format='png')
            data3.seek(0)
            fig4, ax4 = plt.subplots()
            plt.pie(datostipos, labels=datostiposnom, autopct='%1.1f%%')
            ax4.axis('equal')
            plt.title('Posibles casos positivos por tipo de actividad.')
            plt.legend()
            data4 = io.BytesIO()
            plt.savefig(data4, format='png')
            data4.seek(0)

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename=ReporteAnalisis.pdf'
            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize='A4')
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fechaget)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)

            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Datos generales')
            p.drawString(30,690,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,675,'Casos negativos de la empresa detectados en el mes: '+str(totalempneg))
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,660,'Casos positivos de la empresa detectados en el mes: '+str(totalemppos))
            p.drawString(30,645,'')
            Image = ImageReader(data)
            p.drawImage(Image, 100, 350, width=400, height=300)
            p.drawString(30,335,'')
            p.showPage()
            
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fechaget)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Areas')
            p.drawString(30,690,'')
            aux=690
            for areas in datosareas:
                p.setFont('Helvetica-Bold', 12)
                p.drawString(30,aux-15,areas[3]+':')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-30,str(areas[0])+'% de los registros de empleados del area en este mes fueron')
                p.drawString(30,aux-45,'posibles portadores.')
                p.drawString(30,aux-60,'')
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-75,'Casos positivos detectados en el mes: '+str(areas[1]))
                p.setFont('Helvetica', 10)
                p.drawString(30,aux-90,'Casos negativos detectados en el mes: '+str(areas[2]))
                aux-=105
            Image3 = ImageReader(data3)
            p.drawImage(Image3, 100, 60, width=320, height=220)

            p.showPage()
            
            p.setLineWidth(.3)
            p.setFont('Helvetica', 22)
            p.drawString(30,750,'COVID Watcher')
            p.setFont('Helvetica', 12)
            p.drawString(30,735,'Reporte de analisis del '+fechaget)
            p.drawString(30,720,'')
            p.setFont('Helvetica-Bold', 12)
            fechahoy=datetime.datetime.now().strftime('%Y-%m-%d')
            p.drawString(480,750,fechahoy)
            p.setFont('Helvetica-Bold', 15)
            p.drawString(30,705,'Areas')
            p.drawString(30,690,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,675,'Tipo de actividad con mayor numero de posibles contagios:')
            p.setFont('Helvetica', 10)
            p.drawString(30,660,datostiposfn[0])
            p.drawString(30,645,'')
            p.setFont('Helvetica', 10)
            p.drawString(30,630,'Casos positivos: '+str(datostiposfn[1]))
            p.drawString(30,615,'')
            p.setFont('Helvetica-Bold', 12)
            p.drawString(30,600,'Tipo de actividad con menor numero de posibles contagios:')
            p.setFont('Helvetica', 10)
            p.drawString(30,585,datostiposfn[2])
            p.drawString(30,570,'')
            p.setFont('Helvetica', 10)
            p.drawString(30,555,'Casos positivos: '+str(datostiposfn[3]))
            Image4 = ImageReader(data4)
            p.drawImage(Image4, 100, 60, width=320, height=220)
            

            p.save()
            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)
            del request.session['fecha']
        else:
            messages.error(request, f'Por favor elija una fecha')
            return redirect('historialResMes')
        return response
    except KeyError:
        return redirect('/') 

@transaction.atomic
def cambiarDatosAdmin(request):
    try:
        idadminaux = request.session["idadmin"]
        if request.method == 'POST':
            form = registroAdministradorDatosEmpresaForm(request.POST)
            if form.is_valid():
                auxid = Empresa.objects.get(idadmin = idadminaux)
                cd = form.cleaned_data
                
                auxid.nombregenerado = cd['nombregenerado']
                auxid.clave=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
                auxid.save()
                messages.success(request, f'Cambios realizados')
                return redirect('menuAdmin')
            else:
                print(form.errors)
        else:
            form = registroAdministradorDatosEmpresaForm()

    except KeyError:
        return redirect('/') 

    return render(request, 'registroAdministradorDatos.html', {})

@transaction.atomic
def modifArea(request):
    try:
        idadminaux = request.session["idadmin"]
        idareaaux = request.GET.get('id')
        if request.method == 'POST':
            #form = crearAreaForm(request.POST)

            auxid = Empresa.objects.get(idadmin = idadminaux)
            areaux = Area.objects.get(idempresa=auxid, idarea=idareaaux)
            if request.POST.get('nombre'):
                areaux.nombre = request.POST.get('nombre')
            if request.POST.get('descripcion'):
                areaux.descripcion = request.POST.get('descripcion')
            if request.POST.get('tipo'):
                areaux.tipo = request.POST.get('tipo')

            areaux.save()
            messages.success(request, f'Cambios realizados')
            return redirect('menuAdmin')

    except KeyError:
        return redirect('/') 
    
    context = {}
    return render(request, 'modifArea.html', context)

@transaction.atomic
def consEmpleados(request):
    try:
        idadminaux = request.session["idadmin"]
        idareaaux = request.GET.get('id')
        auxid = Empresa.objects.get(idadmin = idadminaux)
        areaux = Area.objects.get(idempresa=auxid, idarea=idareaaux)
        datossi=0
        if Empleado.objects.select_related('idarea').filter(idarea=areaux.idarea):
            emparea = Empleado.objects.select_related('idarea').filter(idarea=areaux.idarea)
            empareacont = Empleado.objects.select_related('idarea').filter(idarea=areaux.idarea).count()
            datosemp = [[] for i in range(empareacont)]
            b=0
            for emp in emparea:
                datosemp[b].append(emp.correo)
                datosemp[b].append(emp.sexo)
                datosemp[b].append(emp.idarea.nombre)
                datosemp[b].append(emp.idarea.tipo)
                datosemp[b].append(emp.idempleado)
                b+=1
            datossi=1
            context = {'datosemp' : datosemp, 'datossi':datossi}
            request.session['areaid'] = idareaaux
        else:
            datossi=0
            context = {}
            print("ERROR") 

    except KeyError:
        return redirect('/') 
    
    return render(request, 'consEmpleados.html', context)

@transaction.atomic
def bajaEmpleados(request):
    try:
        idadminaux = request.session["idadmin"]
        idempaux = request.GET.get('id')
        aux = Empleado.objects.get(idempleado = idempaux)
        messages.success(request, f'Usuario eliminado')
        base_url = reverse('consEmpleados')
        query_string = urlencode({'id': aux.idarea_id})
        url = '{}?{}'.format(base_url, query_string)
        aux.delete()
        return redirect(url)
    except KeyError:
        return redirect('/') 

@transaction.atomic
def elimArea(request):
    try:
        idadminaux = request.session["idadmin"]
        idareaux = request.GET.get('id')
        aux = Area.objects.get(idarea = idareaux)
        empaux = Empleado.objects.filter(idarea = idareaux)
        for i in empaux:
            delemp = Empleado.objects.get(idempleado = i.idempleado_id)
            delemp.delete()
        aux.delete()
        messages.success(request, f'Area eliminada')
        return redirect('menuAdmin')
    except KeyError:
        return redirect('/') 

@transaction.atomic
def modifAreaEmp(request):
    try:
        idempaux = request.GET.get('id')
        idareaux = request.session["areaid"]
        idadminaux = request.session["idadmin"]
        empr= Empresa.objects.get(idadmin = idadminaux)
        areas = Area.objects.filter(idempresa = empr.idempresa).exclude(idarea=idareaux)
        if request.method == 'POST':
            empaux = Empleado.objects.get(idempleado = idempaux)
            empaux.idarea_id = request.POST.get('tipo')
            empaux.save()
            messages.success(request, f'Area del empleado cambiada.')
            del request.session['areaid']

    except KeyError:
        return redirect('/') 
    
    return render(request, 'modifAreaEmp.html', {'areas':areas})