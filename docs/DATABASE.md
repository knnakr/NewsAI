# News AI — Database Documentation

PostgreSQL 16+ · 11 tablo · `schema.sql` proje kökünde

---

## Tablolar

| Tablo | Açıklama |
|---|---|
| `users` | Platform kullanıcıları. Email/password ve OAuth desteği. |
| `refresh_tokens` | JWT refresh token'ları. 30 günlük ömür. |
| `password_reset_tokens` | Şifre sıfırlama linkleri. 15 dakika geçerli. |
| `email_verification_tokens` | E-posta doğrulama linkleri. 24 saat geçerli. |
| `user_preferences` | Kullanıcı başına CrewAI agent davranış ve UI tercihleri. |
| `conversations` | Chat session'ları. Soft delete destekli. |
| `messages` | Konuşma mesajları. Tavily kaynakları JSONB olarak saklanır. |
| `agent_tool_calls` | CrewAI agent'larının her mesajda kullandığı tool çağrıları. |
| `fact_checks` | Fact Check Crew geçmişi. Giriş yapmadan da kullanılabilir. |
| `saved_articles` | Kullanıcının kaydettiği haberler. |
| `article_cache` | NewsAPI 100 req/gün limitini yönetmek için 6 saatlik önbellek. |

---

## ENUM Types

| Type | Değerler |
|---|---|
| `news_category` | world, technology, sports, economy, health, science, entertainment |
| `message_role` | user, assistant, system |
| `fact_verdict` | TRUE, FALSE, UNVERIFIED |
| `user_role` | user, admin |
| `auth_provider` | email, google, github |
| `ai_tone` | neutral, formal, casual |
| `agent_tool` | web_search, fetch_news_by_category, fetch_trending, fact_check_search, summarize_article |

> **Not:** `agent_tool` ENUM'undaki değerler, CrewAI `BaseTool` sınıflarının `name` alanlarıyla birebir eşleşmelidir. Yeni bir CrewAI tool eklendiğinde:
> 1. `BaseTool` sınıfında `name = "tool_name"` tanımla
> 2. Bu ENUM'a yeni değeri ekle (`schema.sql` + Alembic migration)
> 3. `app/crew/hooks.py` içindeki `known_tools` kümesini güncelle
> 4. `DATABASE.md`'deki agent-tool eşleşme tablosunu güncelle

---

## İlişkiler

```
users ──────────── user_preferences     (1-to-1, trigger ile otomatik oluşur)
users ──────────── conversations        (1-to-many)
users ──────────── fact_checks          (1-to-many, user_id nullable)
users ──────────── saved_articles       (1-to-many)
users ──────────── refresh_tokens       (1-to-many)
conversations ──── messages             (1-to-many, cascade delete)
messages ────────── agent_tool_calls    (1-to-many, cascade delete)
```

---

## `agent_tool_calls` — CrewAI Bağlamı

Bu tablo, CrewAI agent'larının her mesaj için yaptığı tool çağrılarını kaydeder.

| Sütun | Açıklama |
|---|---|
| `message_id` | Hangi asistan mesajına ait olduğu |
| `tool_name` | Çağrılan CrewAI tool'unun adı (`agent_tool` ENUM) |
| `input_params` | Tool'a gönderilen parametreler (JSONB) |
| `output_result` | Tool'dan dönen sonuç (TEXT) |
| `duration_ms` | Tool çalışma süresi (ms) |
| `is_success` | Başarılı mı? |
| `error_message` | Hata varsa mesajı |

**Hangi agent hangi tool'u kullanır:**

| Agent (CrewAI) | Kullandığı Tool'lar |
|---|---|
| `NewsFetcherAgent` | `web_search`, `fetch_news_by_category`, `fetch_trending` |
| `NewsAnalystAgent` | `summarize_article` |
| `FactCheckerAgent` | `fact_check_search`, `web_search` |
| `VerdictAgent` | *(tool yok — sadece context değerlendirir)* |

---

## `user_preferences` — CrewAI Agent Davranışı

`user_preferences` tablosundaki alanlar doğrudan CrewAI agent'larının davranışını etkiler:

| Sütun | Etkisi |
|---|---|
| `language` | `NewsAnalystAgent`'ın `goal` alanına eklenir → yanıt dili |
| `ai_tone` | `NewsAnalystAgent`'ın `goal` alanına eklenir → yanıt tonu |
| `news_categories` | `NewsFetcherAgent`'ın hangi kategorileri önceliklendireceğini belirler |

---

## Trigger'lar

| Trigger | Ne Yapar |
|---|---|
| `trg_create_user_preferences` | Yeni kullanıcı kaydolduğunda `user_preferences` satırı otomatik oluşturur |
| `trg_conversations_updated_at` | Conversation güncellendiğinde `updated_at` otomatik set edilir |
| `trg_message_updates_conversation` | Yeni mesaj eklendiğinde conversation'ın `updated_at`'i güncellenir |
| `trg_user_preferences_updated_at` | Tercihler güncellendiğinde `updated_at` otomatik set edilir |

---

## Kritik Constraint'ler

```sql
-- Kullanıcı aynı makaleyi iki kez kaydedemez
UNIQUE(user_id, article_url)

-- Cache key benzersiz olmalı
UNIQUE(cache_key)

-- Email/password veya OAuth
CHECK (auth_provider = 'email' AND hashed_password IS NOT NULL) OR auth_provider != 'email'

-- Güven skoru 0-1 arası (VerdictAgent çıktısı doğrulanır)
CHECK (confidence_score BETWEEN 0.0 AND 1.0)
```

---

## Cache Temizliği

`cleanup_expired_cache()` fonksiyonu APScheduler ile her 6 saatte çalıştırılır:
- Süresi dolmuş `article_cache` kayıtlarını siler
- Revoke edilmiş ve süresi dolmuş `refresh_tokens`'ı siler
- Kullanılmış ve süresi dolmuş `password_reset_tokens`'ı siler
- Kullanılmış ve süresi dolmuş `email_verification_tokens`'ı siler

---

## Test Veritabanı

Testlerde ayrı bir `newsai_test` veritabanı kullanılır. `conftest.py` her test fonksiyonu için tabloları oluşturur ve test sonrası temizler:

```python
# tests/conftest.py
TEST_DATABASE_URL = "postgresql+asyncpg://newsai:newsai@localhost:5433/newsai_test"
```

Test DB'si Docker'daki PostgreSQL üzerinde oluşturulur — ayrı container gerekmez:
```bash
docker compose exec db psql -U newsai -c "CREATE DATABASE newsai_test;"
```

---

## Bağlantı

```bash
# Docker ile local bağlantı
psql -h localhost -p 5433 -U newsai -d newsai

# Container içinden
docker compose exec db psql -U newsai -d newsai

# Test DB
psql -h localhost -p 5433 -U newsai -d newsai_test
```
