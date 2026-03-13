from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, IntegerField, RadioField, SubmitField, SelectField, HiddenField
from wtforms import EmailField
from wtforms import validators
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

class UseForm(Form):
    id=IntegerField('id')
    nombre=StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=20,message='Ingresae min=4 max=20')])
    apellidos=StringField('apellidos',[
        validators.DataRequired(message='El campo es requerido')])
    email=EmailField('Correo',[
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingrese un correo valido')])
    telefono=StringField('telefono',[
        validators.DataRequired(message='El campo es requerido')
    ])

class MaestroForm(Form):
    matricula=IntegerField('matricula',)
    nombre=StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=20,message='Ingresae min=4 max=20')])
    apellidos=StringField('apellidos',[
        validators.DataRequired(message='El campo es requerido')])
    especialidad=StringField('especialidad',[
        validators.DataRequired(message='El campo es requerido')])
    email=StringField('email',[
        validators.DataRequired(message='El campo es requerido')
    ])

class CursoForm(Form):
    id=IntegerField('')
    nombre=StringField('Nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=30,message='Ingrese nombre valido')
    ])
    descripcion=StringField('Descripción',[
        validators.DataRequired(message='El campo es requerido')
    ])
    maestro_id = SelectField(
        'Maestro',
        choices=[],
        coerce=int,
        validators=[DataRequired()]
    )
class InscripcionForm(FlaskForm):
    curso_id = HiddenField(validators=[DataRequired()])
    alumno_id = SelectField("Alumno", coerce=int)
    


    
    