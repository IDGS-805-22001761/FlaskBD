from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_wtf import CSRFProtect
from config import DevelopmentConfig
import forms
from models import db, Alumno

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
	create_forms=forms.UserForm2(request.form)

	alumno=Alumno.query.all() #Select * from alumnos
	return render_template("index.html", form=create_forms, alumno=alumno)

@app.route("/detalles", methods=["GET", "POST"])
def detalles():
	create_forms=forms.UserForm2(request.form)
	if request.method == 'GET':
		id=request.args.get('id')
		alumno=db.session.query(Alumno).filter(Alumno.id==id).first()
		nom=alumno.nombre
		ape=alumno.apaterno
		mail=alumno.email
		return render_template("detalles.html", form=create_forms, nom=nom, ape=ape, mail=mail)

@app.route("/agregar", methods=["GET", "POST"])
def agregar():
	create_forms=forms.UserForm2(request.form)
	if request.method == 'POST':
		alumno=Alumno(nombre=create_forms.nombre.data,
				apaterno=create_forms.apaterno.data,
			    email=create_forms.email.data)
		#insertar alumnos
		db.session.add(alumno)
		db.session.commit()
		flash("Alumno agregado correctamente")
		return redirect(url_for("index"))
	return render_template("agregar.html", form=create_forms)
	
if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
	app.run()
