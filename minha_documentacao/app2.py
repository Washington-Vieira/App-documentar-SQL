import os
import sqlparse
import streamlit as st
import shutil  # Para exclusão de subcategorias
import subprocess  # Para executar comandos do terminal

# Pasta principal da documentação
PASTA_DOCS = "docs"

# Função para atualizar o repositório Git
def atualizar_git(mensagem_commit):
    try:
        # Adicionar todos os arquivos ao Git
        subprocess.run(["git", "add", "."], check=True)

        # Criar um commit com a mensagem informada
        subprocess.run(["git", "commit", "-m", mensagem_commit], check=True)

        # Fazer o push para o repositório remoto
        subprocess.run(["git", "push", "origin", "main"], check=True)
        st.success("Alterações enviadas para o repositório GitHub com sucesso!")
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao atualizar o repositório Git: {e}")

# Configurar a interface com Streamlit
st.title("Documentador de Consultas SQL")

# Criar a lista dinâmica de subcategorias
if not os.path.exists(PASTA_DOCS):
    os.makedirs(PASTA_DOCS)

subcategorias_existentes = [d for d in os.listdir(PASTA_DOCS) if os.path.isdir(os.path.join(PASTA_DOCS, d))]
nova_subcategoria = st.text_input("Adicionar uma nova subcategoria:", key="nova_subcategoria")

if st.button("Criar Subcategoria", key="criar_subcategoria"):
    if nova_subcategoria.strip():
        pasta_nova_subcategoria = os.path.join(PASTA_DOCS, nova_subcategoria.strip())
        if not os.path.exists(pasta_nova_subcategoria):
            os.makedirs(pasta_nova_subcategoria)
            st.success(f"Subcategoria '{nova_subcategoria}' criada com sucesso!")
            atualizar_git(f"Adicionada nova subcategoria: {nova_subcategoria}")  # Atualizar Git
            st.session_state["refresh"] = True  # Marca para recarregar a página
        else:
            st.warning(f"A subcategoria '{nova_subcategoria}' já existe.")
    else:
        st.error("Por favor, insira um nome válido para a subcategoria.")

# Forçar o refresh da página ao detectar a marcação no estado
if st.session_state.get("refresh"):
    st.session_state["refresh"] = False  # Reseta o estado
    st.experimental_rerun()  # Recarrega a página

# Exibir subcategorias como abas
if subcategorias_existentes:
    abas = st.tabs([f"📂 {subcategoria}" for subcategoria in subcategorias_existentes])

    for aba, subcategoria in zip(abas, subcategorias_existentes):
        with aba:
            st.subheader(f"Gerenciando a Subcategoria: {subcategoria}")

            # Pasta da subcategoria
            pasta_subcategoria = os.path.join(PASTA_DOCS, subcategoria)
            arquivos = [f for f in os.listdir(pasta_subcategoria) if f.endswith(".md")]

            # Abas internas para gerenciar consultas
            abas_internas = st.tabs(["Adicionar Consulta", "Visualizar Consultas", "Editar Consultas", "Excluir Consultas"])

            # Aba: Adicionar Consulta
            with abas_internas[0]:
                st.subheader("Adicionar Nova Consulta")
                nome_arquivo = st.text_input(
                    "Nome do arquivo (sem extensão):",
                    value="nova_consulta",
                    key=f"nome_arquivo-{subcategoria}"
                )
                consulta_sql = st.text_area(
                    "Digite a consulta SQL aqui:",
                    key=f"consulta_sql-{subcategoria}"
                )

                if st.button("Salvar Consulta", key=f"salvar_consulta-{subcategoria}"):
                    if not nome_arquivo.strip() or not consulta_sql.strip():
                        st.error("Por favor, preencha todos os campos!")
                    else:
                        consulta_formatada = sqlparse.format(consulta_sql, reindent=True, keyword_case='upper')
                        conteudo_markdown = f"# Consulta SQL - {subcategoria}\n\n```sql\n{consulta_formatada}\n```\n"
                        caminho_arquivo = os.path.join(pasta_subcategoria, f"{nome_arquivo}.md")
                        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                            arquivo.write(conteudo_markdown)
                        st.success(f"Consulta '{nome_arquivo}' salva com sucesso!")
                        atualizar_git(f"Adicionada nova consulta: {nome_arquivo} na subcategoria {subcategoria}")  # Atualizar Git
                        st.session_state["refresh"] = True  # Marca para recarregar a página

            # Aba: Visualizar Consultas
            with abas_internas[1]:
                st.subheader("Visualizar Consultas")
                if arquivos:
                    consulta_selecionada = st.selectbox(
                        f"Selecione uma consulta para visualizar:",
                        arquivos,
                        key=f"visualizar-{subcategoria}"
                    )
                    if consulta_selecionada:
                        caminho_consulta = os.path.join(pasta_subcategoria, consulta_selecionada)
                        with open(caminho_consulta, "r", encoding="utf-8") as arquivo:
                            conteudo = arquivo.read()
                        st.markdown(conteudo)
                else:
                    st.info(f"Nenhuma consulta documentada na subcategoria **{subcategoria}**.")

            # Aba: Editar Consultas
            with abas_internas[2]:
                st.subheader("Editar Consultas")
                if arquivos:
                    consulta_selecionada = st.selectbox(
                        f"Selecione uma consulta para editar:",
                        arquivos,
                        key=f"editar-{subcategoria}"
                    )
                    if consulta_selecionada:
                        caminho_consulta = os.path.join(pasta_subcategoria, consulta_selecionada)
                        with open(caminho_consulta, "r", encoding="utf-8") as arquivo:
                            conteudo_atual = arquivo.read()

                        # Extrair apenas o conteúdo SQL, removendo o Markdown
                        if "```sql" in conteudo_atual:
                            inicio_sql = conteudo_atual.index("```sql") + len("```sql\n")
                            fim_sql = conteudo_atual.index("```", inicio_sql)
                            conteudo_sql = conteudo_atual[inicio_sql:fim_sql].strip()
                        else:
                            conteudo_sql = conteudo_atual.strip()

                        # Editor para a consulta SQL
                        consulta_editada = st.text_area(
                            "Edite a consulta SQL:",
                            value=conteudo_sql,
                            height=200,
                            key=f"editar_consulta-{consulta_selecionada}"
                        )

                        # Botão para salvar as alterações
                        if st.button("Salvar Alterações", key=f"salvar-{consulta_selecionada}"):
                            consulta_formatada = sqlparse.format(consulta_editada, reindent=True, keyword_case='upper')
                            conteudo_markdown = f"# Consulta SQL - {subcategoria}\n\n```sql\n{consulta_formatada}\n```\n"
                            with open(caminho_consulta, "w", encoding="utf-8") as arquivo:
                                arquivo.write(conteudo_markdown)
                            st.success(f"Consulta '{consulta_selecionada}' foi atualizada com sucesso!")
                            atualizar_git(f"Atualizada consulta: {consulta_selecionada} na subcategoria {subcategoria}")  # Atualizar Git
                            st.session_state["refresh"] = True  # Marca para recarregar a página

                else:
                    st.info(f"Nenhuma consulta disponível para edição na subcategoria **{subcategoria}**.")

            # Aba: Excluir Consultas
            with abas_internas[3]:
                st.subheader("Excluir Consultas")
                if arquivos:
                    consulta_selecionada = st.selectbox(
                        f"Selecione uma consulta para excluir:",
                        arquivos,
                        key=f"excluir-{subcategoria}"
                    )
                    if consulta_selecionada:
                        if st.button(f"Excluir Consulta '{consulta_selecionada}'", key=f"confirmar-excluir-{consulta_selecionada}"):
                            caminho_consulta = os.path.join(pasta_subcategoria, consulta_selecionada)
                            os.remove(caminho_consulta)
                            st.warning(f"Consulta '{consulta_selecionada}' foi excluída.")
                            atualizar_git(f"Excluída consulta: {consulta_selecionada} na subcategoria {subcategoria}")  # Atualizar Git
                            st.session_state["refresh"] = True  # Marca para