# 📡 Projeto IoT - Pipeline e Dashboard de Temperatura

Este projeto consiste em um pipeline de ingestão de dados de sensores IoT a partir de um arquivo CSV para um banco de dados PostgreSQL, além de um dashboard interativo desenvolvido com Streamlit e Plotly para visualização e análise dos dados.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10+**
- **Pandas**
- **SQLAlchemy**
- **psycopg2-binary**
- **PostgreSQL**
- **Streamlit**
- **Plotly**

---

## 📁 Estrutura do Projeto

```
.
├── data/
│   └── IOT-temp.csv               # Arquivo de entrada com dados dos sensores
├── img/                           # Pasta com imagens
├── venv/                          # Pasta do ambiente virtual
├── pipeline.py                    # Pipeline de ingestão de dados
├── dashboard.py                   # Dashboard interativo
├── requirements.txt               # Dependências do projeto
└── README.md                      # Documentação
```

---

## 📦 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto-iot-dashboard.git
cd projeto-iot-dashboard
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## 🗄️ Configuração do Banco de Dados PostgreSQL

Certifique-se de ter o PostgreSQL instalado e rodando. Crie um banco de dados com as seguintes credenciais (ajuste conforme necessário):

- **Usuário:** `postgres`
- **Senha:** `senha123`
- **Host:** `localhost`
- **Porta:** `5432`
- **Banco:** `postgres`

Você pode ajustar a string de conexão nos scripts, se necessário.

---

## 🚀 Execução

### 1. Rode o pipeline para carregar os dados no banco

Certifique-se de que o arquivo `data/IOT-temp.csv` está presente.

```bash
python pipeline.py
```

Esse script criará (ou substituirá) a tabela `temperature_readings` no banco com os dados do CSV.

---

### 2. Crie as views no banco (necessárias para os gráficos)

Execute os comandos SQL abaixo no PostgreSQL:

```sql
-- View 1: Temperatura media por dispositivo
CREATE OR REPLACE VIEW temperatura_media_por_dispositivo AS
SELECT 
    "room_id/id" AS dispositivo,
    AVG(temp) AS temperatura_media
FROM temperature_readings
GROUP BY "room_id/id";


-- View 2: Contagem de leituras por hora
CREATE OR REPLACE VIEW contagem_leituras_por_hora AS
SELECT 
    EXTRACT(HOUR FROM TO_TIMESTAMP(noted_date, 'DD-MM-YYYY HH24:MI')) AS hora,
    COUNT(*) AS total_leituras
FROM temperature_readings
GROUP BY hora
ORDER BY hora;

-- View 3: Temperatura máxima e mínima por dia
CREATE OR REPLACE VIEW temp_max_min_por_dia AS
SELECT 
    TO_DATE(SPLIT_PART(noted_date, ' ', 1), 'DD-MM-YYYY') AS data,
    MAX(temp)/100000 AS temp_max,
    MIN(temp)/100000 AS temp_min
FROM temperature_readings
GROUP BY data
ORDER BY data;
```

---

### 3. Rode o dashboard

```bash
streamlit run dashboard.py
```

O Streamlit abrirá o navegador automaticamente com o dashboard interativo.

---

## 📊 Funcionalidades do Dashboard

- **Gráfico 1**: Média de temperatura por dispositivo (room_id/id).
![alt text](/img/mediatemp.png)
- **Gráfico 2**: Contagem de leituras por hora.
![alt text](/img/leituradia.png)
- **Gráfico 3**: Temperaturas máximas e mínimas por dia.
![alt text](/img/tempmaxmin.png)

---

## 📝 Observações

- A temperatura no CSV original está em uma escala multiplicada por 100.000. O ajuste é feito no código para exibir corretamente em °C.
- O campo `noted_date` no CSV deve estar no formato `DD-MM-YYYY HH:MM`.

---
🌡️ 1. View: temperatura_media_por_dispositivo
    🔍 Propósito:
        Calcula a temperatura média registrada por cada dispositivo (identificado pelo campo "room_id/id").

    🧠 Por que é útil?
        Ajuda a comparar os sensores entre si.
        Permite detectar dispositivos com leituras fora do padrão (muito mais quentes ou frios que os outros).
        Útil em diagnósticos de funcionamento ou de microclimas diferentes nos ambientes monitorados.

    ⚠️ Observação:
        Assim como nas outras views, aqui o campo temp ainda está na escala bruta (multiplicado por 100.000), então a conversão é feita no código Python, antes de exibir o gráfico.

    📈 Como é usada no dashboard?
        No primeiro gráfico de barras, com:
        Eixo X: room_id/id (ID do dispositivo)
        Eixo Y: temperatura média (ajustada no código para °C)



📊 2. View: contagem_leituras_por_hora
    🔍 Propósito:
        Esta view agrupa todas as leituras de temperatura por hora do dia e conta quantas leituras ocorreram em cada uma dessas horas.

    🧠 Por que é útil?
        Permite identificar em quais horários os dispositivos estão mais ativos, ou seja, quando mais leituras foram registradas.

        Útil para visualizar padrões de uso ou detecção de anomalias temporais.

    📈 Como é usada no dashboard?
        No gráfico de linha com hora no eixo X e total_leituras no eixo Y, para mostrar a frequência das leituras ao longo do dia.



🌡️ 3. View: temp_max_min_por_dia
    🔍 Propósito:
        Esta view extrai a data de cada leitura (ignorando a hora) e calcula:   
        A temperatura máxima
        A temperatura mínima
        para cada dia.

    🧠 Por que é útil?
        Permite visualizar a variação térmica diária, identificando os extremos de temperatura registrados.
        Muito comum em dashboards ambientais ou de monitoramento climático.

    ⚠️ Observações técnicas:
        A temperatura é dividida por 100.000 porque no CSV ela vem em uma escala amplificada (por exemplo, 2478900 representa 24.789°C).

    📈 Como é usada no dashboard?
        Em um gráfico de linhas duplas, comparando as temperaturas mínimas e máximas ao longo do tempo.
