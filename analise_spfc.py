from bs4 import BeautifulSoup
import pandas as pd

import requests

url = "https://www.arqtricolor.com/memorial/campeonato-brasileiro-2008/"

response = requests.get(url)

if response.status_code == 200:

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    
    data = []

    skip_first_row = True

    for row in table.find_all('tr'):
        if skip_first_row:
            skip_first_row = False
            continue
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]
        data.append(cols)

    df = pd.DataFrame(data, columns=["Pos", "Time", "PTS", "JG", "V", "E", "D", "GM", "GS", "SG", "AP"])

    df["PTS"] = df["PTS"].str.replace(",", "").astype(int)
    df["GM"] = df["GM"].str.replace(",", "").astype(int)
    df["GS"] = df["GS"].str.replace(",", "").astype(int)
    df["SG"] = df["SG"].str.replace(",", "").astype(int)

    print("\n" + "-"*25 + " TABELA BRASILEIRÃO 2008 " + "-"*25 +"\n")
    print(df)
    print("\n" + "-"*75)
    
    tags_rodada = soup.find_all('strong', string=lambda text: text and 'ª Rodada –' in text)

    gols_em_casa = 0
    gols_fora_de_casa = 0

    jogos_em_casa = []
    jogos_fora_de_casa = []

    vitorias_em_casa = 0
    vitorias_fora_de_casa = 0

    print("\nJogos do São Paulo F.C.\n")

    for tag in tags_rodada:
        jogos = tag.text.split("–")[1]
        print(jogos)

        mandantes = jogos.split("x")[0]
        visitantes = jogos.split("x")[1]

        if "São Paulo" in mandantes: 
            jogos_em_casa.append(jogos)
            gols_spfc_mandante = int(mandantes.strip().split()[-1])
            gols_adversario_visitante = int(visitantes.strip().split()[0])
            gols_em_casa += gols_spfc_mandante
            if gols_spfc_mandante > gols_adversario_visitante:
                vitorias_em_casa += 1

        elif "São Paulo" in visitantes:
            jogos_fora_de_casa.append(jogos)
            gols_spfc_visitante = int(visitantes.strip().split()[0])
            gols_adversario_mandante = int(mandantes.strip().split()[-1])
            gols_fora_de_casa += gols_spfc_visitante
            if gols_spfc_visitante > gols_adversario_mandante:
                vitorias_fora_de_casa += 1

    print(f"\nJogos em casa: {jogos_em_casa}")
    print(f"\nJogos fora de casa: {jogos_fora_de_casa}")

    print(f"\nTotal de {vitorias_em_casa} de 19 partidas vencidas em casa")
    print(f"Total de {vitorias_fora_de_casa} de 19 partidas vencidas fora de casa")

    print(f"\nQuantidade de gols em casa: {gols_em_casa}")
    print(f"Média de gols em casa: {(gols_em_casa/19):.2f}")

    print(f"\nQuantidade de gols fora de casa: {gols_fora_de_casa}")
    print(f"Média de gols fora de casa: {(gols_fora_de_casa/19):.2f}")
    



