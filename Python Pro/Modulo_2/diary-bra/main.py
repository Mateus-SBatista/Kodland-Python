# Importações
from flask import Flask, render_template, request, redirect, session
# Conectando a biblioteca do banco de dados
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Definindo a chave secreta para a sessão
app.secret_key = 'my_top_secret_123'
# Estabelecendo conexão com SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Criando o banco de dados
db = SQLAlchemy(app)
# Criando uma tabela

class Card(db.Model):
    # Definindo os campos do registro
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Título
    title = db.Column(db.String(100), nullable=False)
    # Descrição
    subtitle = db.Column(db.String(300), nullable=False)
    # Texto
    text = db.Column(db.Text, nullable=False)
    # E-mail do dono do card
    user_email = db.Column(db.String(100), nullable=False)

    # Exibindo o objeto e seu ID
    def __repr__(self):
        return f'<Card {self.id} - {self.title}>'
    
# Tarefa nº 1. Criar a tabela User
class User(db.Model):
    # Criar campos
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Email
    email = db.Column(db.String(100),  nullable=False)
    # Senha
    password = db.Column(db.String(30), nullable=False)

# Criar as tabelas se não existirem
with app.app_context():
    db.create_all()

# Iniciando a página de login
@app.route('/', methods=['GET','POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']
            
        # Tarefa nº 4. Implementar verificação do usuário
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session['user_email'] = user.email
                return redirect('/index')
        error = 'Usuário ou senha incorretos'
        return render_template('login.html', error=error)
     
    else:
        return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Tarefa nº 3. Implementar o registro do usuário
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()  
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Iniciando a página de conteúdo
@app.route('/index')
def index():
    email = session.get('user_email')
    cards = Card.query.filter_by(user_email=email).all()
    return render_template('index.html', cards=cards)

# Iniciando a página do card
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)
    
# Iniciando a página de criação de cards
@app.route('/create')
def create():
    return render_template('create_card.html')

# Formulário de criação do card
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        # Criando o objeto para envio ao banco de dados
        email = session['user_email']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)