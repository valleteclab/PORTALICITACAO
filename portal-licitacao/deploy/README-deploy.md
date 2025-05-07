# Documentação de Deploy do Portal de Licitações

Este documento contém instruções detalhadas para instalação, configuração e manutenção do Portal de Licitações em um servidor VPS (Virtual Private Server).

## Índice

1. [Requisitos de Sistema](#1-requisitos-de-sistema)
2. [Instalação de Dependências](#2-instalação-de-dependências)
3. [Configuração do Banco de Dados](#3-configuração-do-banco-de-dados)
4. [Configuração do Ambiente](#4-configuração-do-ambiente)
5. [Processo de Build e Deploy](#5-processo-de-build-e-deploy)
6. [Configuração do Servidor Web](#6-configuração-do-servidor-web)
7. [Configuração de SSL/TLS](#7-configuração-de-ssltls)
8. [Backup e Restauração](#8-backup-e-restauração)
9. [Manutenção e Monitoramento](#9-manutenção-e-monitoramento)
10. [Solução de Problemas](#10-solução-de-problemas)

## 1. Requisitos de Sistema

### Hardware Recomendado

- **CPU**: 2 vCPUs ou superior
- **Memória RAM**: 4GB ou superior
- **Armazenamento**: 20GB SSD ou superior
- **Banda de Internet**: 100 Mbps ou superior

### Software Necessário

- **Sistema Operacional**: Ubuntu 20.04 LTS ou superior
- **Node.js**: v20.x LTS
- **PostgreSQL**: 14.x ou superior
- **Nginx**: Versão mais recente
- **Certbot**: Para certificados SSL Let's Encrypt

## 2. Instalação de Dependências

O script `install.sh` automatiza a instalação de todas as dependências necessárias. Para executá-lo:

```bash
sudo bash ~/portal-licitacao/deploy/install.sh
```

Este script instala:

- Node.js 20.x
- PostgreSQL
- Nginx
- Certbot para SSL
- PM2 (gerenciador de processos para Node.js)

### Instalação Manual de Dependências

Se preferir instalar manualmente, siga os passos abaixo:

#### Node.js

```bash
# Adicionar repositório NodeSource
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -

# Instalar Node.js
sudo apt install -y nodejs

# Verificar instalação
node -v
npm -v
```

#### PostgreSQL

```bash
# Instalar PostgreSQL
sudo apt install -y postgresql postgresql-contrib

# Iniciar e habilitar serviço
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### Nginx

```bash
# Instalar Nginx
sudo apt install -y nginx

# Iniciar e habilitar serviço
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### Certbot (para SSL)

```bash
# Instalar Certbot
sudo apt install -y certbot python3-certbot-nginx
```

#### PM2 (Gerenciador de Processos)

```bash
# Instalar PM2 globalmente
sudo npm install -g pm2
```

## 3. Configuração do Banco de Dados

O script de instalação configura automaticamente o banco de dados PostgreSQL. Se precisar configurar manualmente:

```bash
# Acessar PostgreSQL como usuário postgres
sudo -u postgres psql

# Criar usuário para a aplicação
CREATE USER portal_user WITH PASSWORD 'senha_segura';

# Criar banco de dados
CREATE DATABASE portal_licitacao OWNER portal_user;

# Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE portal_licitacao TO portal_user;

# Sair do PostgreSQL
\q
```

### Migrações do Banco de Dados

Para aplicar as migrações do Prisma manualmente:

```bash
cd /opt/portal-licitacao
npx prisma migrate deploy
```

## 4. Configuração do Ambiente

### Variáveis de Ambiente

O arquivo `.env` contém todas as configurações necessárias para a aplicação. Um modelo está disponível em `.env.example`.

```bash
# Copiar arquivo de exemplo
cp ~/portal-licitacao/deploy/.env.example /opt/portal-licitacao/.env

# Editar com valores reais
nano /opt/portal-licitacao/.env
```

Variáveis importantes a serem configuradas:

- `DATABASE_URL`: URL de conexão com o banco de dados
- `JWT_SECRET`: Chave secreta para autenticação
- `NEXT_PUBLIC_SITE_URL`: URL pública do site
- `PNCP_API_KEY`: Chave de API para integração com o PNCP

### Permissões de Arquivos

```bash
# Definir permissões corretas
sudo chown -R portal:portal /opt/portal-licitacao
sudo chmod 600 /opt/portal-licitacao/.env
```

## 5. Processo de Build e Deploy

### Instalação de Dependências do Projeto

```bash
cd /opt/portal-licitacao
npm install
```

### Build da Aplicação

```bash
cd /opt/portal-licitacao
npm run build
```

### Iniciar a Aplicação

Usando PM2:

```bash
cd /opt/portal-licitacao
pm2 start npm --name "portal-licitacao" -- start
pm2 save
pm2 startup
```

Usando systemd:

```bash
# Copiar arquivo de serviço
sudo cp ~/portal-licitacao/deploy/portal-licitacao.service /etc/systemd/system/

# Recarregar systemd
sudo systemctl daemon-reload

# Iniciar e habilitar serviço
sudo systemctl start portal-licitacao
sudo systemctl enable portal-licitacao
```

## 6. Configuração do Servidor Web

### Configuração do Nginx

```bash
# Copiar arquivo de configuração
sudo cp ~/portal-licitacao/deploy/nginx_portal_licitacao.conf /etc/nginx/sites-available/portal-licitacao

# Editar o arquivo para ajustar o domínio
sudo nano /etc/nginx/sites-available/portal-licitacao

# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/portal-licitacao /etc/nginx/sites-enabled/

# Remover configuração padrão (opcional)
sudo rm /etc/nginx/sites-enabled/default

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Configuração de Cache e Compressão

A configuração do Nginx já inclui otimizações de cache e compressão gzip para melhor performance.

## 7. Configuração de SSL/TLS

### Obter Certificado SSL com Let's Encrypt

```bash
sudo certbot --nginx -d seu-dominio.com.br
```

O Certbot irá modificar automaticamente a configuração do Nginx para usar HTTPS.

### Renovação Automática de Certificados

O Certbot configura automaticamente um cron job para renovação dos certificados. Para testar:

```bash
sudo certbot renew --dry-run
```

## 8. Backup e Restauração

### Backup Manual

```bash
sudo /usr/local/bin/portal-backup
```

Ou diretamente:

```bash
sudo bash ~/portal-licitacao/deploy/backup.sh
```

### Restauração de Backup

```bash
sudo bash ~/portal-licitacao/deploy/restore.sh /caminho/para/arquivo_backup.tar.gz
```

### Backup Automático

O script de instalação configura um backup diário às 2h da manhã. Para modificar:

```bash
sudo crontab -e
```

Exemplo de configuração:

```
0 2 * * * /usr/local/bin/portal-backup
```

## 9. Manutenção e Monitoramento

### Monitoramento com PM2

```bash
# Verificar status da aplicação
pm2 status

# Visualizar logs
pm2 logs portal-licitacao

# Monitoramento em tempo real
pm2 monit
```

### Logs do Sistema

```bash
# Logs do Nginx
sudo tail -f /var/log/nginx/portal-licitacao-access.log
sudo tail -f /var/log/nginx/portal-licitacao-error.log

# Logs do PostgreSQL
sudo tail -f /var/log/postgresql/postgresql-14-main.log

# Logs do sistema
sudo journalctl -u portal-licitacao -f
```

### Atualizações do Sistema

```bash
# Atualizar pacotes do sistema
sudo apt update && sudo apt upgrade -y

# Reiniciar servidor (se necessário)
sudo reboot
```

### Atualizações da Aplicação

```bash
cd /opt/portal-licitacao
git pull
npm install
npm run build
pm2 restart portal-licitacao
```

## 10. Solução de Problemas

### Problemas de Conexão com o Banco de Dados

Verifique se o PostgreSQL está rodando:

```bash
sudo systemctl status postgresql
```

Verifique as credenciais no arquivo `.env`.

### Problemas com o Nginx

Verifique a sintaxe da configuração:

```bash
sudo nginx -t
```

Verifique os logs de erro:

```bash
sudo tail -f /var/log/nginx/error.log
```

### Problemas com a Aplicação Node.js

Verifique os logs da aplicação:

```bash
pm2 logs portal-licitacao
```

Verifique se todas as dependências estão instaladas:

```bash
cd /opt/portal-licitacao
npm install
```

### Problemas com Certificados SSL

Verifique o status do Certbot:

```bash
sudo certbot certificates
```

Tente renovar manualmente:

```bash
sudo certbot renew --force-renewal
```

---

## Informações Adicionais

### Estrutura de Diretórios

```
/opt/portal-licitacao/         # Diretório principal da aplicação
├── .next/                     # Build da aplicação Next.js
├── node_modules/              # Dependências do Node.js
├── prisma/                    # Esquemas e migrações do Prisma
├── public/                    # Arquivos estáticos públicos
├── src/                       # Código-fonte da aplicação
├── uploads/                   # Diretório de uploads (se aplicável)
├── .env                       # Variáveis de ambiente
└── package.json               # Configuração do projeto

/var/backups/portal-licitacao/ # Diretório de backups
```

### Contatos de Suporte

Para suporte técnico, entre em contato com:

- Email: suporte@exemplo.com.br
- Telefone: (XX) XXXX-XXXX

---

Documentação criada em: Maio de 2025
