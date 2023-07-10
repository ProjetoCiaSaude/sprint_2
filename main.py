#################################################################################################
############################################ IMPORTS ############################################
#################################################################################################
from flask import Flask, render_template, request, redirect, session, flash
from bd import tratamentos, pacientes, usuarios
from functions import pacientesTable_toHTML
from time import sleep
import bcrypt
import os

##################
#### FLASK APP ###
##################

app = Flask(__name__)
app.secret_key = "sua_chave_secreta"

#############
### ROTAS ###
#############

# HOME
@app.route('/home')
def home():
    return render_template('home.html')

# LOGOUT
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return render_template('landing_page.html')

#############
### LOGIN ###
#############

# ROTA LOGIN
@app.route('/')
def login_page():
    return render_template('login.html', boolean = True)

# Rota de login
@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Buscar o usuário no banco de dados
    user = usuarios.find_one({'username': username})

    # Verificar usuário e senha
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        flash('Login feito com sucesso!', category='success')
        return redirect('/home')
    else:
        flash('Usuário ou senha incorreto!', category='error')
        sleep(2)
        return redirect("/")

################
### PACIENTE ###
################
@app.route('/paciente', methods = ['GET', 'POST'])
def paciente_novo():

    if request.method == 'POST':
        # paciente = request.form.to_dict()
        paciente = request.form

        # variaveis do form
        nome = paciente.get('nome')
        endereco = paciente.get('endereco')
        rg = paciente.get('rg')
        cpf = paciente.get('cpf')
        telefone = paciente.get('telefone')
        email = paciente.get('email')
        data_nascimento = paciente.get('data_nascimento')
        responsavel = paciente.get('responsavel')
        medico_solicitante = paciente.get('medico_solicitante')
        crm = paciente.get('crm')
        ocupacao = paciente.get('ocupacao')
        cid = paciente.get('cid')
        numero_carteirinha = paciente.get('numero_carteirinha')
        plano = paciente.get('plano')

        # regra para não pegar o valor "Selecione uma opção"
        if paciente.get('pagamento') == 'Selecione uma opção':
            pagamento = ""
        if paciente.get('pagamento') != 'Selecione uma opção':
            pagamento = paciente.get('pagamento')
            
        if paciente.get('empresa') == 'Selecione uma opção':
            empresa = ""
        if paciente.get('empresa') != 'Selecione uma opção':
            empresa = paciente.get('empresa')


        response = {
            'nome': nome,
            'endereco': endereco,
            'rg': rg,
            'cpf': cpf,
            'telefone': telefone,
            'email': email,
            'data_nascimento': data_nascimento,
            'responsavel': responsavel,
            'medico_solicitante': medico_solicitante,
            'crm': crm,
            'ocupacao': ocupacao,
            'cid': cid,
            'pagamento': pagamento,
            'empresa': empresa,
            'numero_carteirinha': numero_carteirinha,
            'plano': plano
        }

        print(response)

        # Inserir o novo usuário no banco de dados
        pacientes.insert_one(response)

        flash('Paciente cadastrado com sucesso!', category='success')
        return redirect('/tratamento')

    return render_template('paciente.html')

################
### CONSULTA ###
################
@app.route('/consulta')
def paciente_consulta():
    pacientesTable_toHTML()
    return render_template('consulta.html')

##################
### TRATAMENTO ###
##################
@app.route('/tratamento', methods = ['GET', 'POST'])
def tratamento():

    if request.method == 'POST':
        tratamento_dict = request.form.to_dict()

        # Inserir o novo usuário no banco de dados
        tratamento_dict.insert_one(tratamento)

        flash('Tratamento cadastrado com sucesso!', category='success')
        return redirect('/consulta')

    return render_template('tratamento.html')

######################
### PACIENTE TABLE ###
######################
@app.route('/pacientes_table')
def pacientes_table():
    return render_template('pacientes_table.html')

#################################
############## RUN ##############
#################################
if __name__ == '__main__':
    app.run(debug=True)