from flask import (Flask, Blueprint, render_template, request)
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user = 	'ngqzsexp'
password = 'fD9ORrczYakTYTWKHm3f_Ca0dfhJcC54'
host = 'tuffi.db.elephantsql.com'
database = 'ngqzsexp'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ngqzsexp:fD9ORrczYakTYTWKHm3f_Ca0dfhJcC54@tuffi.db.elephantsql.com/ngqzsexp'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'projeto blue_final'

db = SQLAlchemy(app)

class Cidades(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(50), nullable = False)
    imagem_url = db.Column(db.String(800), nullable = False)
    curiosidades = db.Column(db.String(800), nullable = False)

    def __init__ (self, nome, imagem_url, curiosidades):
        self.nome = nome
        self.imagem_url = imagem_url
        self.curiosidades = curiosidades

    @staticmethod
    def read_all():
        return Cidades.query.all()

    @staticmethod
    def read_single(cidade_id):
        return Cidades.query.get(cidade_id)

    def save(self): 
        db.session.add(self) # estamos adicionando as informações passadas no form (Nome, url) p/ o Banco de Dados (utilizando sessão)
        db.session.commit()

    def update(self, new_data):
        self.nome = new_data.nome
        self.imagem_url = new_data.imagem_url
        self.curiosidades = new_data.curiosidades
        self.save()

    def delete(self):
        db.session.delete(self) # estamos removendo as informações de um filme do banco de dados
        db.session.commit()

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/read')
def listar_cidades():
    cidades = Cidades.read_all()
    return render_template("listar-cidades.html", listaDeCidades=cidades)

@bp.route('/read/<cidade_id>')
def lista_detalhe_cidade(cidade_id):
    cidades=Cidades.read_single(cidade_id)

    return render_template('read_single.html',
    cidades=cidades)

@bp.route('/create', methods=('GET', 'POST'))
def create():

  id_atribuido = None
#Como o método utilizado no formulário é POST, pegamos os valores dos campos
  if request.method =='POST':
    form=request.form
    cidades = Cidades(form['nome'],form['imagem_url'],form['curiosidades']) 
    cidades.save()
    id_atribuido=cidades.id
  return render_template('create.html', id_atribuido=id_atribuido)

@bp.route('/update/<cidade_id>',methods=('GET', 'POST'))
def update(cidade_id):
  sucesso = None
  cidades = Cidades.read_single(cidade_id)  

  if request.method =='POST':
    form=request.form

    new_data= Cidades(form['nome'],form['imagem_url'],form['curiosidades']) 

    cidades.update(new_data)

    sucesso = True

  return render_template('update.html', cidades=cidades,sucesso=sucesso)


@bp.route('/delete/<cidade_id>') # Rota de confirmação de Delete (pedir para o usuario confirmar se ele realmente quer deletar o filme selecionado)
def delete(cidade_id):
  cidades = Cidades.read_single(cidade_id)

  return render_template('delete.html', cidades=cidades)


@bp.route('/delete/<cidade_id>/confirmed') # Rota que realiza de fato a deleção do filme selecionado e mostra o HTML de SUCESSO
def delete_confirmed(cidade_id):
  sucesso = None

  cidades = Cidades.read_single(cidade_id)

  if cidades:
    cidades.delete()
    sucesso = True

  return render_template('delete.html', sucesso=sucesso)



app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(debug=True)