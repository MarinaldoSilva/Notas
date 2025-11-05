# Avaliação Completa – Notas API (Revisão)

Data: 04/11/2025
Avaliado: Marinaldo Silva
Escopo: avaliação técnica completa do repositório atual, considerando qualidade de código, arquitetura, segurança, documentação, testes e prontidão para evolução.

## 1) Visão geral da solução
- Framework: Django 5 + Django REST Framework
- Autenticação: JWT (djangorestframework-simplejwt) com blacklist e rotação de refresh
- Documentação: drf-spectacular (Swagger/Redoc) configurado
- Apps:
  - `users`: modelo de usuário custom (extends `AbstractUser`), endpoints de perfil (Ponto Fortíssimo)
  - `authentication`: endpoints de registro, login e logout com tokens
  - `notas`: CRUD de notas, envio de e-mail na criação

## 2) Pontos fortes
- **Separação por apps**: organização modular (`users`, `authentication`, `notas`) facilita manutenção e evolução.
- **Autenticação moderna**: uso de SimpleJWT com blacklist e rotação de refresh é uma boa prática.
- **Documentação da API**: drf-spectacular + rotas de Swagger/Redoc prontos.
- **Regras de negócio**: validações no serializer de notas (mínimo de palavras; título ≠ descrição) mostram preocupação com domínio.
- **Integração de e-mail**: notificação ao criar nota, com template HTML dedicado.
- **Correções recentes**: `AUTH_USER_MODEL` configurado; `STATIC_URL`/`MEDIA_*` incluídos; template de e-mail recebeu variáveis coerentes (`titulo_nota`).

## 3) Pontos fracos e riscos
### 3.1 Código e arquitetura
- **Serializer de Notas**:
  - `extra_kwargs` tem typo (erro de digitação) em `ststus` (deveria ser `status`).
  - `validate(self, data)`: quando `descricao` não é enviada, retorna `None` e quebra o fluxo; deve sempre retornar `data`.
  - `update`: se o `titulo` não mudar, retorna a instância sem aplicar outras alterações (ex.: `descricao`, `status`), o que não é um problema, mas não é uma boa prática. Deve sempre chamar `super().update(...)` após eventual ajuste do título para garantir que as alterações sejam aplicadas e que o serializer retorne a instância atualizada.
- **Views de Notas**:
  - `NotasDetailAPIView`: em 404 usa `serializer.errors` que não existe no escopo do `except`.
  - Erros sem HTTP status adequado em alguns retornos (ex.: 404/400 ausentes), e uso incorreto de constante (`status.HTTP_404` ao invés de `HTTP_404_NOT_FOUND`).
  - `NotasCreateAPIView`: trata `Notas.DoesNotExist` em `post`, exceção que não faz sentido no trecho; o caso real é `ValidationError`.
- **Users**:
  - `UserUpdateAPIView.patch(self, request, pk)`: resposta 200 quando deveria ser 403 em caso de proibição.

### 3.2 Configuração e ambiente
- **`.gitignore` ignora `migrations/`** (duplicado): sem versionar migrations, o setup limpo fica inconsistente.
- **Estrutura de diretórios**: pastas físicas `Users/` e `Notas/` (caixa alta) vs apps minúsculos em `INSTALLED_APPS`; funciona no Windows, pode falhar em Linux/CI por case sensitivity.
- **`settings.py`**:
  - `MIDDLEWARE`: `CommonMiddleware` duplicado e `CorsMiddleware` no fim. A ordem recomendada coloca `corsheaders.middleware.CorsMiddleware` no topo (antes de `CommonMiddleware`).
  - `TEMPLATES`: bloco definido duas vezes; deve existir apenas um (com `DIRS: [BASE_DIR / 'templates']`).
  - I18N: `LANGUAGE_CODE='en-us'` e `TIME_ZONE='UTC'` destoam do contexto PT-BR.
  - Segurança: `DEBUG=True`, `CORS_ALLOW_ALL_ORIGINS=True`, `ALLOWED_HOSTS=[]` são aceitáveis no desenvolvimento, mas perigosos para produção.

### 3.3 E-mail
- **Interpolação**: em `form_email`, f-strings com `$` e aspas simples (ex.: `"${titulo_nota}"`) geram textos estranhos no assunto/preview. Acredito que tenha sido usada a sintaxe errada para interpolação em Python (ficou semelhante ao JavaScript).
- **Variáveis não utilizadas**: em `msg_txt_pure` não é utilizada.
- **Envio**: `send_mail` é chamado com `message=None`. O parâmetro `message` deve ser uma string (usar a versão texto puro), mesmo com `html_message` presente.

### 3.4 Documentação e testes
- **Comentários irrelevantes**: em `utils.py`, comentário "#titulo do email" não é relevante, uma vez que o nome da variável é auto-explicativo (subject). O mesmo padrão se repete em outras variáveis do mesmo arquivo.
- **README**: exemplos de endpoints, métodos e paths divergem do código (e.g., paths duplicando `/`, nomes diferentes, métodos trocados). Comandos de migrations usam caixa alta nos nomes de apps.
- **Testes**: arquivos de teste vazios — não há cobertura automatizada dos fluxos críticos (auth, CRUD, validações).

## 4) Aderência à senioridade (Júnior 1)
- **Adequações positivas**
  - Separação por apps e uso de serializers com regras de negócio mostram entendimento dos conceitos básicos do Django/DRF.
  - Configuração do usuário custom e de rotas de documentação evidenciam iniciativa e aprendizado contínuo.
- **Pontos a desenvolver**
  - Consistência de respostas HTTP (status codes, mensagens de erro) e manuseio correto de exceções.
  - Boas práticas de `settings.py` (ordem de middlewares, blocos únicos, chaves válidas de libs, I18N e segurança por ambiente).
  - Reprodutibilidade do ambiente (migrations versionadas) e renomear diretórios para minúsculo (users/, notas/) para compatibilidade cross-OS.
  - Qualidade de entrega: README alinhado ao código, testes mínimos e uso de linters/formatters.

## 5) Dívidas técnicas principais
- Migrations não versionadas e `.gitignore` inadequado.
- Duplicidade em `TEMPLATES` e `CommonMiddleware` + ordem do `CORS`.
- Serializer/Views de Notas com inconsistências funcionais e de status code.
- Users Update/Patch desalinhados com rotas e instânciação do serializer.
- Interpolação e `message` no envio de e-mails.
- README desatualizado e ausência de testes automatizados.

## 6) Recomendações priorizadas para melhorias e evolução
- **P0 – Execução confiável (S–M)**
  - Parar de ignorar `migrations/` no `.gitignore` e versionar migrations dos apps.
  - Renomear pastas de apps para minúsculo (`users/`, `notas/`) e ajustar imports para compatibilidade com Linux/CI.
- **P1 – API e validações (S)**
  - `NotasSerializer`: corrigir `status` em `extra_kwargs`; garantir `return data` em `validate`; ajustar `update` para sempre aplicar alterações e, se título mudou, adicionar sufixo de data antes de `super().update`.
  - Views de `notas`: corrigir 404/400/403 e mensagens; usar constantes corretas do DRF; remover `DoesNotExist` do `post` e tratar `ValidationError`.
  - `users`: retornar 403 quando apropriado.
- **P1 – Settings (S)**
  - Consolidar `TEMPLATES` em um bloco com `DIRS: [BASE_DIR / 'templates']`.
  - Mover `corsheaders.middleware.CorsMiddleware` para o topo e remover duplicação de `CommonMiddleware`.
- **P2 – I18N e ambiente (XS–S)**
  - `LANGUAGE_CODE='pt-br'`, `TIME_ZONE='America/Sao_Paulo'`.
  - Parametrizar `DEBUG`, `ALLOWED_HOSTS` e CORS por variável de ambiente (Boa Prática).
- **P3 – Documentação e qualidade (XS–M)**
  - Atualizar README com endpoints reais e exemplo de uso; incluir link do Swagger (`/api/schema/swagger-ui/`).
  - Adicionar `black` (lint), `isort` (organização de imports), `flake8` (lint) e testes mínimos (auth + CRUD notas + validações).

## 8) Conclusão
O projeto demonstra um bom domínio inicial para um Júnior de nível 1: boas escolhas de stack, modularização e preocupação com regras de negócio e documentação. As pendências são típicas do nível (configurações inconsistentes, respostas HTTP, reprodutibilidade e testes). Com o roteiro acima, a base fica estável e pronta para evoluir com segurança.

## 9) Legenda de Prioridades
- P0: Prioridade 0
- P1: Prioridade 1
- P2: Prioridade 2
- P3: Prioridade 3

## 10) Legenda de Complexidade
- XS: Complexidade Extra-Simples
- S: Complexidade Simples
- M: Complexidade Média
- L: Complexidade Livre
