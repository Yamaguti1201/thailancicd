SHELL := /bin/bash

VERSION ?= latest

-include .env
export

.PHONY: deploy login pull up down status logs build test clean restart

deploy: login pull up
	@echo ""
	@echo "========================================="
	@echo " Deploy concluído com sucesso! (devops007)"
	@echo " Imagem: $(IMAGE_NAME):$(VERSION)"
	@echo " Domínio: $(DOMAIN)"
	@echo " Dupla: Dyama (Yamaguti) & Djotage"
	@echo "========================================="

login:
	@echo "Autenticando no GitHub Packages (GHCR)..."
	@echo "$(GHCR_TOKEN)" | docker login ghcr.io -u "$(GHCR_USER)" --password-stdin

pull:
	@echo "Baixando imagem $(IMAGE_NAME):$(VERSION)..."
	@IMAGE_NAME="$(IMAGE_NAME)" VERSION="$(VERSION)" docker compose pull api

build:
	@echo "Construindo imagens localmente..."
	@IMAGE_NAME="$(IMAGE_NAME)" VERSION="$(VERSION)" docker compose build

up:
	@echo "Subindo os serviços (DB, API, NGINX)..."
	@IMAGE_NAME="$(IMAGE_NAME)" VERSION="$(VERSION)" docker compose up -d

down:
	@echo "Parando os serviços..."
	@docker compose down

restart: down up

status:
	@docker compose ps

logs:
	@docker compose logs -f

logs-api:
	@docker compose logs -f api

logs-db:
	@docker compose logs -f db

test:
	@echo "Testando endpoints da API via Nginx..."
	@echo "1. Healthcheck:"
	@curl -s http://localhost:$(HOST_PORT)/health || echo "Erro ao testar /health"
	@echo ""
	@echo "2. Rota principal (/):"
	@curl -s http://localhost:$(HOST_PORT)/ || echo "Erro ao testar /"
	@echo ""
	@echo "3. Mensagens cadastradas (/mensagens):"
	@curl -s http://localhost:$(HOST_PORT)/mensagens || echo "Erro ao testar /mensagens"
	@echo ""

clean:
	@echo "Parando containers e removendo volumes de dados..."
	@docker compose down -v
