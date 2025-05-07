# Portal de Licitações - Scripts de Deploy

Este diretório contém scripts e arquivos de configuração para facilitar o deploy do Portal de Licitações em um servidor VPS.

## Arquivos Disponíveis

- **install.sh**: Script principal de instalação que configura todo o ambiente
- **backup.sh**: Script para realizar backup do banco de dados e arquivos importantes
- **restore.sh**: Script para restaurar o sistema a partir de um backup
- **quick-install.sh**: Script para instalação rápida a partir do repositório
- **portal-licitacao.service**: Arquivo de configuração do systemd
- **nginx_portal_licitacao.conf**: Arquivo de configuração do Nginx
- **.env.example**: Exemplo de arquivo de variáveis de ambiente
- **README-deploy.md**: Documentação detalhada de deploy

## Instalação Rápida

Para realizar uma instalação rápida em um servidor novo:

```bash
# Baixar o script de instalação rápida
wget -O quick-install.sh https://raw.githubusercontent.com/seu-usuario/portal-licitacao/main/deploy/quick-install.sh

# Tornar o script executável
chmod +x quick-install.sh

# Executar o script (como root ou com sudo)
sudo ./quick-install.sh
```

## Instalação Manual

Para realizar a instalação manual:

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/portal-licitacao.git
   ```

2. Execute o script de instalação:
   ```bash
   cd portal-licitacao
   sudo ./deploy/install.sh
   ```

3. Siga as instruções na tela para completar a instalação.

## Documentação Detalhada

Para instruções detalhadas sobre instalação, configuração e manutenção, consulte o arquivo [README-deploy.md](README-deploy.md).

## Requisitos Mínimos

- Ubuntu 20.04 LTS ou superior
- 2 vCPUs
- 4GB de RAM
- 20GB de espaço em disco
- Conexão com a internet

## Suporte

Para suporte técnico, entre em contato com a equipe de desenvolvimento.
