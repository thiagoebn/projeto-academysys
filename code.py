import json
from tkinter import *
from tkinter import messagebox
from random import randint

# ==========================
# Funções utilitárias
# ==========================


def salvar_json(nome_arquivo, dados):
    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        json.dump(dados, arq, ensure_ascii=False, indent=4)


def ler_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as arq:
            return json.load(arq)
    except FileNotFoundError:
        return {}


def validar_email(email):
    return "@" in email


# ==========================
# Funções principais
# ==========================


def cadastrar_usuario(tipo):
    def salvar_cadastro():
        nome = entry_nome.get().strip().title()
        email = entry_email.get().strip().lower()
        senha = entry_senha.get().strip()

        if not nome or not email or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return

        usuarios = ler_json("usuarios.json")

        if email in usuarios:
            messagebox.showwarning("Atenção", "Usuário já cadastrado!")
            return

        usuarios[email] = {"nome": nome, "senha": senha, "tipo": tipo}
        salvar_json("usuarios.json", usuarios)

        messagebox.showinfo(
            "Sucesso", f"{tipo.title()} cadastrado com sucesso!"
        )
        janela.destroy()

    janela = Toplevel(root)
    janela.title(f"Cadastro de {tipo.title()}")
    janela.geometry("300x250")

    Label(
        janela, text=f"Cadastro de {tipo.title()}", font=("Arial", 12, "bold")
    ).pack(pady=10)

    Label(janela, text="Nome completo:").pack()
    entry_nome = Entry(janela)
    entry_nome.pack()

    Label(janela, text="E-mail:").pack()
    entry_email = Entry(janela)
    entry_email.pack()

    Label(janela, text="Senha:").pack()
    entry_senha = Entry(janela, show="*")
    entry_senha.pack()

    Button(janela, text="Cadastrar", command=salvar_cadastro).pack(pady=10)


def login():
    def autenticar():
        email = entry_email.get().strip().lower()
        senha = entry_senha.get().strip()

        usuarios = ler_json("usuarios.json")

        if email in usuarios and usuarios[email]["senha"] == senha:
            messagebox.showinfo(
                "Bem-vindo",
                f"Login bem-sucedido! Olá, {usuarios[email]['nome']}",
            )
            janela.destroy()

            if usuarios[email]["tipo"] == "professor":
                menu_professor()
            else:
                menu_aluno(usuarios[email])
        else:
            messagebox.showerror("Erro", "E-mail ou senha incorretos!")

    janela = Toplevel(root)
    janela.title("Login")
    janela.geometry("300x200")

    Label(janela, text="Login", font=("Arial", 12, "bold")).pack(pady=10)

    Label(janela, text="E-mail:").pack()
    entry_email = Entry(janela)
    entry_email.pack()

    Label(janela, text="Senha:").pack()
    entry_senha = Entry(janela, show="*")
    entry_senha.pack()

    Button(janela, text="Entrar", command=autenticar).pack(pady=10)


# ==========================
# Funções do Professor
# ==========================


def incluir_aluno():
    def salvar_aluno():
        nome = entry_nome.get().title()
        cep = entry_cep.get()
        telefone = entry_tel.get()
        email = entry_email.get().strip()

        if not nome or not cep or not telefone or not email:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        if not validar_email(email):
            messagebox.showerror("Erro", "E-mail inválido!")
            return

        ra = randint(5123, 6000)
        dados = ler_json("dados_aluno.json")

        dados[str(ra)] = {
            "Nome": nome,
            "CEP": cep,
            "Telefone": telefone,
            "E-mail": email,
        }

        salvar_json("dados_aluno.json", dados)

        messagebox.showinfo("Sucesso", f"Aluno cadastrado! RA: {ra}")
        janela.destroy()

    janela = Toplevel(root)
    janela.title("Cadastrar Aluno")
    janela.geometry("300x300")

    Label(janela, text="Cadastro de Aluno", font=("Arial", 12, "bold")).pack(
        pady=10
    )

    Label(janela, text="Nome:").pack()
    entry_nome = Entry(janela)
    entry_nome.pack()

    Label(janela, text="CEP:").pack()
    entry_cep = Entry(janela)
    entry_cep.pack()

    Label(janela, text="Telefone:").pack()
    entry_tel = Entry(janela)
    entry_tel.pack()

    Label(janela, text="E-mail:").pack()
    entry_email = Entry(janela)
    entry_email.pack()

    Button(janela, text="Salvar Aluno", command=salvar_aluno).pack(pady=10)


def incluir_materia():
    def salvar_materia():
        nome_materia = entry_materia.get().strip().title()

        if not nome_materia:
            messagebox.showerror("Erro", "Digite o nome da matéria!")
            return

        materias = ler_json("materias.json")

        if nome_materia in materias:
            messagebox.showwarning("Atenção", "Matéria já cadastrada!")
            return

        materias[nome_materia] = {"professor": "A definir"}
        salvar_json("materias.json", materias)

        messagebox.showinfo("Sucesso", "Matéria cadastrada com sucesso!")
        janela.destroy()

    janela = Toplevel(root)
    janela.title("Incluir Matéria")
    janela.geometry("300x150")

    Label(
        janela, text="Cadastro de Matéria", font=("Arial", 12, "bold")
    ).pack(pady=10)

    Label(janela, text="Nome da matéria:").pack()
    entry_materia = Entry(janela)
    entry_materia.pack()

    Button(janela, text="Salvar Matéria", command=salvar_materia).pack(
        pady=10
    )


def ver_alunos():
    dados = ler_json("dados_aluno.json")

    if not dados:
        messagebox.showinfo("Alunos", "Nenhum aluno cadastrado ainda.")
        return

    janela = Toplevel(root)
    janela.title("Lista de Alunos")
    janela.geometry("400x300")

    Label(
        janela, text="Alunos Cadastrados", font=("Arial", 12, "bold")
    ).pack(pady=10)

    texto = Text(janela, width=45, height=10)
    texto.pack()

    for ra, aluno in dados.items():
        texto.insert(
            END,
            f"RA: {ra}\nNome: {aluno['Nome']}\nE-mail: {aluno['E-mail']}\n\n",
        )


def lancar_notas():
    def salvar_nota():
        ra = entry_ra.get().strip()
        nota = entry_nota.get().strip()

        alunos = ler_json("dados_aluno.json")

        if ra not in alunos:
            messagebox.showerror("Erro", "Aluno não encontrado!")
            return

        try:
            nota = float(nota)
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida!")
            return

        notas = ler_json("notas.json")

        notas[ra] = {
            "Nome": alunos[ra]["Nome"],
            "Nota": nota,
        }

        salvar_json("notas.json", notas)

        messagebox.showinfo(
            "Sucesso", f"Nota lançada para {alunos[ra]['Nome']}"
        )
        janela.destroy()

    janela = Toplevel(root)
    janela.title("Lançar Notas")
    janela.geometry("300x200")

    Label(
        janela, text="Lançamento de Notas", font=("Arial", 12, "bold")
    ).pack(pady=10)

    Label(janela, text="RA do aluno:").pack()
    entry_ra = Entry(janela)
    entry_ra.pack()

    Label(janela, text="Nota:").pack()
    entry_nota = Entry(janela)
    entry_nota.pack()

    Button(janela, text="Salvar Nota", command=salvar_nota).pack(pady=10)


def menu_professor():
    janela = Toplevel(root)
    janela.title("Menu do Professor")
    janela.geometry("250x250")

    Label(janela, text="Menu do Professor", font=("Arial", 12, "bold")).pack(
        pady=10
    )

    Button(janela, text="Cadastrar Aluno", command=incluir_aluno).pack(
        pady=5
    )
    Button(janela, text="Lançar Notas", command=lancar_notas).pack(pady=5)
    Button(janela, text="Incluir Matéria", command=incluir_materia).pack(
        pady=5
    )
    Button(
        janela, text="Ver Alunos Cadastrados", command=ver_alunos
    ).pack(pady=5)

    Button(janela, text="Sair", command=janela.destroy).pack(pady=10)


# ==========================
# Funções do Aluno
# ==========================


def consultar_nota(email_aluno):
    notas = ler_json("notas.json")
    alunos = ler_json("dados_aluno.json")

    for ra, dados in alunos.items():
        if dados["E-mail"] == email_aluno:
            if ra in notas:
                messagebox.showinfo(
                    "Nota", f"Sua nota: {notas[ra]['Nota']}"
                )
            else:
                messagebox.showinfo(
                    "Nota", "Você ainda não possui nota lançada."
                )
            return

    messagebox.showwarning("Atenção", "Aluno não encontrado.")


def menu_aluno(usuario):
    janela = Toplevel(root)
    janela.title("Menu do Aluno")
    janela.geometry("250x180")

    Label(janela, text="Menu do Aluno", font=("Arial", 12, "bold")).pack(
        pady=10
    )

    Button(
        janela,
        text="Consultar Nota",
        command=lambda: consultar_nota(usuario["nome"]),
    ).pack(pady=5)

    Button(janela, text="Sair", command=janela.destroy).pack(pady=10)


# ==========================
# Interface principal
# ==========================

root = Tk()
root.title("AcademySys")
root.geometry("300x300")

Label(root, text="AcademySys", font=("Arial", 14, "bold")).pack(pady=15)

Button(
    root,
    text="Cadastrar Professor",
    command=lambda: cadastrar_usuario("professor"),
    width=25,
).pack(pady=5)

Button(
    root,
    text="Cadastrar Aluno",
    command=lambda: cadastrar_usuario("aluno"),
    width=25,
).pack(pady=5)

Button(root, text="Login", command=login, width=25).pack(pady=5)

Button(root, text="Sair", command=root.destroy, width=25).pack(pady=15)

root.mainloop()
