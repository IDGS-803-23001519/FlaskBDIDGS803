from . import maestros
from models import db
from flask import render_template, request
import forms
from models import Maestros
from maestros.routes import maestros
from flask import Flask, render_template, request, redirect, url_for

@maestros.route('/maestros', methods=['GET', 'POST'])
def listado_maestros():  
    create_form = forms.MaestroForm(request.form)
    lista_maestros = Maestros.query.all()
    return render_template(
        "maestros/listadoMaes.html",
        form=create_form,
        maestros=lista_maestros
    )

@maestros.route("/Maestro", methods=['POST','GET'])
def maestro():
    create_form = forms.MaestroForm(request.form)

    if request.method == 'POST':

        existe = Maestros.query.filter_by(
            matricula=create_form.matricula.data
        ).first()

        if existe:
            return render_template(
                "maestros/maestros.html",
                form=create_form,
                error="Ya existe un maestro con esa matrícula"
            )
        maestro = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data
        )

        db.session.add(maestro)
        db.session.commit()

        return redirect(url_for('maestros.listado_maestros'))

    return render_template("maestros/maestros.html", form=create_form)

@maestros.route("/detallesMaes",methods=['GET','POST'])
def detallesMaes():
	create_form=forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		matricula=request.args.get('matricula')
		nombre=maes1.nombre
		apellidos=maes1.apellidos
		especialidad=maes1.especialidad
		email=maes1.email
	return render_template("maestros/detalleMaes.html", matricula=matricula,nombre=nombre, apellidos=apellidos,especialidad=especialidad,email=email)

@maestros.route("/modificarMaes",methods=['GET','POST'])
def modificarMaes():
	create_form=forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes1.nombre
		create_form.apellidos.data=maes1.apellidos
		create_form.especialidad.data=maes1.especialidad
		create_form.email.data=maes1.email
	if request.method == 'POST':
		matricula=create_form.matricula.data
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		maes1.nombre=create_form.nombre.data
		maes1.apellidos=create_form.apellidos.data
		maes1.especialidad=create_form.especialidad.data
		maes1.email=create_form.email.data

		db.session.add(maes1)
		db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))
	return render_template("maestros/modificarMaes.html", form=create_form)

@maestros.route("/eliminarMaes",methods=['GET','POST'])
def eliminarMaes():
	create_form=forms.MaestroForm(request.form)
	if request.method == 'GET':
		matricula=request.args.get('matricula')
		maes1=db.session.query(Maestros).filter(Maestros.matricula==matricula).first()
		create_form.matricula.data=request.args.get('matricula')
		create_form.nombre.data=maes1.nombre
		create_form.apellidos.data=maes1.apellidos
		create_form.especialidad.data=maes1.especialidad
		create_form.email.data=maes1.email
	if request.method == 'POST':
		matricula=request.args.get('matricula')
		maes = Maestros.query.get(matricula)

		db.session.delete(maes)
		db.session.commit()
		return redirect(url_for('maestros.listado_maestros'))
	return render_template("maestros/eliminarMaes.html", form=create_form)

@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil de {nombre}"