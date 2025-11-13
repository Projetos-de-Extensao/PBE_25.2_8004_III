# Deploy - Sistema de Monitoria

## 📋 Pré-requisitos

- Conta no [Render](https://render.com)
- Conta no [Vercel](https://vercel.com) (opcional, como alternativa)
- Repositório Git configurado

## 🚀 Deploy no Render (Recomendado para Django)

### 1. Preparação

O projeto já está configurado com os arquivos necessários:
- `render.yaml` - Configuração de serviços
- `render-build.sh` - Script de build
- `runtime.txt` - Versão do Python

### 2. Criar Web Service no Render

1. Acesse [Render Dashboard](https://dashboard.render.com)
2. Clique em **"New +"** → **"Web Service"**
3. Conecte seu repositório GitHub
4. Configure:
   - **Name**: `monitoria-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `cd src && gunicorn myproject.wsgi:application`
   - **Instance Type**: Free (ou pago para melhor performance)

### 3. Configurar Banco de Dados PostgreSQL

1. No Render Dashboard, clique em **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `monitoria-db`
   - **Database**: `monitoria`
   - **User**: `monitoria_user`
   - **Region**: Mesma do Web Service

3. Após criar, copie a **Internal Database URL**

### 4. Variáveis de Ambiente no Render

No seu Web Service, vá em **Environment** e adicione:

```
DATABASE_URL=<Internal Database URL copiada>
SECRET_KEY=<gere uma chave aleatória segura>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
PYTHON_VERSION=3.9.18
```

Para gerar SECRET_KEY segura:
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

### 5. Deploy

1. Clique em **"Manual Deploy"** → **"Deploy latest commit"**
2. Aguarde o build completar (~2-5 minutos)
3. Acesse a URL fornecida (ex: `https://monitoria-backend.onrender.com`)

---

## 🌐 Deploy no Vercel (Alternativa)

### 1. Instalar Vercel CLI

```bash
npm i -g vercel
```

### 2. Deploy

```bash
# Na raiz do projeto
vercel

# Para produção
vercel --prod
```

### 3. Configurar Variáveis de Ambiente

No [Vercel Dashboard](https://vercel.com/dashboard):

1. Vá em **Settings** → **Environment Variables**
2. Adicione:
   - `SECRET_KEY`: Chave secreta Django
   - `DEBUG`: `False`
   - `DATABASE_URL`: URL do banco PostgreSQL
   - `ALLOWED_HOSTS`: `.vercel.app`

### 4. Banco de Dados para Vercel

Opções:
- **Supabase** (PostgreSQL gratuito): https://supabase.com
- **Neon** (PostgreSQL serverless): https://neon.tech
- **PlanetScale** (MySQL serverless): https://planetscale.com

---

## 🗄️ Configuração do Banco de Dados

### Opção 1: Render PostgreSQL (Recomendado)
- Já configurado no `render.yaml`
- Backup automático (planos pagos)
- Mesma infraestrutura do backend

### Opção 2: Supabase (Para Vercel)
1. Crie projeto em https://supabase.com
2. Copie a connection string PostgreSQL
3. Adicione como `DATABASE_URL` nas variáveis de ambiente

### Opção 3: Neon (Serverless)
1. Crie projeto em https://neon.tech
2. Copie a connection string
3. Adicione como `DATABASE_URL`

---

## 🔧 Comandos Úteis

### Aplicar Migrações Manualmente (Render)
```bash
# No terminal do Render Web Service
cd src
python manage.py migrate
```

### Criar Superusuário
```bash
cd src
python manage.py createsuperuser
```

### Coletar Arquivos Estáticos
```bash
cd src
python manage.py collectstatic --no-input
```

### Ver Logs (Render)
- Acesse o Web Service → **Logs** tab

---

## 📊 Monitoramento

### Render
- Dashboard mostra CPU, memória e requisições
- Logs em tempo real
- Alertas configuráveis (planos pagos)

### Vercel
- Analytics integrado
- Logs de função
- Métricas de performance

---

## 🔒 Segurança em Produção

✅ Já configurado:
- `DEBUG=False` desabilita modo debug
- `SECURE_SSL_REDIRECT` força HTTPS
- `SESSION_COOKIE_SECURE` cookies seguros
- `CSRF_COOKIE_SECURE` proteção CSRF
- WhiteNoise para servir arquivos estáticos

⚠️ Importante:
- Use SECRET_KEY única e segura
- Configure ALLOWED_HOSTS corretamente
- Mantenha DATABASE_URL secreto
- Ative backup do banco (produção)

---

## 🚨 Troubleshooting

### Erro de Static Files
```bash
cd src
python manage.py collectstatic --no-input --clear
```

### Erro de Database
- Verifique DATABASE_URL está correto
- Execute migrations: `python manage.py migrate`
- Verifique conexão do banco no dashboard

### Erro 502/503
- Render: Verifique logs do serviço
- Aguarde cold start (serviços free dormem após inatividade)

### Build Falha
- Verifique `requirements.txt`
- Confirme `runtime.txt` tem versão Python válida
- Veja logs de build para erro específico

---

## 📝 Checklist de Deploy

- [ ] Repositório no GitHub atualizado
- [ ] `requirements.txt` completo
- [ ] Variáveis de ambiente configuradas
- [ ] Banco de dados PostgreSQL criado
- [ ] Migrações aplicadas
- [ ] Arquivos estáticos coletados
- [ ] Superusuário criado
- [ ] Teste de login funcionando
- [ ] URLs e rotas funcionando

---

## 🔗 Links Úteis

- [Render Docs](https://render.com/docs)
- [Vercel Docs](https://vercel.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/)
- [Gunicorn Docs](https://docs.gunicorn.org/)
