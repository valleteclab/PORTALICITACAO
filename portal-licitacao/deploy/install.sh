#!/bin/bash
# Script de instalação do Portal de Licitações
# Este script automatiza a instalação e configuração do Portal de Licitações em uma VPS

set -e  # Encerra o script se qualquer comando falhar

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

# Definir variáveis
APP_NAME="portal-licitacao"
APP_DIR="/opt/$APP_NAME"
DEPLOY_USER="portal"
DB_NAME="portal_licitacao"
DB_USER="portal_user"
NODE_VERSION="20.x"  # Versão LTS recomendada
DOMAIN=""  # Será solicitado durante a instalação

log "Iniciando instalação do Portal de Licitações..."

# Solicitar o domínio para configuração
read -p "Digite o domínio para o portal (ex: licitacoes.prefeitura.gov.br): " DOMAIN
if [ -z "$DOMAIN" ]; then
    error "Domínio não pode ser vazio."
fi

# Gerar senha aleatória para o banco de dados
DB_PASSWORD=$(openssl rand -base64 16)

# Atualizar o sistema
log "Atualizando o sistema..."
apt update && apt upgrade -y || error "Falha ao atualizar o sistema."

# Instalar dependências básicas
log "Instalando dependências básicas..."
apt install -y curl wget git build-essential ca-certificates gnupg lsb-release || error "Falha ao instalar dependências básicas."

# Instalar Node.js
log "Instalando Node.js $NODE_VERSION..."
mkdir -p /etc/apt/keyrings
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_VERSION nodistro main" | tee /etc/apt/sources.list.d/nodesource.list
apt update && apt install -y nodejs || error "Falha ao instalar Node.js."

# Verificar a instalação do Node.js
node -v || error "Node.js não foi instalado corretamente."
npm -v || error "NPM não foi instalado corretamente."

# Instalar PM2 globalmente
log "Instalando PM2 para gerenciamento de processos..."
npm install -g pm2 || error "Falha ao instalar PM2."

# Instalar PostgreSQL
log "Instalando PostgreSQL..."
apt install -y postgresql postgresql-contrib || error "Falha ao instalar PostgreSQL."

# Verificar se o PostgreSQL está rodando
systemctl is-active --quiet postgresql || systemctl start postgresql

# Criar usuário e banco de dados
log "Configurando banco de dados PostgreSQL..."
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" || warn "Usuário do banco de dados já pode existir."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" || warn "Banco de dados já pode existir."
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" || warn "Privilégios já podem estar configurados."

# Instalar Nginx
log "Instalando e configurando Nginx..."
apt install -y nginx || error "Falha ao instalar Nginx."

# Instalar Certbot para SSL
log "Instalando Certbot para certificados SSL..."
apt install -y certbot python3-certbot-nginx || error "Falha ao instalar Certbot."

# Criar usuário para a aplicação
log "Criando usuário para a aplicação..."
id -u $DEPLOY_USER &>/dev/null || useradd -m -s /bin/bash $DEPLOY_USER || error "Falha ao criar usuário."

# Criar diretório da aplicação
log "Configurando diretório da aplicação..."
mkdir -p $APP_DIR
chown -R $DEPLOY_USER:$DEPLOY_USER $APP_DIR

# Clonar o repositório (substitua com o URL real do repositório)
log "Clonando o repositório do projeto..."
read -p "Digite a URL do repositório Git (deixe em branco para pular): " GIT_REPO
if [ ! -z "$GIT_REPO" ]; then
    su - $DEPLOY_USER -c "git clone $GIT_REPO $APP_DIR" || error "Falha ao clonar o repositório."
else
    warn "Etapa de clonagem pulada. Você precisará copiar os arquivos manualmente para $APP_DIR."
fi

# Configurar arquivo .env
log "Configurando variáveis de ambiente..."
if [ -f "$APP_DIR/.env.example" ]; then
    cp $APP_DIR/.env.example $APP_DIR/.env
    # Atualizar as variáveis do banco de dados no .env
    sed -i "s/DATABASE_URL=.*/DATABASE_URL=postgresql:\/\/$DB_USER:$DB_PASSWORD@localhost:5432\/$DB_NAME/" $APP_DIR/.env
    # Adicionar outras variáveis de ambiente necessárias
    echo "NEXT_PUBLIC_SITE_URL=https://$DOMAIN" >> $APP_DIR/.env
else
    # Criar arquivo .env básico se não existir .env.example
    cat > $APP_DIR/.env << EOF
# Configurações do Banco de Dados
DATABASE_URL=postgresql://$DB_USER:$DB_PASSWORD@localhost:5432/$DB_NAME

# Configurações da Aplicação
NODE_ENV=production
NEXT_PUBLIC_SITE_URL=https://$DOMAIN

# Configurações de Segurança
# Gere uma chave secreta com: openssl rand -base64 32
JWT_SECRET=$(openssl rand -base64 32)
EOF
fi

# Ajustar permissões
chown $DEPLOY_USER:$DEPLOY_USER $APP_DIR/.env

# Instalar dependências e fazer build da aplicação
log "Instalando dependências e construindo a aplicação..."
cd $APP_DIR
su - $DEPLOY_USER -c "cd $APP_DIR && npm install" || error "Falha ao instalar dependências."
su - $DEPLOY_USER -c "cd $APP_DIR && npm run build" || error "Falha ao construir a aplicação."

# Configurar o Prisma (se necessário)
if [ -f "$APP_DIR/prisma/schema.prisma" ]; then
    log "Executando migrações do Prisma..."
    su - $DEPLOY_USER -c "cd $APP_DIR && npx prisma migrate deploy" || warn "Falha ao executar migrações do Prisma."
fi

# Configurar PM2
log "Configurando PM2 para gerenciar a aplicação..."
su - $DEPLOY_USER -c "cd $APP_DIR && pm2 start npm --name \"$APP_NAME\" -- start" || error "Falha ao iniciar a aplicação com PM2."
su - $DEPLOY_USER -c "pm2 save" || warn "Falha ao salvar configuração do PM2."
su - $DEPLOY_USER -c "pm2 startup" | tail -n 1 > /tmp/pm2_startup_command
chmod +x /tmp/pm2_startup_command
/bin/bash /tmp/pm2_startup_command || warn "Falha ao configurar inicialização automática do PM2."

# Configurar Nginx
log "Configurando Nginx..."
cat > /etc/nginx/sites-available/$APP_NAME << EOF
server {
    listen 80;
    server_name $DOMAIN;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Configuração para servir arquivos estáticos
    location /_next/static/ {
        alias $APP_DIR/.next/static/;
        expires 365d;
        access_log off;
    }

    location /public/ {
        alias $APP_DIR/public/;
        expires 365d;
        access_log off;
    }

    # Configurações adicionais para segurança
    add_header X-Frame-Options "SAMEORIGIN";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
}
EOF

# Ativar o site no Nginx
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/ || error "Falha ao ativar site no Nginx."
rm -f /etc/nginx/sites-enabled/default  # Remover o site padrão

# Testar configuração do Nginx
nginx -t || error "Configuração do Nginx inválida."

# Reiniciar Nginx
systemctl restart nginx || error "Falha ao reiniciar Nginx."

# Configurar SSL com Certbot
log "Configurando certificado SSL com Certbot..."
certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN || warn "Falha ao configurar SSL. Você pode executar 'certbot --nginx' manualmente depois."

# Configurar firewall (se instalado)
if command -v ufw &> /dev/null; then
    log "Configurando firewall..."
    ufw allow 'Nginx Full' || warn "Falha ao configurar regra do firewall para Nginx."
    ufw allow ssh || warn "Falha ao configurar regra do firewall para SSH."
    ufw --force enable || warn "Falha ao ativar firewall."
fi

# Criar scripts de backup
log "Configurando scripts de backup..."
cp ~/portal-licitacao/deploy/backup.sh /usr/local/bin/portal-backup
chmod +x /usr/local/bin/portal-backup

# Configurar backup automático (diário às 2h da manhã)
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/portal-backup") | crontab -

log "Instalação concluída com sucesso!"
log "Portal de Licitações está disponível em: https://$DOMAIN"
log "Senha do banco de dados: $DB_PASSWORD (guarde em um local seguro)"
log "Para verificar o status da aplicação: sudo su - $DEPLOY_USER -c 'pm2 status'"

# Instruções finais
cat << EOF

=====================================================================
                PORTAL DE LICITAÇÕES - INSTRUÇÕES FINAIS
=====================================================================

1. Verifique se a aplicação está rodando:
   $ sudo su - $DEPLOY_USER -c 'pm2 status'

2. Para reiniciar a aplicação:
   $ sudo su - $DEPLOY_USER -c 'pm2 restart $APP_NAME'

3. Para visualizar logs:
   $ sudo su - $DEPLOY_USER -c 'pm2 logs $APP_NAME'

4. Backup manual:
   $ sudo /usr/local/bin/portal-backup

5. Senha do banco de dados: $DB_PASSWORD
   (Guarde esta senha em um local seguro)

6. Acesse o portal em: https://$DOMAIN

=====================================================================
EOF
