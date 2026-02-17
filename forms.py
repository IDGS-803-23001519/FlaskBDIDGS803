from wtforms import Form
from wtforms import StringField, PasswordField, EmailField, BooleanField, IntegerField, RadioField, SubmitField
from wtforms import EmailField
from wtforms import validators

class UseForm(Form):
    id=IntegerField('id')
    nombre=StringField('nombre',[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4,max=20,message='Ingresae min=4 max=20')])
    apaterno=StringField('apaterno',[
        validators.DataRequired(message='El campo es requerido')])
    email=EmailField('Correo',[
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingrese un correo valido')
    ])


    
    