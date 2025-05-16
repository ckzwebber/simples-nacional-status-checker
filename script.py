import pandas as pd
import re
import requests
import time
import os

def extrair_cnpjs(arquivo_excel):
    df = pd.read_excel(arquivo_excel)
    cnpj_regex = r"\d{14}"
    cnpjs = []
    vistos = set()
    for coluna in df.columns:
        for valor in df[coluna].astype(str):
            encontrados = re.findall(cnpj_regex, valor)
            for cnpj in encontrados:
                if cnpj not in vistos:
                    vistos.add(cnpj)
                    cnpjs.append(cnpj)
    return cnpjs

def consultar_simples_nacional(cnpj):
    cnpj_limpo = re.sub(r'\D', '', cnpj)
    url = f'https://publica.cnpj.ws/cnpj/{cnpj_limpo}'
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            simples = dados.get('simples', {})
            if simples and simples.get('simples'):
                return 'Optante'
            else:
                return 'Não optante'
        else:
            return 'Erro na consulta'
    except Exception as e:
        return f'Erro: {e}'

def main():
    arquivo_entrada = 'caminho_do_arquivo' # mude o caminho do arquivo de entrada
    arquivo_parcial = 'resultado_simples_parcial.xlsx' # caso precise, mude o caminho do arquivo de saida parcial
    arquivo_final = 'resultado_simples.xlsx' # caso precise, mude o caminho do arquivo de saida final

    cnpjs = extrair_cnpjs(arquivo_entrada)
    resultados = []
    cnpjs_processados = set()

    if os.path.exists(arquivo_parcial):
        df_parcial = pd.read_excel(arquivo_parcial)
        resultados = df_parcial.to_dict(orient='records')
        cnpjs_processados = set(df_parcial['CNPJ'].astype(str))
        print(f'Continuando de onde parou. {len(cnpjs_processados)} CNPJs já processados.')

    for i, cnpj in enumerate(cnpjs, start=1):
        if cnpj in cnpjs_processados:
            continue

        situacao = consultar_simples_nacional(cnpj)
        print(f'CNPJ: {cnpj} - Situação: {situacao}')
        resultados.append({'CNPJ': cnpj, 'Situação Simples Nacional': situacao})
        cnpjs_processados.add(cnpj)

        if len(resultados) % 10 == 0:
            print(f'Salvando parcial após {len(resultados)} consultas...')
            pd.DataFrame(resultados).to_excel(arquivo_parcial, index=False)

        if len(resultados) % 3 == 0:
            print('Aguardando 61 segundos para respeitar o limite de consultas...')
            time.sleep(61)
        else:
            time.sleep(1)

    pd.DataFrame(resultados).to_excel(arquivo_final, index=False)
    print(f'Consulta concluída. Resultado final salvo em {arquivo_final}')

if __name__ == '__main__':
    main()
