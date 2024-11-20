from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'  # Necessário para gerenciar sessões.

# Página inicial redireciona para o cadastro
@app.route("/")
def home():
    return redirect(url_for("cadastro"))

# Página de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Armazena os dados na sessão (em um projeto real, salve no banco de dados)
        session["nome"] = nome
        session["email"] = email

        return redirect(url_for("calculadora"))

    return render_template("cadastro.html")

# Página de cálculo de salário líquido
@app.route("/calculadora", methods=["GET", "POST"])
def calculadora():
    if request.method == "POST":
        valor_salario = float(request.form["salario"])
        valor_beneficios = float(request.form["beneficio"])
        valor_imposto = 0

        # Cálculo do imposto com base no salário
        if valor_salario >= 0 and valor_salario <= 1100:
            valor_imposto = 0.05 * valor_salario
        elif valor_salario >= 1100.01 and valor_salario <= 2500:
            valor_imposto = 0.10 * valor_salario
        else:
            valor_imposto = 0.15 * valor_salario

        saida = valor_salario - valor_imposto + valor_beneficios

        return render_template(
            "index.html",
            salario=valor_salario,
            beneficios=valor_beneficios,
            imposto=valor_imposto,
            resultado=saida,
            nome=session.get("nome", "Usuário")
        )

    return render_template("index.html", resultado=None, nome=session.get("nome", "Usuário"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)