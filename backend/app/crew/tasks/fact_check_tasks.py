from __future__ import annotations

from crewai import Task


def create_research_task(agent, claim: str) -> Task:
	return Task(
		description=(
			f"Su iddiayi arastir: '{claim}'\n\n"
			"- En az 3 farkli kaynakta ara\n"
			"- Bagimsiz kaynaklari onceliklendir\n"
			"- Her kaynagin URL'ini kaydet"
		),
		expected_output="Kaynaklar listesi: baslik, URL, iddiayi destekleme/curutme durumu.",
		agent=agent,
	)


def create_verdict_task(agent, research_task: Task) -> Task:
	return Task(
		description=(
			"Arastirma bulgularini degerlendirip su JSON formatinda yanit ver:\n"
			'{"verdict": "TRUE|FALSE|UNVERIFIED", '
			'"explanation": "2-3 cumle", '
			'"confidence_score": 0.0-1.0, '
			'"sources": [{"title": "...", "url": "...", "snippet": "..."}]}'
		),
		expected_output="Gecerli JSON, baska hicbir sey yok.",
		agent=agent,
		context=[research_task],
	)
