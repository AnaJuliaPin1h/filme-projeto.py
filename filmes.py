"""

          sistema de cadastro de filmes              
                                                              
"""

import os
import csv
import time

# ── Configurações 
ARQUIVO = "filmes.txt"
SEPARADOR = "|"
CAMPOS = ["id", "titulo", "genero", "ano", "duracao_min", "nota"]

# ── Cores ANSI
class Cor:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    AMARELO = "\033[93m"
    CIANO   = "\033[96m"
    VERDE   = "\033[92m"
    VERMELHO= "\033[91m"
    BRANCO  = "\033[97m"
    CINZA   = "\033[90m"
    MAGENTA = "\033[95m"
    AZUL    = "\033[94m"


#  UTILITÁRIOS DE TELA

def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def linha(char="═", tam=62, cor=Cor.CIANO):
    print(f"{cor}{char * tam}{Cor.RESET}")

def titulo_bloco(texto):
    limpar()
    linha("═")
    print(f"{Cor.BOLD}{Cor.AMARELO}  🎬  {texto.upper()}{Cor.RESET}")
    linha("═")
    print()

def pausar():
    print()
    input(f"  {Cor.CINZA}[ Pressione ENTER para continuar... ]{Cor.RESET}")

def msg_ok(texto):
    print(f"\n  {Cor.VERDE}✔  {texto}{Cor.RESET}")

def msg_erro(texto):
    print(f"\n  {Cor.VERMELHO}✘  {texto}{Cor.RESET}")

def msg_aviso(texto):
    print(f"\n  {Cor.AMARELO}⚠  {texto}{Cor.RESET}")



#  FUNÇÕES DE ARQUIVO


def inicializar_arquivo():
    """Cria o arquivo .txt com cabeçalho se não existir."""
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", encoding="utf-8") as f:
            f.write(SEPARADOR.join(CAMPOS) + "\n")

def carregar_filmes():
    """Lê todos os filmes do arquivo e retorna lista de dicionários."""
    filmes = []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        linhas = f.readlines()
    if len(linhas) <= 1:
        return filmes
    for linha_txt in linhas[1:]:
        linha_txt = linha_txt.strip()
        if linha_txt:
            partes = linha_txt.split(SEPARADOR)
            if len(partes) == len(CAMPOS):
                filmes.append(dict(zip(CAMPOS, partes)))
    return filmes

def salvar_filmes(filmes):
    """Salva lista de filmes no arquivo, substituindo conteúdo anterior."""
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        f.write(SEPARADOR.join(CAMPOS) + "\n")
        for filme in filmes:
            linha_txt = SEPARADOR.join([
                filme["id"], filme["titulo"], filme["genero"],
                filme["ano"], filme["duracao_min"], filme["nota"]
            ])
            f.write(linha_txt + "\n")

def proximo_id(filmes):
    """Gera o próximo ID disponível."""
    if not filmes:
        return "1"
    ids = [int(f["id"]) for f in filmes if f["id"].isdigit()]
    return str(max(ids) + 1) if ids else "1"



#  VALIDAÇÕES

def validar_ano(ano):
    if not ano.isdigit():
        return False, "Ano deve conter apenas números."
    a = int(ano)
    if a < 1888 or a > 2030:
        return False, "Ano deve estar entre 1888 e 2030."
    return True, ""

def validar_duracao(dur):
    if not dur.isdigit():
        return False, "Duração deve conter apenas números inteiros."
    if int(dur) <= 0:
        return False, "Duração deve ser maior que zero."
    return True, ""

def validar_nota(nota):
    try:
        n = float(nota.replace(",", "."))
        if n < 0 or n > 10:
            return False, "Nota deve estar entre 0 e 10."
        return True, ""
    except ValueError:
        return False, "Nota inválida. Use formato numérico (ex: 8.5)."

def validar_titulo_duplicado(titulo, filmes, id_excluir=None):
    for f in filmes:
        if f["titulo"].strip().lower() == titulo.strip().lower():
            if id_excluir and f["id"] == id_excluir:
                continue
            return True
    return False

def entrada_obrigatoria(prompt):
    while True:
        valor = input(prompt).strip()
        if valor:
            return valor
        msg_erro("Campo obrigatório. Não pode ser vazio.")

def escolher_genero():
    generos = [
        "Ação", "Aventura", "Animação", "Comédia", "Documentário",
        "Drama", "Ficção Científica", "Horror", "Romance", "Suspense", "Outros"
    ]
    print(f"\n  {Cor.CIANO}Gêneros disponíveis:{Cor.RESET}")
    for i, g in enumerate(generos, 1):
        print(f"  {Cor.CINZA}[{i:2}]{Cor.RESET} {g}")
    while True:
        op = input(f"\n  {Cor.BRANCO}Escolha o número do gênero: {Cor.RESET}").strip()
        if op.isdigit() and 1 <= int(op) <= len(generos):
            return generos[int(op) - 1]
        msg_erro("Opção inválida. Digite um número da lista.")



#  EXIBIÇÃO DE FILMES

def imprimir_cabecalho_tabela():
    print(f"  {Cor.BOLD}{Cor.CIANO}"
          f"{'ID':<5} {'TÍTULO':<28} {'GÊNERO':<15} {'ANO':<6} {'MIN':<5} {'NOTA':<5}"
          f"{Cor.RESET}")
    linha("─", 62, Cor.CINZA)

def imprimir_filme_linha(f):
    nota = float(f["nota"].replace(",", "."))
    cor_nota = Cor.VERDE if nota >= 7 else (Cor.AMARELO if nota >= 5 else Cor.VERMELHO)
    titulo = f["titulo"][:27] if len(f["titulo"]) > 27 else f["titulo"]
    genero = f["genero"][:14] if len(f["genero"]) > 14 else f["genero"]
    print(
        f"  {Cor.AMARELO}{f['id']:<5}{Cor.RESET}"
        f"{Cor.BRANCO}{titulo:<28}{Cor.RESET}"
        f"{Cor.CINZA}{genero:<15}{Cor.RESET}"
        f"{f['ano']:<6}"
        f"{f['duracao_min']:<5}"
        f"{cor_nota}{f['nota']:<5}{Cor.RESET}"
    )

def imprimir_ficha_filme(f):
    linha("─", 62, Cor.CINZA)
    print(f"  {Cor.BOLD}{Cor.AMARELO}ID         {Cor.RESET}{f['id']}")
    print(f"  {Cor.BOLD}{Cor.AMARELO}Título     {Cor.RESET}{f['titulo']}")
    print(f"  {Cor.BOLD}{Cor.AMARELO}Gênero     {Cor.RESET}{f['genero']}")
    print(f"  {Cor.BOLD}{Cor.AMARELO}Ano        {Cor.RESET}{f['ano']}")
    print(f"  {Cor.BOLD}{Cor.AMARELO}Duração    {Cor.RESET}{f['duracao_min']} min")
    print(f"  {Cor.BOLD}{Cor.AMARELO}Nota       {Cor.RESET}{f['nota']} / 10")
    linha("─", 62, Cor.CINZA)



#  FUNCIONALIDADES CRUD

def incluir_filme():
    titulo_bloco("Incluir Novo Filme")
    filmes = carregar_filmes()

    print(f"  {Cor.CINZA}Preencha os dados do filme abaixo.{Cor.RESET}\n")

    # Título
    while True:
        titulo = entrada_obrigatoria(f"  {Cor.BRANCO}Título: {Cor.RESET}")
        if validar_titulo_duplicado(titulo, filmes):
            msg_erro(f"Já existe um filme com o título \"{titulo}\". Informe outro.")
        else:
            break

    # Gênero
    genero = escolher_genero()

    # Ano
    while True:
        ano = entrada_obrigatoria(f"  {Cor.BRANCO}Ano de lançamento: {Cor.RESET}")
        ok, erro = validar_ano(ano)
        if ok:
            break
        msg_erro(erro)

    # Duração
    while True:
        duracao = entrada_obrigatoria(f"  {Cor.BRANCO}Duração (minutos): {Cor.RESET}")
        ok, erro = validar_duracao(duracao)
        if ok:
            break
        msg_erro(erro)

    # Nota
    while True:
        nota = entrada_obrigatoria(f"  {Cor.BRANCO}Nota (0 a 10): {Cor.RESET}")
        nota = nota.replace(",", ".")
        ok, erro = validar_nota(nota)
        if ok:
            nota = f"{float(nota):.1f}"
            break
        msg_erro(erro)

    # Confirmação
    novo = {
        "id": proximo_id(filmes),
        "titulo": titulo,
        "genero": genero,
        "ano": ano,
        "duracao_min": duracao,
        "nota": nota
    }

    print()
    imprimir_ficha_filme(novo)
    confirmar = input(f"\n  {Cor.AMARELO}Confirmar inclusão? (S/N): {Cor.RESET}").strip().upper()
    if confirmar == "S":
        filmes.append(novo)
        salvar_filmes(filmes)
        msg_ok(f"Filme \"{titulo}\" cadastrado com sucesso! (ID: {novo['id']})")
    else:
        msg_aviso("Inclusão cancelada.")
    pausar()


def alterar_filme():
    titulo_bloco("Alterar Filme")
    filmes = carregar_filmes()

    if not filmes:
        msg_aviso("Nenhum filme cadastrado.")
        pausar()
        return

    id_busca = entrada_obrigatoria(f"  {Cor.BRANCO}Informe o ID do filme a alterar: {Cor.RESET}")
    filme = next((f for f in filmes if f["id"] == id_busca), None)

    if not filme:
        msg_erro(f"Filme com ID {id_busca} não encontrado.")
        pausar()
        return

    print(f"\n  {Cor.CIANO}Dados atuais:{Cor.RESET}")
    imprimir_ficha_filme(filme)
    print(f"\n  {Cor.CINZA}(Deixe em branco para manter o valor atual){Cor.RESET}\n")

    # Título
    while True:
        novo_titulo = input(f"  {Cor.BRANCO}Título [{filme['titulo']}]: {Cor.RESET}").strip()
        if not novo_titulo:
            novo_titulo = filme["titulo"]
            break
        if validar_titulo_duplicado(novo_titulo, filmes, id_excluir=id_busca):
            msg_erro(f"Já existe outro filme com o título \"{novo_titulo}\".")
        else:
            break

    # Gênero
    trocar_genero = input(f"  {Cor.BRANCO}Alterar gênero [{filme['genero']}]? (S/N): {Cor.RESET}").strip().upper()
    novo_genero = escolher_genero() if trocar_genero == "S" else filme["genero"]

    # Ano
    while True:
        novo_ano = input(f"  {Cor.BRANCO}Ano [{filme['ano']}]: {Cor.RESET}").strip()
        if not novo_ano:
            novo_ano = filme["ano"]
            break
        ok, erro = validar_ano(novo_ano)
        if ok:
            break
        msg_erro(erro)

    # Duração
    while True:
        nova_dur = input(f"  {Cor.BRANCO}Duração em minutos [{filme['duracao_min']}]: {Cor.RESET}").strip()
        if not nova_dur:
            nova_dur = filme["duracao_min"]
            break
        ok, erro = validar_duracao(nova_dur)
        if ok:
            break
        msg_erro(erro)

    # Nota
    while True:
        nova_nota = input(f"  {Cor.BRANCO}Nota (0-10) [{filme['nota']}]: {Cor.RESET}").strip()
        if not nova_nota:
            nova_nota = filme["nota"]
            break
        nova_nota = nova_nota.replace(",", ".")
        ok, erro = validar_nota(nova_nota)
        if ok:
            nova_nota = f"{float(nova_nota):.1f}"
            break
        msg_erro(erro)

    # Atualiza
    idx = next(i for i, f in enumerate(filmes) if f["id"] == id_busca)
    filmes[idx] = {
        "id": id_busca,
        "titulo": novo_titulo,
        "genero": novo_genero,
        "ano": novo_ano,
        "duracao_min": nova_dur,
        "nota": nova_nota
    }

    print()
    imprimir_ficha_filme(filmes[idx])
    confirmar = input(f"\n  {Cor.AMARELO}Confirmar alteração? (S/N): {Cor.RESET}").strip().upper()
    if confirmar == "S":
        salvar_filmes(filmes)
        msg_ok("Filme atualizado com sucesso!")
    else:
        msg_aviso("Alteração cancelada.")
    pausar()


def excluir_filme():
    titulo_bloco("Excluir Filme")
    filmes = carregar_filmes()

    if not filmes:
        msg_aviso("Nenhum filme cadastrado.")
        pausar()
        return

    id_busca = entrada_obrigatoria(f"  {Cor.BRANCO}Informe o ID do filme a excluir: {Cor.RESET}")
    filme = next((f for f in filmes if f["id"] == id_busca), None)

    if not filme:
        msg_erro(f"Filme com ID {id_busca} não encontrado.")
        pausar()
        return

    print(f"\n  {Cor.VERMELHO}Você está prestes a excluir:{Cor.RESET}")
    imprimir_ficha_filme(filme)

    confirmar = input(f"\n  {Cor.VERMELHO}Confirmar exclusão? (S/N): {Cor.RESET}").strip().upper()
    if confirmar == "S":
        filmes = [f for f in filmes if f["id"] != id_busca]
        salvar_filmes(filmes)
        msg_ok(f"Filme \"{filme['titulo']}\" excluído com sucesso!")
    else:
        msg_aviso("Exclusão cancelada.")
    pausar()


def relatorio_geral():
    titulo_bloco("Relatório Geral de Filmes")
    filmes = carregar_filmes()

    if not filmes:
        msg_aviso("Nenhum filme cadastrado.")
        pausar()
        return

    # Ordenar por título
    filmes_ord = sorted(filmes, key=lambda f: f["titulo"].lower())

    imprimir_cabecalho_tabela()
    for f in filmes_ord:
        imprimir_filme_linha(f)

    linha("─", 62, Cor.CINZA)

    # Estatísticas
    total = len(filmes)
    notas = [float(f["nota"].replace(",", ".")) for f in filmes]
    media = sum(notas) / total
    melhor = max(filmes, key=lambda f: float(f["nota"].replace(",", ".")))
    pior   = min(filmes, key=lambda f: float(f["nota"].replace(",", ".")))

    print(f"\n  {Cor.BOLD}{Cor.CIANO}── Estatísticas ──────────────────────────────{Cor.RESET}")
    print(f"  Total de filmes : {Cor.AMARELO}{total}{Cor.RESET}")
    print(f"  Nota média      : {Cor.AMARELO}{media:.2f}{Cor.RESET}")
    print(f"  Melhor avaliado : {Cor.VERDE}{melhor['titulo']} ({melhor['nota']}){Cor.RESET}")
    print(f"  Pior avaliado   : {Cor.VERMELHO}{pior['titulo']} ({pior['nota']}){Cor.RESET}")
    pausar()


def relatorio_especifico():
    titulo_bloco("Consulta Específica")
    filmes = carregar_filmes()

    if not filmes:
        msg_aviso("Nenhum filme cadastrado.")
        pausar()
        return

    print(f"  {Cor.CIANO}Buscar por:{Cor.RESET}")
    print(f"  {Cor.CINZA}[1]{Cor.RESET} ID")
    print(f"  {Cor.CINZA}[2]{Cor.RESET} Título (busca parcial)")
    print(f"  {Cor.CINZA}[3]{Cor.RESET} Gênero")
    print(f"  {Cor.CINZA}[4]{Cor.RESET} Nota mínima")
    print()

    op = input(f"  {Cor.BRANCO}Opção: {Cor.RESET}").strip()

    resultado = []

    if op == "1":
        val = entrada_obrigatoria(f"  {Cor.BRANCO}ID: {Cor.RESET}")
        resultado = [f for f in filmes if f["id"] == val]

    elif op == "2":
        val = entrada_obrigatoria(f"  {Cor.BRANCO}Título (ou parte): {Cor.RESET}")
        resultado = [f for f in filmes if val.lower() in f["titulo"].lower()]

    elif op == "3":
        generos_presentes = sorted(set(f["genero"] for f in filmes))
        print(f"\n  {Cor.CIANO}Gêneros cadastrados:{Cor.RESET}")
        for i, g in enumerate(generos_presentes, 1):
            print(f"  {Cor.CINZA}[{i}]{Cor.RESET} {g}")
        while True:
            op_g = input(f"\n  {Cor.BRANCO}Número do gênero: {Cor.RESET}").strip()
            if op_g.isdigit() and 1 <= int(op_g) <= len(generos_presentes):
                genero_escolhido = generos_presentes[int(op_g) - 1]
                resultado = [f for f in filmes if f["genero"] == genero_escolhido]
                break
            msg_erro("Opção inválida.")

    elif op == "4":
        while True:
            val = entrada_obrigatoria(f"  {Cor.BRANCO}Nota mínima (0-10): {Cor.RESET}")
            val = val.replace(",", ".")
            ok, erro = validar_nota(val)
            if ok:
                resultado = [f for f in filmes if float(f["nota"].replace(",", ".")) >= float(val)]
                break
            msg_erro(erro)
    else:
        msg_erro("Opção inválida.")
        pausar()
        return

    print()
    if not resultado:
        msg_aviso("Nenhum filme encontrado com esse critério.")
    else:
        print(f"  {Cor.VERDE}{len(resultado)} filme(s) encontrado(s):{Cor.RESET}\n")
        if len(resultado) == 1:
            imprimir_ficha_filme(resultado[0])
        else:
            imprimir_cabecalho_tabela()
            for f in resultado:
                imprimir_filme_linha(f)
            linha("─", 62, Cor.CINZA)

    pausar()



#  MENU PRINCIPAL

def menu_principal():
    opcoes = {
        "1": ("Incluir Filme",          incluir_filme),
        "2": ("Alterar Filme",          alterar_filme),
        "3": ("Excluir Filme",          excluir_filme),
        "4": ("Relatório Geral",        relatorio_geral),
        "5": ("Consulta Específica",    relatorio_especifico),
        "0": ("Sair",                   None),
    }

    while True:
        limpar()
        print(f"""
{Cor.BOLD}{Cor.AMARELO}
  
          SISTEMA DE CADASTRO DE FILMES          
  
{Cor.RESET}""")

        for chave, (label, _) in opcoes.items():
            if chave == "0":
                print(f"  {Cor.CINZA}{'─'*46}{Cor.RESET}")
            icone = "✦" if chave != "0" else "✖"
            cor = Cor.CIANO if chave != "0" else Cor.VERMELHO
            print(f"  {cor}[{chave}]{Cor.RESET}  {icone}  {label}")

        print()
        linha("═", 62)
        op = input(f"\n  {Cor.BOLD}{Cor.BRANCO}Escolha uma opção: {Cor.RESET}").strip()

        if op == "0":
            limpar()
            print(f"\n  {Cor.AMARELO}Até logo!{Cor.RESET}\n")
            break
        elif op in opcoes:
            opcoes[op][1]()
        else:
            msg_erro("Opção inválida. Tente novamente.")
            time.sleep(1)



#  PONTO DE ENTRADA

if __name__ == "__main__":
    inicializar_arquivo()
    menu_principal()
