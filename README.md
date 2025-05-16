# Simples Nacional Status Checker

Script em Python para extrair CNPJs de um arquivo Excel e consultar automaticamente a situação de optante no Simples Nacional através da API pública [CNPJ.ws](https://publica.cnpj.ws/).

## 🔍 Funcionalidades

- Extrai todos os CNPJs de 14 dígitos de qualquer coluna de uma planilha Excel.
- Consulta cada CNPJ usando a API pública do CNPJ.ws.
- Verifica se a empresa é "Optante" ou "Não optante" do Simples Nacional.
- Salva os resultados parciais a cada 10 CNPJs para permitir retomar em caso de interrupções.
- Aguarda entre requisições para respeitar o limite de consultas da API.

## 📁 Arquivo de Entrada

A planilha deve conter ao menos uma coluna com valores que possuam CNPJs válidos (14 dígitos). O script fará a extração automaticamente.

## ▶️ Como usar

1. Instale as dependências:

```bash
pip install pandas openpyxl requests
```

2. Edite o script:

No início da função `main()`, defina o caminho do arquivo de entrada:

```python
arquivo_entrada = 'caminho_do_arquivo.xlsx'
```

3. Execute o script:

```bash
python main.py
```

## 🧾 Saída

- `resultado_simples_parcial.xlsx`: resultado parcial salvo a cada 10 CNPJs.
- `resultado_simples.xlsx`: resultado final após a conclusão de todas as consultas.

## ⏱ Limite de Requisições

- O script aguarda 1 segundo entre as requisições.
- A cada 3 consultas, aguarda 61 segundos para evitar bloqueio por limite de uso.

## ⚠️ Aviso

Este projeto utiliza uma **API pública e não oficial** (`https://publica.cnpj.ws`). Use com responsabilidade e respeite os limites e termos de uso da API.

## 📄 Licença

Distribuído sob a licença MIT.