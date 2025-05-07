#!/bin/bash
# Script de restauração para o Portal de Licitações
# Este script restaura o banco de dados e arquivos importantes da aplicação a partir de um backup

# Definir variáveis
APP_NAME="portal-licitacao"
APP_DIR="/opt/$APP_NAME"
BACKUP_DIR="/var/backups/$APP_NAME"
DB_NAME="portal_licitacao"
DB_USER="portal_user"
DEPLOY_USER="portal"

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

# Verificar se o arquivo de backup foi fornecido
if [ -z "$1" ]; then
    echo "Uso: $0 <arquivo_de_backup.tar.gz>"
    echo "Backups disponíveis:"
    ls -lh $BACKUP_DIR/*.tar.gz 2>/dev/null || echo "Nenhum backup encontrado em $BACKUP_DIR"
    exit 1
fi

BACKUP_FILE="$1"

# Verificar se o arquivo de backup existe
if [ ! -f "$BACKUP_FILE" ]; then
    # Verificar se é um caminho relativo no diretório de backup
    if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
        BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE"
    else
        error "Arquivo de backup não encontrado: $BACKUP_FILE"
    fi
fi

log "Iniciando restauração a partir de: $BACKUP_FILE"

# Confirmar a restauração
read -p "ATENÇÃO: Esta operação irá substituir o banco de dados e arquivos da aplicação. Continuar? (s/N): " CONFIRM
if [[ ! "$CONFIRM" =~ ^[Ss]$ ]]; then
    log "Operação cancelada pelo usuário."
    exit 0
fi

# Criar diretório temporário para extração
TEMP_DIR=$(mktemp -d)
log "Extraindo backup em $TEMP_DIR..."

# Extrair o arquivo de backup
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR" || error "Falha ao extrair arquivo de backup."

# Parar a aplicação
log "Parando a aplicação..."
systemctl stop nginx || warn "Falha ao parar Nginx."
su - $DEPLOY_USER -c "pm2 stop $APP_NAME" || warn "Falha ao parar aplicação via PM2."

# Restaurar banco de dados
if [ -f "$TEMP_DIR/database.sql" ]; then
    log "Restaurando banco de dados..."
    # Dropar e recriar o banco de dados
    sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;" || warn "Falha ao dropar banco de dados."
    sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" || error "Falha ao criar banco de dados."
    # Restaurar dados
    sudo -u postgres psql -d $DB_NAME -f "$TEMP_DIR/database.sql" || error "Falha ao restaurar banco de dados."
else
    warn "Arquivo de backup do banco de dados não encontrado."
fi

# Restaurar arquivos de configuração
if [ -f "$TEMP_DIR/.env" ]; then
    log "Restaurando arquivo .env..."
    cp "$TEMP_DIR/.env" "$APP_DIR/.env" || warn "Falha ao restaurar arquivo .env."
    chown $DEPLOY_USER:$DEPLOY_USER "$APP_DIR/.env"
fi

# Restaurar diretório public
if [ -d "$TEMP_DIR/public" ]; then
    log "Restaurando diretório public..."
    cp -r "$TEMP_DIR/public" "$APP_DIR/" || warn "Falha ao restaurar diretório public."
    chown -R $DEPLOY_USER:$DEPLOY_USER "$APP_DIR/public"
fi

# Restaurar diretório uploads (se existir)
if [ -d "$TEMP_DIR/uploads" ]; then
    log "Restaurando diretório uploads..."
    cp -r "$TEMP_DIR/uploads" "$APP_DIR/" || warn "Falha ao restaurar diretório uploads."
    chown -R $DEPLOY_USER:$DEPLOY_USER "$APP_DIR/uploads"
fi

# Restaurar configuração do Nginx
if [ -f "$TEMP_DIR/nginx_config" ]; then
    log "Restaurando configuração do Nginx..."
    cp "$TEMP_DIR/nginx_config" "/etc/nginx/sites-available/$APP_NAME" || warn "Falha ao restaurar configuração do Nginx."
fi

# Restaurar configuração do PM2 (opcional)
if [ -f "$TEMP_DIR/pm2_dump.json" ]; then
    log "Restaurando configuração do PM2..."
    cp "$TEMP_DIR/pm2_dump.json" "/home/$DEPLOY_USER/.pm2/dump.pm2" || warn "Falha ao restaurar configuração do PM2."
    chown $DEPLOY_USER:$DEPLOY_USER "/home/$DEPLOY_USER/.pm2/dump.pm2"
fi

# Limpar diretório temporário
rm -rf "$TEMP_DIR"

# Reiniciar serviços
log "Reiniciando serviços..."
su - $DEPLOY_USER -c "cd $APP_DIR && pm2 restart $APP_NAME" || warn "Falha ao reiniciar aplicação via PM2."
systemctl restart nginx || warn "Falha ao reiniciar Nginx."

log "Restauração concluída com sucesso!"
log "Verifique se a aplicação está funcionando corretamente acessando o site."
log "Para verificar o status da aplicação: sudo su - $DEPLOY_USER -c 'pm2 status'"
