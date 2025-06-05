from flask import Flask, render_template_string, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'chave-super-secreta'  # Necessário para CSRF protection 
# um mecanismo de segurança que impede que invasores façam um usuário autenticado realizar ações indesejadas em um site, usando as credenciais desse usuário sem autorização.
#representa um agendamento
class Agendamento:
    def __init__(self, nome, email, telefone, servico, data, mensagem=None):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.servico = servico
        self.data = data
        self.mensagem = mensagem

    # Salva os dados do agendamento em arquivo local
    def salvar_em_arquivo(self, caminho_arquivo='agendamentos.txt'):
        with open(caminho_arquivo, 'a', encoding='utf-8') as arquivo:
            arquivo.write(f'{self.nome};{self.email};{self.telefone};{self.servico};{self.data.strftime("%Y-%m-%d")};{self.mensagem or ""}\n')

# Formulário para agendamento com validação
class AgendamentoForm(FlaskForm):
    nome = StringField('Nome completo', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone', validators=[DataRequired()])
    servico = SelectField('Selecione um serviço', choices=[
        ('Tratamento Facial', 'Tratamento Facial'),
        ('Massagem Relaxante', 'Massagem Relaxante'),
        ('Depilação a Laser', 'Depilação a Laser'),
        ('Terapias Naturais', 'Terapias Naturais'),
        ('Manicure & Pedicure', 'Manicure & Pedicure'),
        ('Redução de Medidas', 'Redução de Medidas')
    ], validators=[DataRequired()])
    data = DateField('Data desejada', format='%Y-%m-%d', validators=[DataRequired()])
    mensagem = TextAreaField('Mensagem (opcional)')
    submit = SubmitField('Agendar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = AgendamentoForm()
    if form.validate_on_submit():
        agendamento = Agendamento(
            nome=form.nome.data,
            email=form.email.data,
            telefone=form.telefone.data,
            servico=form.servico.data,
            data=form.data.data,
            mensagem=form.mensagem.data
        )
        # Salvar dados no arquivo local
        agendamento.salvar_em_arquivo()
        return render_template_string(confirmacao_html, agendamento=agendamento)
    return render_template_string(index_html, form=form)

# HTML para o formulário de agendamento
index_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Agendamento de Serviço</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f2f2f2; padding: 40px; }
        .container { max-width: 520px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        label { font-weight: bold; margin-top: 10px; display: block; }
        input, select, textarea { width: 100%; padding: 10px; margin-top: 5px; border-radius: 5px; border: 1px solid #ccc; }
        input[type="submit"] { background-color: #28a745; color: white; font-weight: bold; border: none; cursor: pointer; margin-top: 20px; }
        input[type="submit"]:hover { background-color: #218838; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Agende seu atendimento</h2>
        <form method="POST">
            {{ form.hidden_tag() }}
            <label>{{ form.nome.label }}</label> {{ form.nome() }}
            <label>{{ form.email.label }}</label> {{ form.email() }}
            <label>{{ form.telefone.label }}</label> {{ form.telefone() }}
            <label>{{ form.servico.label }}</label> {{ form.servico() }}
            <label>{{ form.data.label }}</label> {{ form.data() }}
            <label>{{ form.mensagem.label }}</label> {{ form.mensagem(rows=3) }}
            {{ form.submit() }}
        </form>
    </div>
</body>
</html>
"""

# HTML para confirmação do agendamento
confirmacao_html = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Agendamento Confirmado</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #e6f9ed; padding: 50px; }
        .box { max-width: 600px; margin: auto; background: #fff; padding: 30px; border-radius: 12px; text-align: center; box-shadow: 0 0 15px rgba(0,0,0,0.1); }
        h2 { color: #28a745; }
        p { font-size: 16px; margin: 10px 0; color: #444; }
    </style>
</head>
<body>
    <div class="box">
        <h2>Agendamento Confirmado</h2>
        <p>Olá, <strong>{{ agendamento.nome }}</strong>!</p>
        <p>Seu agendamento para <strong>{{ agendamento.servico }}</strong></p>
        <p>está marcado para o dia <strong>{{ agendamento.data.strftime('%d/%m/%Y') }}</strong>.</p>
        {% if agendamento.mensagem %}
            <p><em>Mensagem:</em> "{{ agendamento.mensagem }}"</p>
        {% endif %}
        <p>Entraremos em contato pelo telefone <strong>{{ agendamento.telefone }}</strong></p>
        <p>ou pelo e-mail <strong>{{ agendamento.email }}</strong>.</p>
    </div>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(debug=True)
