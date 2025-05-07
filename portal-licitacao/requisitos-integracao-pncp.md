# Relatório Técnico: Requisitos de Integração com o PNCP

## 1. Introdução

Este documento apresenta os requisitos técnicos para integração com o Portal Nacional de Contratações Públicas (PNCP), conforme análise do manual de integração e da documentação da API disponibilizada pelo portal. O objetivo é fornecer as informações necessárias para o desenvolvimento do portal de licitação para câmaras de vereadores e prefeituras da região oeste da Bahia, garantindo conformidade com a Lei nº 14.133/2021 (Nova Lei de Licitações e Contratos Administrativos).

## 2. Contexto Legal

A Lei nº 14.133/2021 estabelece a obrigatoriedade de divulgação centralizada dos atos relacionados às licitações e contratos no PNCP (Art. 174). A integração com o PNCP é, portanto, um requisito fundamental para qualquer portal de licitação, visando garantir a transparência, controle e integração dos processos de contratação pública.

## 3. Visão Geral da API do PNCP

O PNCP disponibiliza uma API REST para integração com sistemas externos, permitindo o acesso e a manutenção de dados relacionados a contratações públicas. A API segue o padrão OpenAPI 3.0.1 e oferece endpoints para consulta e manutenção de informações sobre órgãos, unidades, contratações, contratos, atas de registro de preço e planos de contratação.

### 3.1 Ambientes Disponíveis

O PNCP disponibiliza dois ambientes para integração:

1. **Ambiente de Treinamento**:
   - Portal: https://treina.pncp.gov.br
   - Documentação Técnica (Swagger): https://treina.pncp.gov.br/api/pncp/swagger-ui/index.html
   - Base URL para serviços: https://treina.pncp.gov.br/api/pncp

2. **Ambiente de Produção**:
   - Portal: https://pncp.gov.br
   - Documentação Técnica (Swagger): https://pncp.gov.br/api/pncp/swagger-ui/index.html
   - Base URL para serviços: https://pncp.gov.br/api/pncp

## 4. Autenticação e Autorização

### 4.1 Método de Autenticação

A API do PNCP utiliza autenticação baseada em JSON Web Token (JWT). O processo de autenticação segue os seguintes passos:

1. A plataforma usuária deve se autenticar com login e senha para obter um JWT.
2. A autenticação é realizada através do endpoint: `POST https://pncp.gov.br/api/pncp/v1/usuarios/login`
3. O token JWT é retornado no cabeçalho (header) da resposta HTTP, no campo "Authorization", após o texto "Bearer".
4. Todas as requisições subsequentes às APIs de manutenção de dados devem incluir este token no cabeçalho "Authorization".

### 4.2 Acesso Público vs. Restrito

- O acesso ao Portal de consultas é público.
- As APIs de manutenção (serviços de inserção, alteração e exclusão) requerem autenticação.

### 4.3 Renovação de Token

O token JWT tem um tempo de validade limitado. É importante implementar um mecanismo de renovação do token quando expirado, para garantir a continuidade do acesso às APIs de manutenção.

## 5. Formato de Dados e Comunicação

- **Protocolo**: REST sobre HTTP/1.1
- **Formato de Dados**: JSON para requisições e respostas
- **Codificação de Caracteres**: UTF-8
- **Headers de Requisição**:
  - Content-Type: application/json
  - Authorization: Bearer {token}
  - Accept: application/json

## 6. Principais Endpoints da API

A API do PNCP é organizada em diferentes recursos, cada um com seus próprios endpoints. Abaixo estão os principais endpoints identificados:

### 6.1 Autenticação

- **POST /v1/usuarios/login**: Autenticação de usuários para obtenção do token JWT

### 6.2 Gestão de Usuários

- **GET /v1/usuarios/{id}**: Consulta de usuário por ID
- **PUT /v1/usuarios/{id}**: Atualização de usuário
- **GET /v1/usuarios**: Consulta de usuários

### 6.3 Gestão de Órgãos

- **POST /v1/orgaos**: Cadastro de órgão
- **GET /v1/orgaos/{cnpj}**: Consulta de órgão por CNPJ

### 6.4 Gestão de Unidades

- **POST /v1/orgaos/{cnpj}/unidades**: Cadastro de unidade
- **GET /v1/orgaos/{cnpj}/unidades/{codigo}**: Consulta de unidade por código
- **GET /v1/orgaos/{cnpj}/unidades**: Consulta de unidades de um órgão

### 6.5 Gestão de Compras/Contratações

- **POST /v1/orgaos/{cnpj}/compras**: Cadastro de compra/contratação
- **PUT /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}**: Atualização de compra/contratação
- **PATCH /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}**: Atualização parcial de compra/contratação
- **DELETE /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}**: Exclusão de compra/contratação
- **GET /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}**: Consulta de compra/contratação

### 6.6 Gestão de Documentos

- **POST /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos**: Upload de documentos
- **DELETE /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos/{id}**: Exclusão de documento
- **GET /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/arquivos/{id}**: Download de documento

### 6.7 Gestão de Itens de Compra

- **POST /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens**: Cadastro de itens de compra
- **PUT /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens/{numero}**: Atualização de item de compra
- **GET /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens/{numero}**: Consulta de item de compra

### 6.8 Gestão de Resultados de Itens

- **POST /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens/{numero}/resultados**: Cadastro de resultado de item
- **PUT /v1/orgaos/{cnpj}/compras/{ano}/{sequencial}/itens/{numero}/resultados/{id}**: Atualização de resultado de item

### 6.9 Gestão de Contratos

- **GET /v1/contratos**: Consulta de contratos por data de publicação
- **GET /v1/contratos/atualizacao**: Consulta de contratos por data de atualização

### 6.10 Consulta de Contratações

- **GET /v1/contratacoes/publicacao**: Consulta de contratações por data de publicação
- **GET /v1/contratacoes/proposta**: Consulta de contratações com recebimento de propostas aberto
- **GET /v1/contratacoes/atualizacao**: Consulta de contratações por data de atualização

### 6.11 Gestão de Atas de Registro de Preço

- **GET /v1/atas**: Consulta de atas por período de vigência
- **GET /v1/atas/atualizacao**: Consulta de atas por data de atualização

### 6.12 Plano de Contratação

- **GET /v1/pca/**: Consulta de itens de PCA por ano e código de classificação
- **GET /v1/pca/atualizacao**: Consulta de PCA por data de atualização
- **GET /v1/pca/usuario**: Consulta de itens de PCA por usuário

## 7. Paginação de Resultados

A API do PNCP implementa paginação para endpoints que retornam múltiplos registros. Os parâmetros de paginação incluem:

- **pagina**: Número da página (começando em 1)
- **tamanhoPagina**: Quantidade de registros por página (mínimo 10, máximo 500 para a maioria dos endpoints, máximo 50 para endpoints de contratação)

A resposta inclui metadados de paginação:
- **totalRegistros**: Total de registros encontrados
- **totalPaginas**: Total de páginas
- **numeroPagina**: Número da página atual
- **paginasRestantes**: Número de páginas restantes
- **empty**: Indica se o resultado está vazio

## 8. Tratamento de Erros

A API do PNCP retorna códigos de status HTTP padrão para indicar o resultado da requisição:

- **200 OK**: Requisição bem-sucedida
- **204 No Content**: Requisição bem-sucedida, sem conteúdo para retornar
- **400 Bad Request**: Requisição inválida
- **401 Unauthorized**: Falha na autenticação
- **422 Unprocessable Entity**: Erro de validação dos dados enviados
- **500 Internal Server Error**: Erro interno do servidor

As respostas de erro geralmente incluem informações detalhadas sobre o problema, como mensagem de erro, caminho da requisição, timestamp e status.

## 9. Envio de Arquivos

A API do PNCP permite o envio de arquivos através de endpoints específicos para documentos. Os formatos de arquivo aceitos incluem:

- PDF
- DOC/DOCX
- XLS/XLSX
- PPT/PPTX
- TXT
- CSV
- ZIP
- RAR
- JPG/JPEG
- PNG
- GIF

O tamanho máximo dos arquivos pode variar, sendo importante verificar as limitações específicas na documentação.

## 10. Fluxos de Integração

### 10.1 Fluxo Básico de Integração

1. **Autenticação**: Obter token JWT através do endpoint de login
2. **Cadastro de Órgão**: Registrar o órgão no PNCP (se ainda não estiver cadastrado)
3. **Cadastro de Unidades**: Registrar as unidades administrativas do órgão
4. **Publicação de Contratações**: Registrar as contratações (licitações, dispensas, etc.)
5. **Upload de Documentos**: Enviar os documentos relacionados às contratações
6. **Registro de Itens**: Cadastrar os itens da contratação
7. **Registro de Resultados**: Informar os resultados dos itens após a conclusão do processo
8. **Registro de Contratos**: Cadastrar os contratos resultantes das contratações

### 10.2 Fluxo de Consulta

1. **Autenticação**: Obter token JWT (se necessário para consultas restritas)
2. **Consulta de Contratações**: Buscar contratações por diferentes critérios
3. **Consulta de Contratos**: Buscar contratos por diferentes critérios
4. **Consulta de Atas**: Buscar atas de registro de preço
5. **Consulta de Planos de Contratação**: Buscar informações sobre planos de contratação

## 11. Considerações para Implementação

### 11.1 Boas Práticas

- **Ambiente de Testes**: Utilizar o ambiente de treinamento para testes antes de integrar com o ambiente de produção
- **Cache**: Implementar cache para reduzir o número de requisições à API
- **Validação de Dados**: Validar os dados antes de enviá-los para a API
- **Tratamento de Erros**: Implementar tratamento de erros robusto
- **Logs**: Manter logs detalhados das interações com a API para fins de auditoria
- **Segurança**: Armazenar credenciais e tokens de forma segura
- **Renovação de Token**: Implementar mecanismo de renovação automática do token JWT

### 11.2 Requisitos de Infraestrutura

- **Conexão Estável**: Garantir conexão estável com a internet
- **Certificados SSL**: Utilizar certificados SSL válidos para comunicação segura
- **Firewall**: Configurar firewall para permitir comunicação com os servidores do PNCP
- **Monitoramento**: Implementar monitoramento das integrações para detectar falhas rapidamente

## 12. Integração com o Portal de Licitação

Para o portal de licitação que estamos desenvolvendo, a integração com o PNCP deve ser implementada como um módulo específico, responsável por:

1. **Gerenciar Autenticação**: Obter e renovar tokens JWT
2. **Sincronizar Dados**: Enviar automaticamente informações sobre licitações, contratos e documentos para o PNCP
3. **Consultar Informações**: Buscar informações no PNCP quando necessário
4. **Validar Dados**: Garantir que os dados estejam em conformidade com os requisitos do PNCP
5. **Tratar Erros**: Lidar com falhas de comunicação e erros retornados pela API
6. **Registrar Logs**: Manter registros detalhados das operações realizadas

## 13. Conclusão

A integração com o PNCP é um requisito legal e técnico fundamental para o portal de licitação que estamos desenvolvendo. A API REST disponibilizada pelo PNCP oferece todos os recursos necessários para essa integração, permitindo o envio e consulta de informações sobre contratações públicas.

Para garantir uma integração eficiente e confiável, é importante seguir as boas práticas de desenvolvimento, utilizar o ambiente de treinamento para testes e implementar mecanismos robustos de tratamento de erros e segurança.

O desenvolvimento do módulo de integração com o PNCP deve ser considerado uma prioridade no projeto do portal de licitação, garantindo a conformidade com a Lei nº 14.133/2021 e facilitando a publicidade e transparência dos processos de contratação pública.

## 14. Referências

1. Manual de Integração PNCP – Versão 2.2.1
2. Documentação da API do PNCP (Swagger)
3. Lei nº 14.133/2021 - Nova Lei de Licitações e Contratos Administrativos
4. Portal Nacional de Contratações Públicas (PNCP) - https://www.gov.br/pncp/pt-br
