"""
Spotify Insights - Projeto Pandas Harve
========================================

App Streamlit que serve de palco para os exercicios das aulas 1, 2, 3 e 4.

Voce NAO precisa mexer neste arquivo. Toda a logica que voce vai escrever
esta em exercicios/aula1.py, aula2.py, aula3.py e aula4.py.

Para rodar:
    streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from exercicios import aula1, aula2, aula3, aula4

# ------------------------------------------------------------------
# Configuracao geral
# ------------------------------------------------------------------
st.set_page_config(
    page_title="Spotify Insights - Pandas Harve",
    page_icon="🎵",
    layout="wide",
)

DATA_DIR     = Path(__file__).parent / "data"
CSV_PRINCIPAL = DATA_DIR / "spotify-2023.csv"
CSV_ARTISTAS  = DATA_DIR / "artistas_info.csv"
CSV_NOVOS     = DATA_DIR / "spotify_novos_lancamentos.csv"

st.title("🎵 Spotify Insights")
st.caption("Projeto do modulo de Pandas - Harve")


# ------------------------------------------------------------------
# Helper para chamar funcoes dos alunos sem quebrar o app
# ------------------------------------------------------------------
def safe_call(func, *args, **kwargs):
    try:
        return func(*args, **kwargs), None
    except NotImplementedError as e:
        return None, f"⏳ {e}"
    except Exception as e:
        return None, f"❌ Erro: {type(e).__name__}: {e}"


# ------------------------------------------------------------------
# Carrega base principal (chama funcao do aluno - aula 2)
# ------------------------------------------------------------------
df, erro_carga = safe_call(aula2.carregar_e_limpar, str(CSV_PRINCIPAL))

if erro_carga:
    st.warning(
        "Para o app comecar a funcionar, implemente primeiro a funcao "
        "`carregar_e_limpar` em **exercicios/aula2.py**."
    )
    st.info(erro_carga)
    st.stop()

st.success(f"Base carregada: {df.shape[0]} musicas, {df.shape[1]} colunas")

# st.dataframe(df)

# ------------------------------------------------------------------
# Abas - uma por aula
# ------------------------------------------------------------------
aba1, aba2, aba3, aba4 = st.tabs([
    "Aula 1 — Primeiros Passos",
    "Aula 2 — Explorador de Faixas",
    "Aula 3 — Analise do Catalogo",
    "Aula 4 — Visual + Export",
])

# ==================================================================
# ABA AULA 1
# ==================================================================
with aba1:
    st.header("Primeiros Passos")
    st.write("Exercicios de criacao de estruturas e inspecao basica.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📋 Criar Series")
        st.code("criar_series_simples([10, 22, 48], ['a', 'b', 'c'])")
        resultado, erro = safe_call(aula1.criar_series_simples, [10, 22, 48], ['a', 'b', 'c'])
        if erro:
            st.info(erro)
        else:
            st.write(resultado)

        st.subheader("📊 Criar DataFrame")
        st.code("criar_dataframe_de_dict({'nome': ['Ana','Bob'], 'idade': [20,25]})")
        resultado, erro = safe_call(aula1.criar_dataframe_de_dict,
                                    {'nome': ['Ana', 'Bob', 'Carla'],
                                     'idade': [20, 25, 30]})
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado)

    with col2:
        st.subheader("📐 Dimensoes")
        resultado, erro = safe_call(aula1.obter_dimensoes, df)
        if erro:
            st.info(erro)
        else:
            st.write(f"shape = {resultado}")

        st.subheader("🏷️ Renomear colunas")
        resultado, erro = safe_call(aula1.renomear_colunas, df,
                                    {'streams': 'reproducoes', 'artist_count': 'qtd_artistas'})
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado.head(5))

    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("🔑 set_index")
        resultado, erro = safe_call(aula1.definir_indice, df, 'track_name')
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado.head(5))

    with col4:
        st.subheader("🔍 Tipos das colunas")
        resultado, erro = safe_call(aula1.tipos_das_colunas, df)
        if erro:
            st.info(erro)
        else:
            st.write(resultado)


# ==================================================================
# ABA AULA 2
# ==================================================================
with aba2:
    st.header("Explorador de Faixas")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔎 Inspecionar coluna")
        coluna = st.selectbox("Coluna:", df.columns, index=0)
        resultado, erro = safe_call(aula2.inspecionar_coluna, df, coluna)
        if erro:
            st.info(erro)
        else:
            st.write(resultado)

    with col2:
        st.subheader("🎤 Filtrar por artista")
        artista = st.text_input("Parte do nome:", value="Taylor")
        if artista:
            resultado, erro = safe_call(aula2.filtrar_por_artista, df, artista)
            if erro:
                st.info(erro)
            else:
                st.write(f"{len(resultado)} musica(s)")
                st.dataframe(resultado[['track_name', 'artist(s)_name', 'released_year', 'streams']])

    st.divider()

    st.subheader("⚡ Filtrar hits (AND)")
    c1, c2 = st.columns(2)
    ano_min     = c1.number_input("Ano min", 1900, 2025, 2020)
    streams_min = c2.number_input("Streams min", 0, value=500_000_000, step=100_000_000)
    resultado, erro = safe_call(aula2.filtrar_hits, df, ano_min, streams_min)
    if erro:
        st.info(erro)
    else:
        st.write(f"{len(resultado)} hit(s)")
        st.dataframe(resultado[['track_name', 'artist(s)_name', 'released_year', 'streams']])

    st.divider()

    st.subheader("🏷️ Categoria de streams")
    resultado, erro = safe_call(aula2.criar_categoria_streams, df)
    if erro:
        st.info(erro)
    else:
        st.write(resultado['categoria_streams'].value_counts())

    st.divider()

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("🎼 Filtrar por modo")
        modo = st.selectbox("Modo:", ["Major", "Minor"])
        resultado, erro = safe_call(aula2.filtrar_por_modo, df, modo)
        if erro:
            st.info(erro)
        else:
            st.write(f"{len(resultado)} musica(s) em {modo}")

    with col6:
        st.subheader("📅 Filtrar por intervalo de ano")
        c1, c2 = st.columns(2)
        a_ini = c1.number_input("De:", 1900, 2025, 2020, key="ai")
        a_fim = c2.number_input("Ate:", 1900, 2025, 2023, key="af")
        resultado, erro = safe_call(aula2.filtrar_por_intervalo_ano, df, a_ini, a_fim)
        if erro:
            st.info(erro)
        else:
            st.write(f"{len(resultado)} musica(s)")

    st.subheader("🔥 Super dancante OU super energica (OR)")
    limite = st.slider("Limite (%)", 50, 100, 85)
    resultado, erro = safe_call(aula2.filtrar_super_dancante_ou_super_energica, df, limite)
    if erro:
        st.info(erro)
    else:
        st.write(f"{len(resultado)} musica(s) acima de {limite}% em pelo menos uma das duas features")

    st.divider()

    col7, col8 = st.columns(2)
    with col7:
        st.subheader("❓ Nulos por coluna")
        resultado, erro = safe_call(aula2.contar_nulos_por_coluna, df)
        if erro:
            st.info(erro)
        else:
            st.write(resultado[resultado > 0] if (resultado > 0).any() else "Sem nulos")

    with col8:
        st.subheader("💧 Preencher nulos")
        col_para_preencher = st.selectbox("Coluna:", ['key', 'in_shazam_charts'])
        resultado, erro = safe_call(aula2.preencher_nulos_da_coluna, df, col_para_preencher, 'Desconhecido')
        if erro:
            st.info(erro)
        else:
            st.write(f"Nulos depois: {resultado[col_para_preencher].isnull().sum()}")


# ==================================================================
# ABA AULA 3
# ==================================================================
with aba3:
    st.header("Analise do Catalogo")

    st.subheader("📊 Estatisticas gerais")
    resultado, erro = safe_call(aula3.estatisticas_gerais, df)
    if erro:
        st.info(erro)
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Total streams", f"{resultado['total_streams']:,}".replace(",", "."))
        c2.metric("BPM medio", f"{resultado['media_bpm']:.1f}")
        c3.metric("Danceability media", f"{resultado['media_danceability']:.1f}%")
        c4, c5 = st.columns(2)
        c4.metric("Ano mais antigo", resultado['ano_mais_antigo'])
        c5.metric("Ano mais recente", resultado['ano_mais_recente'])

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏆 Top N artistas")
        n = st.slider("N", 5, 20, 10)
        resultado, erro = safe_call(aula3.top_n_artistas_por_streams, df, n)
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado)

    with col2:
        st.subheader("🎼 Media de features por modo")
        resultado, erro = safe_call(aula3.media_features_por_modo, df)
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado)

    st.divider()

    st.subheader("📅 Lancamentos por ano")
    resultado, erro = safe_call(aula3.lancamentos_por_ano, df)
    if erro:
        st.info(erro)
    else:
        st.line_chart(resultado)

    st.subheader("🎯 Artista mais streamado em um ano")
    ano_escolhido = st.number_input("Ano:", 1950, 2025, 2023, key="ano_artista")
    resultado, erro = safe_call(aula3.artista_mais_streamado_do_ano, df, int(ano_escolhido))
    if erro:
        st.info(erro)
    else:
        st.success(f"🥇 {resultado}")

    st.divider()

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("💃 Top musicas mais dancantes")
        n2 = st.slider("N", 5, 20, 10, key="n_danca")
        resultado, erro = safe_call(aula3.top_n_musicas_mais_dancantes, df, n2)
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado)

    with col4:
        st.subheader("🎶 BPM medio por modo")
        resultado, erro = safe_call(aula3.bpm_medio_por_modo, df)
        if erro:
            st.info(erro)
        else:
            st.dataframe(resultado)

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("🕒 Streams por decada")
        resultado, erro = safe_call(aula3.streams_por_decada, df)
        if erro:
            st.info(erro)
        else:
            st.bar_chart(resultado)

    with col6:
        st.subheader("👥 Musicas por quantidade de artistas")
        resultado, erro = safe_call(aula3.musicas_por_quantidade_de_artistas, df)
        if erro:
            st.info(erro)
        else:
            st.bar_chart(resultado)

    st.subheader("🚀 Ano com mais streams")
    resultado, erro = safe_call(aula3.ano_com_mais_streams, df)
    if erro:
        st.info(erro)
    else:
        st.success(f"🎉 {resultado}")


# ==================================================================
# ABA AULA 4
# ==================================================================
with aba4:
    st.header("Dashboard Visual + Export")

    st.subheader("📊 Top artistas (barras)")
    n_bar = st.slider("N", 5, 20, 10, key="n_barras")
    resultado, erro = safe_call(aula4.grafico_barras_top_artistas, df, n_bar)
    if erro:
        st.info(erro)
    else:
        st.pyplot(resultado)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🥧 Major x Minor (pizza)")
        resultado, erro = safe_call(aula4.grafico_pizza_modo, df)
        if erro:
            st.info(erro)
        else:
            st.pyplot(resultado)
    with col2:
        st.subheader("📈 Lancamentos por ano (linha)")
        resultado, erro = safe_call(aula4.grafico_linha_lancamentos_por_ano, df)
        if erro:
            st.info(erro)
        else:
            st.pyplot(resultado)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("⚡ Energia x Dancabilidade (scatter)")
        resultado, erro = safe_call(aula4.grafico_dispersao_energia_dancabilidade, df)
        if erro:
            st.info(erro)
        else:
            st.pyplot(resultado)
    with col4:
        st.subheader("🥁 Distribuicao de BPM (histograma)")
        resultado, erro = safe_call(aula4.grafico_histograma_bpm, df)
        if erro:
            st.info(erro)
        else:
            st.pyplot(resultado)

    st.divider()

    st.subheader("🔗 Merge com info dos artistas")
    if CSV_ARTISTAS.exists():
        df_info = pd.read_csv(CSV_ARTISTAS, encoding='utf-8')
        resultado, erro = safe_call(aula4.juntar_com_info_artistas, df, df_info)
        if erro:
            st.info(erro)
        else:
            cols_show = [c for c in ['track_name', 'artist(s)_name', 'streams', 'pais_origem', 'gravadora']
                         if c in resultado.columns]
            st.dataframe(resultado[cols_show].head(20))

    st.subheader("➕ Concat com novos lancamentos")
    if CSV_NOVOS.exists():
        df_novos = pd.read_csv(CSV_NOVOS, encoding='utf-8')
        df_novos['streams'] = pd.to_numeric(df_novos['streams'], errors='coerce')
        resultado, erro = safe_call(aula4.unir_novos_lancamentos, df, df_novos)
        if erro:
            st.info(erro)
        else:
            st.success(f"{len(df)} + {len(df_novos)} -> {len(resultado)} (apos dedup)")
            st.dataframe(resultado.tail(10)[['track_name', 'artist(s)_name', 'released_year', 'streams']])

    st.divider()

    st.subheader("💾 Exportar")
    col5, col6 = st.columns(2)

    with col5:
        st.write("**CSV via funcao salvar_resultado:**")
        if st.button("Salvar saida.csv"):
            destino = Path(__file__).parent / "saida.csv"
            _, erro = safe_call(aula4.salvar_resultado, df, str(destino))
            if erro:
                st.info(erro)
            else:
                st.success(f"Arquivo salvo em {destino}")

        st.write("**Excel via funcao salvar_em_excel:**")
        if st.button("Salvar saida.xlsx"):
            destino_xlsx = Path(__file__).parent / "saida.xlsx"
            _, erro = safe_call(aula4.salvar_em_excel, df, str(destino_xlsx))
            if erro:
                st.info(erro)
            else:
                st.success(f"Arquivo salvo em {destino_xlsx}")

    with col6:
        st.write("**📥 Baixar dataframe direto pelo navegador:**")
        st.caption("Usa a funcao preparar_csv_para_download — sem criar arquivo no servidor.")
        csv_bytes, erro = safe_call(aula4.preparar_csv_para_download, df)
        if erro:
            st.info(erro)
        else:
            st.download_button(
                label="⬇️ Baixar CSV",
                data=csv_bytes,
                file_name="spotify_dataframe.csv",
                mime="text/csv"
            )
