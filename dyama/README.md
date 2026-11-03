# Projeto DevOps - Exercício Prático CI/CD com Containers (Site 4 - Dyama)

Este projeto implementa a arquitetura completa do exercício prático de DevOps:
- **Código-Fonte (Python Flask)**: API REST conectada a banco de dados relacional MySQL.
- **GitHub Actions**: Pipeline de CI/CD que constrói a imagem Docker da API e a publica no GitHub Packages (GHCR).
- **Servidor (Docker Compose + Makefile)**:
  - **NGINX**: Proxy reverso recebendo tráfego HTTP 80 (Cloudflare DNS `devops007.ugbio.com.br`).
  - **IMAGEM API**: Container da aplicação Flask rodando com Gunicorn.
  - **DB MySQL**: Container MySQL 8.4 com volume persistente e verificação de saúde (*healthcheck*).

---

## 📁 Estrutura de Arquivos

```text
dyama/
├── .env                  # Variáveis de ambiente locais (Site 4)
├── .env-example          # Modelo de variáveis de ambiente
├── docker-compose.yml    # Orquestração dos 3 containers (db, api, nginx)
├── Makefile              # Comandos de automação do servidor
├── README.md             # Esta documentação
├── api/
│   ├── .dockerignore
│   ├── Dockerfile        # Build da imagem Python 3.12 Slim + Gunicorn
│   ├── requirements.txt  # Dependências (Flask, mysql-connector-python, gunicorn)
│   └── app.py            # API REST com rotas /, /health, /mensagens
├── nginx/
│   └── default.conf      # Configuração de Proxy Reverso Nginx -> API:5000
└── .github/
    └── workflows/
        └── ci-cd.yml     # Workflow de CI/CD para GitHub Actions -> GHCR
```

---

## 🚀 Como Executar Localmente (Teste Rápido)

1. **Subir os serviços construindo localmente**:
   ```bash
   make up
   # ou
   docker compose up -d --build
   ```

2. **Verificar o status dos containers**:
   ```bash
   make status
   ```

3. **Verificar os logs**:
   ```bash
   make logs
   ```

4. **Testar os endpoints**:
   ```bash
   make test
   # Ou manualmente:
   curl http://localhost/
   curl http://localhost/health
   curl http://localhost/mensagens
   ```

---

## 🌐 Deploy em Produção (Servidor / Azure)

1. Preencha o arquivo `.env` com suas credenciais do GitHub Packages:
   - `GHCR_USER=seu-usuario`
   - `GHCR_TOKEN=seu-personal-access-token`
   - `DOMAIN=devops007.ugbio.com.br`

2. Execute o deploy automatizado:
   ```bash
   make deploy
   ```
   O comando irá se autenticar no GHCR, baixar a versão mais recente da imagem e subir os serviços.
