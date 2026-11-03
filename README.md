# Exercício Prático: CI/CD com Containers

**Instituição:** Centro Universitário Geraldo Di Biase (UGB)  
**Disciplina:** Melhores Práticas DevOps  
**Dupla:** Yamaguti (Dyama) e Djotage  
**Domínio Alocado:** `devops007.ugbio.com.br`  

---

## 🎯 Objetivo do Projeto

Implementação prática de um pipeline completo de CI/CD e orquestração de contêineres conforme a arquitetura da disciplina:
1. **Código-Fonte (Python REST API)**: Backend desenvolvido em Flask, conectando-se a um banco de dados relacional MySQL com criação de tabelas e retries automáticos.
2. **Automação de CI/CD (GitHub Actions)**: Pipeline que compila a imagem Docker da API a cada push na branch `main` e a publica no **GitHub Packages (GHCR)**.
3. **Servidor em Nuvem (Azure VM)**: Orquestrado via **Docker Compose** e automatizado por **Makefile**, com 3 serviços integrados:
   - **`nginx`**: Proxy Reverso recebendo requisições HTTP na porta 80 via Cloudflare DNS (`devops007.ugbio.com.br`).
   - **`api`**: Container da API Flask rodando com servidor de aplicação Gunicorn.
   - **`db`**: Container MySQL 8.4 com volume de dados persistente e verificação de saúde (*healthcheck*).

---

## 📂 Organização do Repositório

O repositório está estruturado com pastas separadas para os membros da dupla, contendo ambientes isolados e funcionais:

```text
thailancicd/
├── .gitignore                # Regras de segurança (ignora .env, caches e temporários)
├── README.md                 # Visão geral e avaliação do projeto
│
├── dyama/                    # Configurações e código de Dyama (Yamaguti)
│   ├── .env-example          # Modelo de configuração de ambiente
│   ├── docker-compose.yml    # Orquestração (MySQL, API Flask, Nginx)
│   ├── Makefile              # Comandos para deploy, build, testes e logs
│   ├── README.md             # Guia de execução específico
│   ├── api/
│   │   ├── app.py            # API REST Flask conectada ao MySQL
│   │   ├── requirements.txt  # Dependências Python
│   │   ├── Dockerfile        # Construção da imagem Docker
│   │   └── .dockerignore
│   ├── nginx/
│   │   └── default.conf      # Configuração de Proxy Reverso Nginx
│   └── .github/workflows/
│       └── ci-cd.yml         # Workflow de CI/CD para GitHub Packages (GHCR)
│
└── djotage/                  # Configurações e código de Djotage
    ├── .env-example          # Modelo de configuração de ambiente
    ├── docker-compose.yml    # Orquestração (MySQL, API Flask, Nginx)
    ├── Makefile              # Comandos para deploy, build, testes e logs
    ├── README.md             # Guia de execução específico
    ├── api/
    │   ├── app.py            # API REST Flask conectada ao MySQL
    │   ├── requirements.txt  # Dependências Python
    │   ├── Dockerfile        # Construção da imagem Docker
    │   └── .dockerignore
    ├── nginx/
    │   └── default.conf      # Configuração de Proxy Reverso Nginx
    └── .github/workflows/
        └── ci-cd.yml         # Workflow de CI/CD para GitHub Packages (GHCR)
```

---

## 🚀 Como Executar e Avaliar

Entre na pasta correspondente (`cd dyama` ou `cd djotage`):

1. **Copiar o modelo de ambiente**:
   ```bash
   cp .env-example .env
   ```

2. **Subir os serviços via Docker Compose (Build Local)**:
   ```bash
   make build
   make up
   ```

3. **Verificar os status e logs**:
   ```bash
   make status
   make logs
   ```

4. **Validar os endpoints da API**:
   ```bash
   make test
   # Ou via curl:
   curl http://localhost/
   curl http://localhost/health
   curl http://localhost/mensagens
   ```

5. **Deploy automatizado via imagem do GitHub Packages**:
   ```bash
   make deploy
   ```
