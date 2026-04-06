# CrewAI Implementation Report

## 1) Project Summary
This report documents the CrewAI implementation in the NewsAI backend.

The system uses a YAML-driven CrewAI architecture with two independent pipelines:
- News pipeline: fetch + analyze
- Fact-check pipeline: research + verdict

The implementation is modular and built around a central factory that creates agents, tasks, and crews from configuration files.

---

## 2) High-Level Architecture
The core flow is:
1. Load agent definitions from YAML.
2. Load task definitions from YAML and apply runtime placeholders.
3. Load crew definitions from YAML.
4. Build CrewAI objects in code via `CrewFactory`.
5. Kick off crews from service layer with retry/fallback logic.

Main implementation files:
- `backend/app/crew/crew_factory.py`
- `backend/app/crew/config/agents.yaml`
- `backend/app/crew/config/tasks.yaml`
- `backend/app/crew/config/crews.yaml`
- `backend/app/services/crew_service.py`
- `backend/app/services/fact_check_service.py`

---

## 3) Agents (Configuration Snippet)
Source: `backend/app/crew/config/agents.yaml`

```yaml
agents:
  news_fetcher:
    role: "News Fetcher"
    goal: "Kullanicinin sorusuyla ilgili guncel ve guvenilir haberleri bul."
    tools:
      - web_search
      - fetch_news_by_category
      - fetch_trending
    llm_profile: default
    max_iter: 5

  news_analyst:
    role: "News Analyst"
    goal: "Getirilen haberleri analiz et ve kullaniciya {language} dilinde, {ai_tone} tonunda, kaynakli bir yanit uret."
    tools:
      - summarize_article
    llm_profile: default

  fact_checker:
    role: "Fact Checker"
    goal: "Iddiayi birden fazla bagimsiz kaynakta arastir."
    tools:
      - fact_check_search
      - web_search
    llm_profile: default
    max_iter: 3

  verdict_agent:
    role: "Verdict Agent"
    goal: "Arastirma bulgularini degerlendirip yapilandirilmis karar ver."
    tools: []
    llm_profile: reasoning
```

### Agent Design Notes
- `news_fetcher` is tool-heavy and iterative for retrieval quality.
- `news_analyst` focuses on synthesis and final response quality.
- `fact_checker` collects evidence from multiple sources.
- `verdict_agent` is isolated from tools and tuned for reasoning output.

---

## 4) Tasks (Configuration Snippet)
Source: `backend/app/crew/config/tasks.yaml`

```yaml
tasks:
  fetch_news:
    description: |
      Konusma gecmisi:
      {conversation_history_text}

      Kullanicinin son sorusu: {user_message}
    expected_output: "Haberlerin listesi: baslik, URL, kisa ozet icermeli."
    agent_ref: news_fetcher

  analyze_news:
    description: |
      Onceki adimda bulunan haberleri analiz et.
      Kullanicinin sorusunu yanitlayan, kaynakli, net bir cevap olustur.
    expected_output: "Kullaniciya yonelik, kaynakli, markdown formatinda yanit."
    agent_ref: news_analyst
    context:
      - fetch_news

  research_claim:
    description: |
      Su iddiayi arastir: '{claim}'
    expected_output: "Kaynaklar listesi: baslik, URL, iddiayi destekleme/curutme durumu."
    agent_ref: fact_checker

  verdict:
    description: |
      Arastirma bulgularini degerlendirip su JSON formatinda yanit ver:
      {{"verdict": "TRUE|FALSE|UNVERIFIED", "explanation": "2-3 cumle", "confidence_score": 0.0-1.0, "sources": [{{"title": "...", "url": "...", "snippet": "..."}}]}}
    expected_output: "Gecerli JSON, baska hicbir sey yok."
    agent_ref: verdict_agent
    context:
      - research_claim
```

### Task Design Notes
- News tasks are chained (`fetch_news` -> `analyze_news`) to separate retrieval and synthesis responsibilities.
- Fact-check tasks enforce structured verdict JSON for deterministic downstream handling.

---

## 5) Crew Definition (CFG Snippet)
Source: `backend/app/crew/config/crews.yaml`

```yaml
crews:
  news:
    agents:
      - news_fetcher
      - news_analyst
    tasks:
      - fetch_news
      - analyze_news
    process: sequential

  fact_check:
    agents:
      - fact_checker
      - verdict_agent
    tasks:
      - research_claim
      - verdict
    process: sequential
```

### Crew Design Notes
- Sequential processing is used to preserve context and pipeline order.
- Separate crews reduce coupling between chat-news generation and fact-check logic.

---

## 6) Kickoff Code Snippets

### 6.1 Factory-Based Crew Construction
Source: `backend/app/crew/crew_factory.py`

```python
class CrewFactory:
    @staticmethod
    def create_news_crew(*, user_message, conversation_history, language, ai_tone, step_callback=None):
        agents = build_agents(language=language, ai_tone=ai_tone)
        tasks = build_tasks(
            agents=agents,
            user_message=user_message,
            conversation_history=conversation_history,
        )
        crews = build_crews(agents=agents, tasks=tasks, step_callback=step_callback)
        return crews["news"]

    @staticmethod
    def create_fact_check_crew(*, claim, default_model=None, reasoning_model=None):
        agents = build_agents(
            language="Turkish",
            ai_tone="neutral",
            default_model=default_model,
            reasoning_model=reasoning_model,
        )
        tasks = build_tasks(agents=agents, claim=claim)
        crews = build_crews(agents=agents, tasks=tasks)
        return crews["fact_check"]
```

### 6.2 News Crew Kickoff in Service Layer
Source: `backend/app/services/crew_service.py`

```python
crew = CrewFactory.create_news_crew(
    user_message=user_message,
    conversation_history=conversation_history,
    language=language,
    ai_tone=ai_tone,
    step_callback=step_callback,
)
result = await crew.kickoff_async()
return result.raw
```

### 6.3 Fact-Check Crew Kickoff in Service Layer
Source: `backend/app/services/fact_check_service.py`

```python
crew = CrewFactory.create_fact_check_crew(claim=claim)
result = await crew.kickoff_async()
return _normalize_fact_check_output(result.raw)
```

### Kickoff Reliability Notes
- Retry logic is applied for rate limit scenarios.
- Fact-check flow includes fallback path for model/API constraints.
- Output normalization ensures robust handling when `result.raw` is returned as string vs dict.

---

## 7) Configuration (CFG) Files Included
This implementation uses the following configuration files:

- `backend/app/crew/config/agents.yaml` (agent definitions)
- `backend/app/crew/config/tasks.yaml` (task templates and context chaining)
- `backend/app/crew/config/crews.yaml` (crew composition and process mode)
- `backend/app/crew/config/crew_schema.py` (Pydantic schema validation for config files)
- `backend/app/crew/config/agents_loader.py` (load/instantiate agents)
- `backend/app/crew/config/tasks_loader.py` (load/instantiate tasks + runtime template formatting)
- `backend/app/crew/config/crews_loader.py` (load/instantiate crews)

---

## 8) Conclusion
The CrewAI implementation is production-oriented in structure:
- Config-driven (YAML + schema validation)
- Layered (factory + loaders + services)
- Reliable (retry/fallback/output normalization)
- Extensible (new agents/tasks/crews can be added with cfg updates)

This report includes the requested agent snippets, task snippets, kickoff snippets, and cfg files.
