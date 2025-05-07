#!/bin/bash
# Script de instalação rápida para o Portal de Licitações
# Este script baixa o repositório e executa o instalador principal

# Cores para melhor visualização
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para exibir mensagens de progresso
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Função para exibir avisos
warn() {
    echo -e "${YELLOW}[AVISO]${NC} $1"
}

# Função para exibir erros
error() {
    echo -e "${RED}[ERRO]${NC} $1"
    exit 1
}

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    error "Este script precisa ser executado como root (sudo)."
fi

log "Iniciando instalação rápida do Portal de Licitações..."

# Verificar se git está instalado
if ! command -v git &> /dev/null; then
    log "Instalando git..."
    apt update && apt install -y git || error "Falha ao instalar git."
fi

# Solicitar URL do repositório
read -p "Digite a URL do repositório Git do Portal de Licitações: " REPO_URL
if [ -z "$REPO_URL" ]; then
    error "URL do repositório não pode ser vazia."
fi

# Diretório temporário para clone
TEMP_DIR=$(mktemp -d)
log "Clonando repositório em $TEMP_DIR..."

# Clonar repositório
git clone "$REPO_URL" "$TEMP_DIR" || error "Falha ao clonar repositório."

# Verificar se o diretório deploy existe no repositório
if [ ! -d "$TEMP_DIR/deploy" ]; then
    error "Diretório 'deploy' não encontrado no repositório."
fi

# Criar diretório de destino
mkdir -p /opt/portal-licitacao || error "Falha ao criar diretório de destino."

# Copiar arquivos de deploy
log "Copiando arquivos de instalação..."
cp -r "$TEMP_DIR/deploy" /opt/portal-licitacao/ || error "Falha ao copiar arquivos de deploy."

# Tornar scripts executáveis
chmod +x /opt/portal-licitacao/deploy/*.sh || warn "Falha ao definir permissões de execução."

# Limpar diretório temporário
rm -rf "$TEMP_DIR"

log "Arquivos de instalação copiados com sucesso."
log "Iniciando instalação principal..."

# Executar instalador principal
bash /opt/portal-licitacao/deploy/install.sh || error "Falha durante a instalação principal."

log "Instalação rápida concluída com sucesso!"
log "Consulte a documentação em /opt/portal-licitacao/deploy/README-deploy.md para mais informações."
