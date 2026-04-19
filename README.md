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

### Frontend Kurulum Adımları

```bash
# 1. Frontend bağımlılıklarını kur
cd frontend
npm install

# 2. Frontend geliştirme sunucusunu başlat
npm run dev

# 3. Tarayıcıdan kontrol et
# http://localhost:3000
```

Frontend geliştirme sırasında backend için `http://localhost:8001` kullanılır.

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
| AI Agent | CrewAI + LangGraph + Groq API |
| Web Search | Tavily API |
| News Data | NewsAPI.org + Google News RSS |
| Frontend | Next.js 15 + Tailwind CSS |
| State | Zustand + TanStack Query |

---

## LangGraph + CrewAI Implementation (Well-Defined Steps)

Bu proje, CrewAI altyapisini koruyarak LangGraph'i ayni backend'e entegre eder. Ilk pilot akisi fact-check uzerinden ilerler.

### 1) Dependencies ve Ortam Hazirligi

- [x] Backend bagimliliklarina `langgraph`, `langchain-core`, `langsmith` eklendi.
- [x] Orchestrator ve tracing ayarlari `.env` seviyesinde tanimlandi.
- [x] Backend gelistirme akisi icin `.venv` kullanimi netlestirildi.

Local backend komutu:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

### 2) LangGraph Fact-Check Pilotu

- [x] LangGraph state graph tabanli fact-check akisi eklendi.
- [x] Node bazli kaynak toplama + karar (verdict) uretilmesi uygulandi.
- [x] Sonsuz dongu riskine karsi `recursion_limit` zorunlu hale getirildi.

### 3) Orchestrator Selection Kurali (Kesin)

- [x] Global override: `ENABLE_LANGGRAPH=False` ise her zaman CrewAI calisir.
- [x] `ENABLE_LANGGRAPH=True` ise kullanici tercihi (`crewai` / `langgraph`) uygulanir.
- [x] Tercih yoksa varsayilan yine CrewAI olur.

### 4) Consistency ve Output Guardrails

- [x] LangGraph ciktisi strict validation'dan gecirilir.
- [x] Verdict payload'i zorunlu alanlar ve deger araliklari ile dogrulanir.
- [x] API donusu `FactCheckResponse` ile uyumlu kalacak sekilde korunur.

### 5) User Preferences + Frontend Toggle

- [x] `user_preferences` tablosuna `orchestrator` alani eklendi.
- [x] Preferences API, orchestrator alanini okuyup guncelleyecek sekilde genisletildi.
- [x] Settings ekraninda orchestrator secimi eklendi (settings-only, form bazli override yok).

### 6) LangSmith Tracing

- [x] LangSmith ayarlari tanimlandi ve opsiyonel tracing desteklendi.
- [x] Tracing sadece konfigurasyonda aktifse devreye girer.

Ornek env alanlari:

```env
ENABLE_LANGGRAPH=False
LANGGRAPH_RECURSION_LIMIT=25
LANGSMITH_TRACING=False
LANGSMITH_API_KEY=
LANGSMITH_PROJECT=newsai-langgraph
```

### 7) Test ve Verification Checklist

- [x] Backend orchestrator secim path testleri yazildi.
- [x] Edge-case testleri eklendi (invalid payload, eksik payload, env override, markdown JSON parse).
- [x] Frontend settings testleri orchestrator toggle ve payload mapping icin guncellendi.
- [x] Docker icinde hedef test setleri basariyla calistirildi.

Ornek backend test komutu (Docker):

```bash
docker exec -e TEST_DATABASE_URL="postgresql+asyncpg://newsai:newsai@db:5432/newsai_test" -e DATABASE_URL="postgresql+asyncpg://newsai:newsai@db:5432/newsai" newsai-api-1 python -m pytest tests/test_fact_check.py tests/test_auth.py --no-cov
```

### 8) Teslim Checklist

- [ ] Son degisiklikleri gozden gecir ve commit mesajlarini netlestir.
- [ ] Git repository/account linkini paylas.
- [ ] Sinifta anlatim icin kisa mimari ozet hazirla:
	- CrewAI ve LangGraph'in birlikte calisma modeli
	- Orchestrator secim kurali
	- Recursion limit ve validation guvenlik katmanlari
	- Test kapsamindan kritik senaryolar

---

## Dokümantasyon

- [Backend Roadmap](docs/ROADMAP_BACKEND.md)
- [Frontend Roadmap](docs/ROADMAP_FRONTEND.md)
- [Database Dokümantasyonu](docs/DATABASE.md)
