<div align="center">
  <h1>🎮 Lavava2025 Bot</h1>
  <p><strong>Um Bot de Discord avançado para gerenciamento de partidas, jogadores e rankings.</strong></p>
  
  <!-- Substitua o link abaixo por uma badge real ou remova se não for usar CI/CD -->
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/discord.py-2.0%2B-blueviolet?logo=discord&logoColor=white" alt="Discord.py" />
  <img src="https://img.shields.io/badge/Made_with-Poetry-cyan?logo=poetry" alt="Poetry" />
</div>

<br>

<div align="center">
  <blockquote>
    🏆 <strong>Projeto de Portfólio:</strong> Este bot foi desenvolvido para demonstrar habilidades em integração de APIs (Discord), arquitetura de software limpa em Python e gerenciamento moderno de dependências.
  </blockquote>
</div>

---

## 📖 Visão Geral

O **Lavava2025 Bot** é uma aplicação construída em Python feita para automatizar e facilitar a organização de comunidades no Discord. Ele atua como um administrador de jogos, permitindo cadastros de jogadores, sorteio de times, gerenciamento de mapas e manutenção de rankings automatizados.

### 🎯 Principais Funcionalidades

- **👤 Gerenciamento de Jogadores:** Sistema completo de CRUD para registrar participantes.
- **🗺️ Sistema de Mapas:** Adição, listagem e randomização de mapas para partidas justas.
- **⚔️ Matchmaking & Times:** Criação automatizada de times equilibrados a partir dos jogadores registrados.
- **🏆 Rankings Dinâmicos:** Sistema de pontuação que acompanha o desempenho dos jogadores ao longo do tempo.

---

## 📷 Como Funciona na Prática

> 💡 **Dica de Portfólio:** Insira aqui GIFs ou Screenshots do bot funcionando no seu servidor do Discord!

### Visualizando o Rank
![Captura de Tela do Comando de Rank](URL_DA_SUA_IMAGEM_AQUI.png)
*Exemplo do bot processando e exibindo a tabela de classificação em tempo real.*

### Gerando Times Aleatórios
*(Insira um GIF do comando de criar times)*

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído seguindo boas práticas de engenharia de software e utiliza as seguintes tecnologias:

- **Linguagem:** [Python](https://www.python.org/) (Rápido, robusto e escalável)
- **Framework Discord:** [discord.py](https://discordpy.readthedocs.io/) (Assíncrono e orientado a eventos)
- **Gerenciamento de Pacotes:** [Poetry](https://python-poetry.org/) (Resolução determinística de dependências e builds)

A arquitetura do projeto foi separada em camadas organizadas (`api/`, `config/`, `core/`, `models/`, `services/`), garantindo que o código seja testável, modular e fácil de manter (Padrões MVC/Service-Layer).

---

## 💻 Como Rodar o Projeto Localmente

Se você deseja testar ou rodar sua própria instância do bot, o processo é projetado para ser simples:

### Pré-requisitos
- Python instalado na máquina
- [Poetry](https://python-poetry.org/docs/#installation) instalado
- Um Token de Bot gerado no [Discord Developer Portal](https://discord.com/developers/applications)

### Instalação

**1. Clone o repositório:**
```bash
git clone https://github.com/codeNilson/lavava2025-bot.git
cd lavava2025-bot
```

**2. Instale as dependências usando Poetry:**
```bash
poetry install
```

**3. Configure o Ambiente:**
Crie ou renomeie o arquivo de configuração para incluir o seu token do Discord.
```bash
# Crie um arquivo .env na raiz e insira seu token
DISCORD_TOKEN=seu_token_aqui
```

**4. Inicie o Bot:**
```bash
poetry run python main.py
```
*(O bot indicará no console que está online e pronto para receber comandos!)*

---

## 🤝 Contato
Criado por **[Denilson Silva](https://github.com/codeNilson)**.
Sinta-se livre para entrar em contato ou dar uma explorada no código fonte!
