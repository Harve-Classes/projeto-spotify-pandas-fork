"""
AULA 4 - Dashboard Visual + Export
====================================

Topicos aplicados:
- Visualizacao de dados (matplotlib)
- Conectando dados (concat e merge)
- Salvando dados (to_csv, to_excel, download)

As funcoes de grafico devem RETORNAR a figura matplotlib (fig), nao chamar
plt.show(). O Streamlit cuida de exibir.
"""

import io
import pandas as pd
import matplotlib.pyplot as plt


def grafico_barras_top_artistas(df: pd.DataFrame, n: int = 10):
    """
    Grafico de barras horizontais com os N artistas que mais somam streams.

    Dica: ax.barh(...). Retorne fig (sem plt.show()).
    """
    top_artistas = (
        df.groupby('artist(s)_name')['streams']
          .sum()
          .sort_values(ascending=False)
          .head(n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_artistas.index, top_artistas.values)
    ax.invert_yaxis()
    ax.set_xlabel('Total de streams')
    ax.set_ylabel('Artista')
    ax.set_title(f'Top {n} artistas por streams')
    fig.tight_layout()
    return fig


def grafico_pizza_modo(df: pd.DataFrame):
    """
    Pizza com a proporcao de musicas em modo 'Major' x 'Minor'.

    Dica: ax.pie(valores, labels=rotulos, autopct='%1.1f%%').
    """
    contagem = df['mode'].value_counts()

    fig, ax = plt.subplots()
    ax.pie(contagem.values, labels=contagem.index, autopct='%1.1f%%')
    ax.set_title('Proporcao de musicas por modo (Major x Minor)')
    return fig


def grafico_linha_lancamentos_por_ano(df: pd.DataFrame):
    """
    Linha com a quantidade de lancamentos por ano (>= 2000).
    """
    df_copy = df.copy()
    df_copy['released_year'] = df_copy['released_year'].astype(int)
    df_copy = df_copy[df_copy['released_year'] >= 2000]

    contagem = df_copy.groupby('released_year').size().sort_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(contagem.index, contagem.values, marker='o')
    ax.set_xlabel('Ano')
    ax.set_ylabel('Quantidade de lancamentos')
    ax.set_title('Lancamentos por ano (a partir de 2000)')
    fig.tight_layout()
    return fig


def juntar_com_info_artistas(df_spotify: pd.DataFrame, df_info: pd.DataFrame) -> pd.DataFrame:
    """
    MERGE entre Spotify e info dos artistas (pais_origem, gravadora, etc).
    No df_spotify a coluna do artista e 'artist(s)_name'; no df_info e 'artist_name'.
    Use how='left' para nao perder musicas.
    """
    df_mergeado = df_spotify.merge(
        right=df_info,
        left_on='artist(s)_name',
        right_on='artist_name',
        how='left'
    )

    return df_mergeado

def unir_novos_lancamentos(df_atual: pd.DataFrame, df_novos: pd.DataFrame) -> pd.DataFrame:
    """
    Concatena os dois DataFrames (linhas) e remove duplicatas.
    """
    return pd.concat([df_atual, df_novos], axis=0).drop_duplicates()

    df_unido = pd.concat([df_atual, df_novos], axis=0)
    return df_unido.drop_duplicates()

def salvar_resultado(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame em CSV no caminho informado, sem indice e encoding utf-8.
    """
    df.to_csv(caminho, index=False, encoding='utf-8')

def grafico_dispersao_energia_dancabilidade(df: pd.DataFrame):
    """
    Scatter plot: eixo X = 'energy_%', eixo Y = 'danceability_%'.

    Passos:
      1) fig, ax = plt.subplots(figsize=(8, 6))
      2) ax.scatter(df['energy_%'], df['danceability_%'], alpha=0.5)
      3) Titulo e labels
      4) Retornar fig
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(df['energy_%'], df['danceability_%'], alpha=0.5)
    ax.set_title('Energia x Dancabilidade')
    ax.set_xlabel('Energy (%)')
    ax.set_ylabel('Danceability (%)')
    return fig


def grafico_histograma_bpm(df: pd.DataFrame, bins: int = 30):
    """
    Histograma do BPM (batidas por minuto).

    Passos:
      1) fig, ax = plt.subplots()
      2) ax.hist(df['bpm'], bins=bins)
      3) Titulo e labels
      4) Retornar fig
    """
    fig, ax = plt.subplots()
    ax.hist(df['bpm'], bins=bins)
    ax.set_title('Distribuicao de BPM')
    ax.set_xlabel('BPM')
    ax.set_ylabel('Frequencia')
    return fig


def salvar_em_excel(df: pd.DataFrame, caminho: str) -> None:
    """
    Salva o DataFrame em formato Excel (.xlsx) no caminho informado, sem
    indice.

    Dica: df.to_excel(caminho, index=False). Precisa do pacote openpyxl
    instalado (ja esta no requirements.txt).
    """
    df.to_excel(caminho, index=False)


def preparar_csv_para_download(df: pd.DataFrame) -> bytes:
    """
    Prepara o DataFrame como CSV pronto para ser baixado pelo botao
    st.download_button do Streamlit.

    DIFERENCA para salvar_resultado: aqui NAO escrevemos em arquivo. A funcao
    deve retornar os BYTES do CSV. O Streamlit recebe esses bytes diretamente.

    Passos:
      1) Use df.to_csv(index=False) (SEM passar caminho — retorna string).
      2) Converta a string para bytes com .encode('utf-8').
      3) Retorne os bytes.

    Exemplo de uso no Streamlit:
      bytes_csv = preparar_csv_para_download(df)
      st.download_button("Baixar", bytes_csv, "dados.csv", "text/csv")
    """
    csv_str = df.to_csv(index=False)
    print(csv_str[:800])  # Debug: mostrar os primeiros caracteres do CSV
    return csv_str.encode('utf-8')