# 🗄️ Configuração de Banco de Dados

Este projeto está configurado para usar **SQLite em desenvolvimento** e **PostgreSQL em produção** automaticamente.

## 🏠 Desenvolvimento Local (SQLite)

Não precisa fazer nada! O projeto usa SQLite por padrão quando você roda localmente.

```bash
# Ativar ambiente virtual
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Rodar migrações
cd src
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

O banco SQLite será criado automaticamente em `src/db.sqlite3`.

---

## ☁️ Produção (PostgreSQL no Vercel)

### 1️⃣ Criar banco PostgreSQL grátis

Escolha uma das opções:

#### Opção A: Supabase (Recomendado)
1. Acesse [supabase.com](https://supabase.com)
2. Crie uma conta gratuita
3. Crie um novo projeto
4. Vá em **Settings → Database**
5. Copie a **Connection String** (formato URI)

#### Opção B: Neon
1. Acesse [neon.tech](https://neon.tech)
2. Crie uma conta gratuita
3. Crie um novo projeto
4. Copie a **Connection String**

#### Opção C: Railway
1. Acesse [railway.app](https://railway.app)
2. Crie um banco PostgreSQL
3. Copie a **DATABASE_URL**

---

### 2️⃣ Configurar no Vercel

1. Vá em **Settings → Environment Variables**
2. Adicione estas variáveis:

| Nome | Valor | Exemplo |
|------|-------|---------|
| `DATABASE_URL` | Sua connection string do PostgreSQL | `postgresql://user:pass@host:5432/db` |
| `DEBUG` | `False` | - |
| `PYTHONPATH` | `src` | - |

3. Faça um novo deploy

---

### 3️⃣ Rodar migrações no banco de produção

Após o deploy, você precisa rodar as migrações uma vez:

**Via Vercel CLI:**
```bash
vercel env pull .env.production
cd src
python manage.py migrate --settings=myproject.settings
```

**Ou adicione no `build.sh`** (já configurado):
```bash
python manage.py migrate --noinput
```

---

## 🔍 Como funciona?

O código em `settings.py` detecta automaticamente:

```python
if os.environ.get('DATABASE_URL'):
    # Está em produção → Usa PostgreSQL
    DATABASES = dj_database_url.config(...)
else:
    # Está em desenvolvimento → Usa SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

---

## ✅ Dependências Instaladas

As seguintes bibliotecas foram adicionadas ao `requirements.txt`:

- `dj-database-url==2.1.0` - Parse da URL do banco
- `psycopg2-binary==2.9.9` - Driver PostgreSQL

---

## 🚨 Importante

- ❌ **Nunca commite** o arquivo `.env` com credenciais
- ✅ Use `.env.example` como template
- ✅ Configure `DATABASE_URL` apenas no Vercel
- ✅ SQLite funciona apenas localmente (não funciona no Vercel)

---

## 🧪 Testar localmente com PostgreSQL (opcional)

Se quiser testar com PostgreSQL localmente:

1. Instale PostgreSQL localmente
2. Crie um banco de dados
3. Crie um arquivo `.env` na raiz do projeto:

```bash
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

4. Instale python-dotenv:
```bash
pip install python-dotenv
```

5. Adicione no `settings.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📚 Mais Informações

- [Django Database Settings](https://docs.djangoproject.com/en/4.2/ref/settings/#databases)
- [Vercel PostgreSQL](https://vercel.com/docs/storage/vercel-postgres)
- [dj-database-url](https://github.com/jazzband/dj-database-url)
