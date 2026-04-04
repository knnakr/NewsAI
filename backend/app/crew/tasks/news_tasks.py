from __future__ import annotations

from crewai import Task


def create_fetch_task(agent, user_message: str, conversation_history: list[dict]) -> Task:
	history_text = "\n".join([f"{m['role']}: {m['content']}" for m in conversation_history[-10:]])
	return Task(
		description=(
			f"Konuşma geçmişi:\n{history_text}\n\n"
			f"Kullanıcının son sorusu: {user_message}\n\n"
			"Bu soru için güncel haberleri ve bilgileri web'de ara. "
			"Kaynak URL'lerini mutlaka dahil et."
		),
		expected_output="Haberlerin listesi: başlık, URL, kısa özet içermeli.",
		agent=agent,
	)


def create_analysis_task(agent, fetch_task: Task) -> Task:
	return Task(
		description=(
			"Önceki adımda bulunan haberleri analiz et. "
			"Kullanıcının sorusunu yanıtlayan, kaynaklı, net bir cevap oluştur. "
			"Her önemli iddia için kaynak URL belirt."
		),
		expected_output=(
			"Kullanıcıya yönelik, kaynaklı, markdown formatında yanıt. "
			"Sonunda kaynaklar listesi bulunmalı."
		),
		agent=agent,
		context=[fetch_task],
	)
