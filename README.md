# 📰 News AI — Intelligent News Assistant

> AI ajanlı haber platformu. Konuşma arayüzü, gerçek zamanlı fact check, haber feed'i ve trend takibi.

---

## Proje Yapısı

```
news-ai/
├── backend/           # FastAPI — Python 3.12
├── frontend/          # Next.js 15 — App Router
├── docs/
│   ├── ROADMAP_BACKEND.md
│   ├── ROADMAP_FRONTEND.md
│   └── DATABASE.md
├── schema.sql         # PostgreSQL schema (Docker'da otomatik yüklenir)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Hızlı Başlangıç

```bash
# 1. Env dosyasını oluştur
cp .env.example .env
# .env dosyasını aç, API key'leri doldur

# 2. Başlat (frontend henüz hazır değil, sadece backend)
docker compose up -d

# 3. Alembic versiyonunu işaretle (ilk kurulumda veya down -v sonrasında)
docker compose exec api python -m alembic stamp head

# 4. Kontrol et
docker compose ps                          # db ve api → healthy olmalı
# PowerShell: Invoke-RestMethod http://localhost:8001/health
# Linux/Mac:  curl http://localhost:8001/health
```

### Sıfırdan Yeniden Başlatma

```bash
docker compose down -v                     # container + volume sil
docker compose up -d                       # yeniden başlat
docker compose exec api python -m alembic stamp head  # versiyonu işaretle
```

---

## Servisler

| Servis | Port | Açıklama |
|--------|------|----------|
| PostgreSQL | 5433 | Ana veritabanı |
| FastAPI | 8001 | Backend API |
| Next.js | 3000 | Frontend |

---

## Environment Variables

`.env.example` dosyasını kopyalayıp doldur:

| Değişken | Açıklama |
|---|---|
| `GROQ_API_KEY` | LLM inference — [console.groq.com](https://console.groq.com) |
| `TAVILY_API_KEY` | Agent web araması — [tavily.com](https://tavily.com) |
| `NEWS_API_KEY` | Haber verisi — [newsapi.org](https://newsapi.org) |
| `JWT_SECRET` | Auth token imzalama — `openssl rand -hex 32` |

---

## Stack

| Katman | Teknoloji |
|---|---|
| Backend | FastAPI + SQLAlchemy + Alembic |
| Database | PostgreSQL 16 |
| AI Agent | Groq API (compound / compound-mini) |
| Web Search | Tavily API |
| News Data | NewsAPI.org + Google News RSS |
| Frontend | Next.js 15 + Tailwind CSS |
| State | Zustand + TanStack Query |

---

## Dokümantasyon

- [Backend Roadmap](docs/ROADMAP_BACKEND.md)
- [Frontend Roadmap](docs/ROADMAP_FRONTEND.md)
- [Database Dokümantasyonu](docs/DATABASE.md)
