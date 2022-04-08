# -*- coding: utf-8 -*-
import os
from django.contrib.sessions.models import Session
from django.contrib import sessions

from django.shortcuts import render
from django.views.generic import FormView, TemplateView
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from django.contrib import messages

from django import forms
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError 

from .forms import FormJob, FormColabora
from .models import WhantJob, Colabora

from django.utils.crypto import get_random_string

from procesos.sender_email import send_email_to_administracion

class GetAJob(FormView):
	form_class  = FormJob 
	template_name = 'getajob.html'
	success_url = '/trabaja-con-nosotros/job_exit/'

	def form_valid(self, form, **kwargs):
		if self.request.method == 'POST':
			if form.is_valid():

				context = super(GetAJob, self).get_context_data(**kwargs)


				# Datos del formulario
				type_doc = form.cleaned_data['tipo_doc']
				doc= form.cleaned_data['doc']
				nombre = form.cleaned_data['nombre']
				celular = form.cleaned_data['celular']
				email = form.cleaned_data['email']
				domicilio = form.cleaned_data['domicilio']
				departamento = form.cleaned_data['departamento']
				provincia = form.cleaned_data['provincia']
				distrito = form.cleaned_data['distrito']

				# Motivo Reclamo
				area = form.cleaned_data['area']
				carrera = form.cleaned_data['carrera']
				idioma = form.cleaned_data['idioma']

				# Adjunto 

				uploaded_file_url=''
				try: 
					adjuntos = self.request.POST.get('cv_adjuntos', True)
				except MultiValueDictKeyError:
					adjuntos = False

				if adjuntos:
					adjuntos = self.request.FILES['cv_adjuntos']
					 
					name_file =  get_available_name(adjuntos.name,doc )

					fs = FileSystemStorage() 
					filename = fs.save('cv/'+name_file, adjuntos)
					uploaded_file_url = fs.url(filename)

					uploaded_file_url = uploaded_file_url.replace('/media', '') 
					
				print('**************************************')
				form_data= WhantJob(
					tipo_doc = type_doc,
					doc =  doc,
					nombre = nombre,
					celular = celular,
					email = email,
					domicilio = domicilio,
					departamento = departamento,
					provincia = provincia,
					distrito = distrito,
					area = area,
					carrera = carrera,
					idioma = idioma,
					cv_adjuntos = uploaded_file_url,
					)
				form_data.save()

				# Envio email 
				asunto = 'Un usuario a registrado sus datos en Bolsa Laboral'
				data_send={
					'type_doc': type_doc,
					'doc' : doc,
					'nombre': nombre,
					'celular': celular,
					'email': email,
					'domicilio': domicilio,
					'departamento': departamento,
					'provincia': provincia,
					'distrito': distrito,

					# Motivo Reclamo
					'area': area,
					'carrera': carrera,
					'idioma':idioma,

					# Adjunto 
					'uploaded_file_url': uploaded_file_url,
				}
				send_email_to_administracion(data_send, asunto) 


			else:
				print(form.errors)

		return super(GetAJob, self).form_valid(form)		

	def get_context_data(self, **kwargs):
		context = super(GetAJob, self).get_context_data(**kwargs)

		context.update(
				{	

				})
		return context

def get_available_name( name , doc):
	dir_name, file_name = os.path.split(name)
	file_root, file_ext = os.path.splitext(file_name)

	name = os.path.join(dir_name, "%s_%s%s" % (doc, get_random_string(7), file_ext))
	return name

class JobExit(TemplateView):
	form_class  = FormJob 
	template_name = 'resp_getajob.html'


class GetColabora(FormView):
	form_class  = FormColabora 
	template_name = 'getajob.html'
	success_url = '/trabaja-con-nosotros/job_exit/'

	def form_valid(self, form, **kwargs):
		if self.request.method == 'POST':
			if form.is_valid():

				context = super(GetColabora, self).get_context_data(**kwargs)
				
				# Datos del formulario
				type_doc = form.cleaned_data['tipo_doc']
				doc = form.cleaned_data['doc']
				nombre = form.cleaned_data['nombre']

				comunidad = form.cleaned_data['comunidad']
				cargo = form.cleaned_data['cargo']

				celular = form.cleaned_data['celular']
				email = form.cleaned_data['email']

				departamento = form.cleaned_data['departamento']
				provincia = form.cleaned_data['provincia']
				distrito = form.cleaned_data['distrito']

				# Motivo Reclamo
				cuentanos = form.cleaned_data['cuentanos']
				
				# Adjunto
				uploaded_file_url=''

				try: 
					adjuntos = self.request.POST.get('doc_adjuntos', True)
				except MultiValueDictKeyError:
					adjuntos = False

				if adjuntos:
					adjuntos = self.request.FILES['doc_adjuntos']

					name_file =  get_available_name(adjuntos.name,doc )

					fs = FileSystemStorage() 
					filename = fs.save('doc/'+ name_file, adjuntos)
					uploaded_file_url = fs.url(filename)

					uploaded_file_url = uploaded_file_url.replace('/media', '')

				print('.......... .... ....... .... **************************************')
				form_data= Colabora(
					tipo_doc = type_doc,
					doc = doc,
					nombre = nombre,
					comunidad = comunidad, 
					cargo = cargo,
					celular = celular,
					email = email,
					departamento = departamento,
					provincia = provincia, 
					distrito = distrito, 
					cuentanos = cuentanos,
					doc_adjuntos = uploaded_file_url,
					)
				form_data.save()

		return super(GetColabora, self).form_valid(form)	
 
	def get_context_data(self, **kwargs):
		context = super(GetColabora, self).get_context_data(**kwargs)

		context.update(
				{	

				})
		return context

