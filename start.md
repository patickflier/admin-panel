## Stap: Structuur van de Monorepository

```
careheld-app/
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── src/
│       ├── settings.py
│       ├── db.py
│       └── main.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── src/
│   │   ├── main.tsx
│   │   └── App.tsx
│   └── vite.config.ts
├── docker-compose.yml
└── .gitignore

```

----------

## Stap: Docker Compose Configuratie

Maak het bestand `docker-compose.yml` in de root-map:

```yaml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    command: ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]
    environment:
      DATABASE_URL: postgresql://postgres:postgres@db:5432/app
    depends_on:
      - db
      - redis
    develop:
      watch:
        - action: sync
          path: ./backend
          target: /app
          ignore:
            - uv.lock
            - .venv
        - action: rebuild
          path: ./backend/uv.lock

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    command: ["pnpm", "run", "dev", "--host"]
    develop:
      watch:
        - action: sync
          path: ./frontend
          target: /app
          ignore:
            - node_modules
            - pnpm-lock.yaml
            - package.json
        - action: rebuild
          path: ./frontend/pnpm-lock.yaml

  db:
    image: postgres:16-alpine
    restart: "unless-stopped"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: app
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  db-data:
```

----------

## Stap: Backend Dockerfile (FastAPI + uv)

Plaats in `backend/Dockerfile`:

```Dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv venv
RUN uv pip install -e .

COPY . .

EXPOSE 8000

```

----------

## Stap: Frontend Dockerfile (Vite + pnpm)

Plaats in `frontend/Dockerfile`:

```Dockerfile
FROM node:24-alpine

WORKDIR /app

RUN npm install -g pnpm

COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .

EXPOSE 3000

```

----------

## Stap: Backend Project Initialiseren

In `backend` map:

```bash
uv init
uv add fastapi uvicorn sqlalchemy alembic pydantic-settings psycopg2-binary
```

----------

## Stap: Backend bestanden (`settings.py`, `db.py`)

### `settings.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost/app"

settings = Settings()

```

### `db.py`

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

class CrmPerson(Base):
    __tablename__ = "crm_person"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100))
```

----------

### `main.py`

```python
# This is for testing purposes to see if it indeed works
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "It works"}

```

----------

## Stap: Alembic migraties

In backend-map, initialiseren met:

```bash
alembic init migrations

```

Aanpassen in `migrations/env.py` om settings te importeren:

```python
from src.settings import settings

config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
```

Maak migratie aan:

```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

```

----------

## Stap: Frontend Opzetten (React, Mantine, ReactRouter)

In `frontend`:

```bash
pnpm create vite . --template react-ts
pnpm install @mantine/core @mantine/hooks @mantine/dates @mantine/form @emotion/react react-router-dom
pnpm install -D biome @types/react-router-dom

```

Verwijder standaard bestanden (`App.css`, etc.) en maak simpele `main.tsx` en `App.tsx`.

### `App.tsx` met Mantine navbar voorbeeld:

Gebruik als basis:  
[https://ui.mantine.dev/component/navbar-nested/](https://ui.mantine.dev/component/navbar-nested/)

----------

## Stap: API Client genereren met `@hey-api/openapi-ts`

In `frontend`:

```bash
pnpm install @hey-api/openapi-ts @tanstack/react-query
pnpm exec openapi-ts -i http://localhost:8000/openapi.json -o src/api

```

Gebruik TanStack Query voor API calls.

----------

## Stap: Controle Tools instellen en uitvoeren

### Backend (`ruff`):

Installeer:

```bash
uv add install ruff

```

Uitvoeren:

```bash
uv run ruff check --ignore T201 --fix .
uv run ruff format .

```

### Frontend (`biome`):

Gebruik de volgende configuratie in `frontend/biome.jsonc`

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": { "enabled": false, "clientKind": "git", "useIgnoreFile": true },
  "files": {
    "ignoreUnknown": false,
    "ignore": [".venv/**", ".vscode/**", "tsconfig.*"]
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "organizeImports": { "enabled": true },
  "linter": {
    "enabled": true,
    "rules": {
      "a11y": {
        // We're not that supportive...
        "noSvgWithoutTitle": "off",
        "useKeyWithClickEvents": "off"
      },
      "correctness": {},
      "suspicious": {
        // Cause, sometimes we need to this
        "noArrayIndexKey": "off"
      },
      "style": {},
      "security": {},
      "nursery": {
        "useSortedClasses": {
          "level": "error",
          "options": {
            "functions": ["clsx"]
          }
        }
      }
    },
    "ignore": []
  },
  "javascript": {
    "formatter": {
      "jsxQuoteStyle": "double",
      "quoteProperties": "asNeeded",
      "trailingCommas": "all",
      "semicolons": "always",
      "arrowParentheses": "always",
      "bracketSameLine": false,
      "quoteStyle": "double",
      "attributePosition": "auto",
      "bracketSpacing": true
    }
  },
  "overrides": [
    {
      "linter": {}
    }
  ]
}
```
### Basis Frontend Setup

Onderstaand een korte uitleg hoe de frontend is ingericht:

---

#### 🗂️ **`main.tsx`**

In dit bestand voeg je de core styles van Mantine toe.

```tsx
import "@mantine/core/styles.css";
```

Importeer hier ook de MantineProvider, zodat de styles correct kunnen worden geladen.
```tsx
import { MantineProvider } from '@mantine/core'
```
Een standaard main.tsx-bestand ziet er als volgt uit:
```tsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom';
import { router } from './routes'
import { MantineProvider } from '@mantine/core'
import "@mantine/core/styles.css";

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <MantineProvider defaultColorScheme="dark">
      <RouterProvider router={router} />
    </MantineProvider>
  </StrictMode>,
)
```

---

#### 🗂️ **`router.tsx`**

In het bestand router.tsx beheren we de routing van onze applicatie. Hier maken we een createBrowserRouter aan en importeren we vervolgens onze componenten.
Het bestand ziet er als volgt uit.

```tsx
import { createBrowserRouter } from 'react-router-dom'
import Homepage from './components/HomePage'
import Overview from './components/dossiers/Overview'
import { Layout } from './components/dossiers/Layout'

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      { index: true, element: <Homepage /> },
      { path: "dossiers", element: <Overview /> },
    ],
  },
])
```

---

#### 🗂️ **`Layout.tsx`**

Op de pagina Layout.tsx beheren we de gebruikersinterface waarmee je door de pagina navigeert.
Hier gebruiken we de Outlet om de andere componenten te renderen.

## Voorbeeld
 
 ```tsx
  import {
  IconBellRinging,
  IconLogout,
  IconReceipt2,
  IconSwitchHorizontal,
} from '@tabler/icons-react';
import { Code, Group } from '@mantine/core';
import classes from '../../assets/styles/Layout.module.css';
import { useState } from 'react';
import { Outlet, useNavigate } from 'react-router-dom';

const data = [
  { link: '/', label: 'Homepage', icon: IconBellRinging },
  { link: '/dossiers', label: 'Dossiers', icon: IconReceipt2 },
];

export function Layout() {
  const [active, setActive] = useState('Homepage');
  const navigate = useNavigate();
  const links = data.map((item) => (
  <a
    className={classes.link}
    data-active={item.label === active || undefined}
    href={item.link}
    key={item.label}
    onClick={(event) => {
      event.preventDefault();
      setActive(item.label);
      navigate(item.link);
    }}
  >
    <item.icon className={classes.linkIcon} stroke={1.5} />
    <span>{item.label}</span>
  </a>
));


  return (
    <div className={classes.container}>
      <nav className={classes.navbar}>
        <div className={classes.navbarMain}>
          <Group className={classes.header} justify="space-between">
            <Code fw={700} className={classes.version}>
              v3.1.2
            </Code>
          </Group>
          {links}
        </div>

        <div className={classes.footer}>
          <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
            <IconSwitchHorizontal className={classes.linkIcon} stroke={1.5} />
            <span>Change account</span>
          </a>

          <a href="#" className={classes.link} onClick={(event) => event.preventDefault()}>
            <IconLogout className={classes.linkIcon} stroke={1.5} />
            <span>Logout</span>
          </a>
        </div>
      </nav>
      <main className={classes.mainContent}>
        <Outlet />
      </main>
    </div>
  );
}
 ```
#### 🗂️ **`Layout.module.css`**
``` css
.navbar {
  height: 100dvh;
  width: 300px;
  padding: var(--mantine-spacing-md);
  display: flex;
  flex-direction: column;
  border-right: 1px solid light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-4));
}

.navbarMain {
  flex: 1;
}

.header {
  padding-bottom: var(--mantine-spacing-md);
  margin-bottom: calc(var(--mantine-spacing-md) * 1.5);
  border-bottom: 1px solid light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-4));
}

.footer {
  padding-top: var(--mantine-spacing-md);
  margin-top: var(--mantine-spacing-md);
  border-top: 1px solid light-dark(var(--mantine-color-gray-3), var(--mantine-color-dark-4));
}

.link {
  display: flex;
  align-items: center;
  text-decoration: none;
  font-size: var(--mantine-font-size-sm);
  color: light-dark(var(--mantine-color-gray-7), var(--mantine-color-dark-1));
  padding: var(--mantine-spacing-xs) var(--mantine-spacing-sm);
  border-radius: var(--mantine-radius-sm);
  font-weight: 500;

  @mixin hover {
    background-color: light-dark(var(--mantine-color-gray-0), var(--mantine-color-dark-6));
    color: light-dark(var(--mantine-color-black), var(--mantine-color-white));

    .linkIcon {
      color: light-dark(var(--mantine-color-black), var(--mantine-color-white));
    }
  }

  &[data-active] {
    &,
    &:hover {
      background-color: var(--mantine-color-blue-light);
      color: var(--mantine-color-blue-light-color);

      .linkIcon {
        color: var(--mantine-color-blue-light-color);
      }
    }
  }
}

.linkIcon {
  color: light-dark(var(--mantine-color-gray-6), var(--mantine-color-dark-2));
  margin-right: var(--mantine-spacing-sm);
  width: 25px;
  height: 25px;
}

.container {
  display: flex;
  min-height: 100vh;
}

.mainContent {
  flex: 1;
  display: flex;
  justify-content: center;
}
```
---


Installeer (al gedaan):

```bash
pnpm exec biome check --fix --unsafe .
pnpm exec biome format --fix .

```

----------

## Stap: Docker controle

Compileer en draai docker:

```bash
docker compose pull
docker compose build

```

----------

## Stap: Commit-message (voorbeeld):

```bash
git add .
git commit -m "
feat: Setup monorepo structure with backend (FastAPI, SQLAlchemy, Alembic) and frontend (React, Mantine, React Router).

- Added docker-compose setup including PostgreSQL and Redis.
- Configured backend Dockerfile with Python 3.12, uv, FastAPI stack.
- Set up frontend Dockerfile with pnpm, Vite, Mantine, React Router.
- Backend includes database setup with declarative models and Alembic migrations.
- Frontend initial setup with Mantine navigation and API integration via hey-api.
- Ruff and Biome configurations enforced for consistent coding standards."

```

s