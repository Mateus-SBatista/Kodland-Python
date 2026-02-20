# Importar
from flask import Flask, render_template, request, redirect
# Importando a biblioteca de banco de dados
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


app = Flask(__name__)
# Conectando ao SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Criando um Banco de Dados (DB)
db = SQLAlchemy(app)

# Tarefa #1. Criar uma tabela no Banco de Dados
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self): 
       return f'<Card {self.id} - {self.title}>'

# Criar as tabelas se não existirem
with app.app_context():
    db.create_all()

# Executando a página com conteúdo
@app.route('/')
def index():
    # Exibindo os objetos do Banco de Dados
    # Tarefa #2. Exibir os objetos do Banco de Dados no index.html
    cards = Card.query.order_by(Card.created_at.desc()).all()
    

    return render_template('index.html',
                           cards = cards

                           )

# Executando a página com o cartão
@app.route('/card/<int:id>')
def card(id):
    # Tarefa #2. Exibir o cartão correto pelo seu id
    card = Card.query.get_or_404(id)
    

    return render_template('card.html', card=card)

# Executando a página e criando o cartão
@app.route('/create')
def create():
    return render_template('create_card.html')

# O formulário do cartão
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']

        # Tarefa #2. Criar uma forma de armazenar dados no Banco de Dados
        new_card = Card(title=title, subtitle=subtitle, text=text)
        db.session.add(new_card)
        db.session.commit()
        




        return redirect('/')
    else:
        return render_template('create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
