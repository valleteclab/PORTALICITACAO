#!/bin/bash
# Script de backup para o Portal de Licitações
# Este script realiza backup do banco de dados PostgreSQL e arquivos importantes da aplicação

# Definir variáveis
APP_NAME="portal-licitacao"
APP_DIR="/opt/$APP_NAME"
BACKUP_DIR="/var/backups/$APP_NAME"
DB_NAME="portal_licitacao"
DB_USER="portal_user"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/${APP_NAME}_backup_$DATE.tar.gz"

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

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR || error "Falha ao criar diretório de backup."

# Criar diretório temporário para o backup
TEMP_DIR=$(mktemp -d)
log "Criando backup temporário em $TEMP_DIR"

# Backup do banco de dados
log "Realizando backup do banco de dados PostgreSQL..."
sudo -u postgres pg_dump $DB_NAME > $TEMP_DIR/database.sql || error "Falha ao realizar backup do banco de dados."

# Backup dos arquivos de configuração
log "Realizando backup dos arquivos de configuração..."
cp $APP_DIR/.env $TEMP_DIR/.env || warn "Arquivo .env não encontrado."
cp -r $APP_DIR/public $TEMP_DIR/public 2>/dev/null || warn "Diretório public não encontrado."

# Backup de uploads (se existir)
if [ -d "$APP_DIR/uploads" ]; then
    log "Realizando backup dos arquivos de upload..."
    cp -r $APP_DIR/uploads $TEMP_DIR/uploads || warn "Falha ao copiar diretório de uploads."
fi

# Backup de configurações do Nginx
log "Realizando backup das configurações do Nginx..."
cp /etc/nginx/sites-available/$APP_NAME $TEMP_DIR/nginx_config || warn "Arquivo de configuração do Nginx não encontrado."

# Backup de configurações do PM2
log "Realizando backup das configurações do PM2..."
sudo -u portal pm2 save
cp /home/portal/.pm2/dump.pm2 $TEMP_DIR/pm2_dump.json 2>/dev/null || warn "Arquivo de configuração do PM2 não encontrado."

# Compactar todos os arquivos
log "Compactando arquivos de backup..."
tar -czf $BACKUP_FILE -C $TEMP_DIR . || error "Falha ao compactar arquivos de backup."

# Limpar diretório temporário
rm -rf $TEMP_DIR

# Definir permissões corretas
chmod 600 $BACKUP_FILE

# Manter apenas os últimos 7 backups diários
log "Removendo backups antigos..."
ls -tp $BACKUP_DIR/${APP_NAME}_backup_*.tar.gz | grep -v '/$' | tail -n +8 | xargs -I {} rm -- {} 2>/dev/null

# Exibir informações do backup
BACKUP_SIZE=$(du -h $BACKUP_FILE | cut -f1)
log "Backup concluído com sucesso!"
log "Arquivo: $BACKUP_FILE"
log "Tamanho: $BACKUP_SIZE"
log "Data: $(date)"

# Opcional: Enviar backup para armazenamento externo
# Descomente e configure as linhas abaixo para habilitar backup externo

# Backup para servidor remoto via SCP
#REMOTE_USER="backup"
#REMOTE_HOST="backup-server.example.com"
#REMOTE_DIR="/backups/$APP_NAME"
#log "Enviando backup para servidor remoto..."
#scp $BACKUP_FILE $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/ || warn "Falha ao enviar backup para servidor remoto."

# Backup para Amazon S3
#S3_BUCKET="my-backup-bucket"
#log "Enviando backup para Amazon S3..."
#aws s3 cp $BACKUP_FILE s3://$S3_BUCKET/$APP_NAME/ || warn "Falha ao enviar backup para Amazon S3."
