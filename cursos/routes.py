from . import cursos
from models import db, Curso, Maestros, Alumnos, Inscripcion
from flask import render_template, request, redirect, url_for, flash
import forms

@cursos.route("/listadoCursos", methods=['GET'])
def listadoCursos():
    lista_cursos = Curso.query.all()
    return render_template(
        "cursos/listadoCursos.html",
        cursos=lista_cursos
    )

@cursos.route("/cursos", methods=['POST', 'GET'])
def curso():
    create_form = forms.CursoForm(request.form)

    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [
        (m.matricula, f"{m.nombre} {m.apellidos} ({m.matricula})")
        for m in maestros
    ]

    if request.method == 'POST' and create_form.validate():
        curso = Curso(
            nombre=create_form.nombre.data,
            descripcion=create_form.descripcion.data,
            maestro_id=create_form.maestro_id.data
        )

        db.session.add(curso)
        db.session.commit()

        return redirect(url_for('cursos.listadoCursos'))

    return render_template("cursos/cursos.html", form=create_form)

@cursos.route("/detallesCurso",methods=['GET','POST'])
def detalles():
	create_form=forms.CursoForm(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		curso=db.session.query(Curso).filter(Curso.id==id).first()
		id=request.args.get('id')
		nombre=curso.nombre
		descripcion=curso.descripcion
		nombreMaes=curso.maestro.nombre
	return render_template("cursos/detallesCurso.html", nombre=nombre, descripcion=descripcion,nombreMaes=nombreMaes)

@cursos.route("/modificarCurso", methods=['GET','POST'])
def modificarCurso():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} ({m.matricula})") for m in maestros]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id
    if request.method == 'POST':
        id = create_form.id.data
        curso = db.session.query(Curso).filter(Curso.id == id).first()
        curso.nombre = create_form.nombre.data
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data
        db.session.commit()
        return redirect(url_for('cursos.listadoCursos'))
    return render_template("cursos/modificarCurso.html", form=create_form)

@cursos.route("/eliminarCurso", methods=['GET','POST'])
def eliminarCurso():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} ({m.matricula})") for m in maestros]
    if request.method == 'GET':
        id = request.args.get('id')
        curso = Curso.query.get_or_404(id)
        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id
    if request.method == 'POST':
        id = create_form.id.data
        curso = Curso.query.get_or_404(id)
        curso.alumnos.clear()
        db.session.delete(curso)
        db.session.commit()
        return redirect(url_for('cursos.listadoCursos'))
    return render_template("cursos/eliminarCurso.html", form=create_form)

@cursos.route("/inscripciones", methods=['GET', 'POST'])
def inscripciones():
    if request.method == 'GET':
        cursos = Curso.query.all()
        alumnos = Alumnos.query.all()
        return render_template(
            "cursos/inscripciones.html",
            cursos=cursos,
            alumnos=alumnos
        )
    
    if request.method == 'POST':
        curso_id = request.form.get('curso_id')
        alumno_id = request.form.get('alumno_id')
        accion = request.form.get('accion')
        
        if accion == 'inscribir':
            # Verificar si ya está inscrito
            existe = Inscripcion.query.filter_by(
                alumno_id=alumno_id, 
                curso_id=curso_id
            ).first()
            
            if not existe:
                inscripcion = Inscripcion(
                    alumno_id=alumno_id,
                    curso_id=curso_id
                )
                db.session.add(inscripcion)
                db.session.commit()
                flash('Alumno inscrito correctamente', 'success')
            else:
                flash('El alumno ya está inscrito en este curso', 'warning')
        
        elif accion == 'eliminar':
            Inscripcion.query.filter_by(
                alumno_id=alumno_id, 
                curso_id=curso_id
            ).delete()
            db.session.commit()
            flash('Inscripción eliminada correctamente', 'success')
        
        return redirect(url_for('cursos.inscripciones'))

@cursos.route("/alumnos_por_curso", methods=['GET', 'POST'])
def alumnos_por_curso():
    curso_id = request.args.get('curso_id') or request.form.get('curso_id')
    curso = Curso.query.get_or_404(curso_id)

    if request.method == 'POST':
        accion = request.form.get('accion')
        alumno_id = request.form.get('alumno_id')

        if accion == "agregar":
            existe = Inscripcion.query.filter_by(
                curso_id=curso_id,
                alumno_id=alumno_id
            ).first()

            if existe:
                flash("El alumno ya está inscrito en este curso", "warning")
            else:
                nueva = Inscripcion(
                    curso_id=curso_id,
                    alumno_id=alumno_id
                )
                db.session.add(nueva)
                db.session.commit()
                flash("Alumno agregado correctamente", "success")

        elif accion == "eliminar":
            Inscripcion.query.filter_by(
                curso_id=curso_id,
                alumno_id=alumno_id
            ).delete()

            db.session.commit()
            flash("Alumno eliminado del curso", "success")

        return redirect(url_for('cursos.alumnos_por_curso', curso_id=curso_id))

    alumnos = curso.alumnos
    alumnos_disponibles = Alumnos.query.all()

    return render_template(
        "cursos/alumnos_por_curso.html",
        curso=curso,
        alumnos=alumnos,
        alumnos_disponibles=alumnos_disponibles
    )

@cursos.route("/cursos_por_alumno", methods=['GET'])
def cursos_por_alumno():
    alumno_id = request.args.get('alumno_id')
    
    if alumno_id:
        alumno = Alumnos.query.get(alumno_id)
        if alumno:
            cursos = alumno.cursos.all() if hasattr(alumno.cursos, 'all') else alumno.cursos
            return render_template(
                "cursos/cursos_por_alumno.html",
                alumno=alumno,
                cursos=cursos
            )
    
    return redirect(url_for('cursos.listadoCursos'))