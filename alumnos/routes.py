from . import alumnoss
from models import db
from flask import render_template, request
import forms
from models import Alumnos
from alumnos.routes import alumnoss
from flask import Flask, render_template, request, redirect, url_for


@alumnoss.route("/index",methods=['GET','POST'])
def index():
	create_form=forms.UseForm(request.form)
	alumno=Alumnos.query.all()
	return render_template("alumnos/index.html",form=create_form,alumno=alumno)

@alumnoss.route("/Alumnos",methods=['POST','GET'])
def alumnos():
	create_form=forms.UseForm(request.form)
	if request.method == 'POST':
		alumno = Alumnos(
			nombre=create_form.nombre.data,
			apellidos=create_form.apellidos.data,
			email=create_form.email.data,
			telefono=create_form.telefono.data
)
		db.session.add(alumno)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/alumnos.html", form=create_form)

@alumnoss.route("/detalles",methods=['GET','POST'])
def detalles():
	create_form=forms.UseForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		id=request.args.get('id')
		nombre=alum1.nombre
		apellidos=alum1.apellidos
		email=alum1.email
		telefono=alum1.telefono
	return render_template("alumnos/detalles.html", nombre=nombre, apellidos=apellidos,email=email,telefono=telefono)

@alumnoss.route("/modificar",methods=['GET','POST'])
def modificar():
	create_form=forms.UseForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alum1.nombre
		create_form.apellidos.data=alum1.apellidos
		create_form.email.data=alum1.email
		create_form.telefono.data=alum1.telefono
	if request.method == 'POST':
		id=create_form.id.data
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		alum1.nombre=create_form.nombre.data
		alum1.apellidos=create_form.apellidos.data
		alum1.email=create_form.email.data
		alum1.telefono=create_form.telefono.data

		db.session.add(alum1)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/modificar.html", form=create_form)

@alumnoss.route("/eliminar",methods=['GET','POST'])
def eliminar():
	create_form=forms.UseForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
		create_form.id.data=request.args.get('id')
		create_form.nombre.data=alum1.nombre
		create_form.apellidos.data=alum1.apellidos
		create_form.email.data=alum1.email
		create_form.telefono.data=alum1.telefono
	if request.method == 'POST':
		id=request.args.get('id')
		alum = Alumnos.query.get(id)
		#delete from alumnos where id=id
		db.session.delete(alum)
		db.session.commit()
		return redirect(url_for('alumnos.index'))
	return render_template("alumnos/eliminar.html", form=create_form)

@alumnoss.route("/cursos_alumno")
def cursos_alumno():
    id = request.args.get('id')

    alumno = Alumnos.query.get(id)

    cursos = alumno.cursos.all()

    return render_template(
        "alumnos/cursos_alumno.html",
        alumno=alumno,
        cursos=cursos
    )
