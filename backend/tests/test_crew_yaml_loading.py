from app.crew.config.agents_loader import load_agent_configs
from app.crew.config.crews_loader import load_crew_configs
from app.crew.config.tasks_loader import build_tasks, load_task_configs


def test_agents_yaml_loads_with_expected_keys():
	config = load_agent_configs()
	assert "news_fetcher" in config.agents
	assert "verdict_agent" in config.agents


def test_tasks_yaml_loads_with_expected_keys():
	config = load_task_configs()
	assert "fetch_news" in config.tasks
	assert "verdict" in config.tasks


def test_crews_yaml_loads_with_expected_keys():
	config = load_crew_configs()
	assert "news" in config.crews
	assert "fact_check" in config.crews


def test_build_tasks_applies_runtime_templates():
	agents = {
		"news_fetcher": object(),
		"news_analyst": object(),
		"fact_checker": object(),
		"verdict_agent": object(),
	}

	class _TaskStub:
		def __init__(self, **kwargs):
			self.description = kwargs["description"]
			self.expected_output = kwargs["expected_output"]
			self.agent = kwargs["agent"]
			self.context = []

	import app.crew.config.tasks_loader as tasks_loader

	original_task = tasks_loader.Task
	try:
		tasks_loader.Task = _TaskStub
		tasks = build_tasks(
			agents=agents,
			user_message="Tech news?",
			conversation_history=[{"role": "user", "content": "old question"}],
			claim="The earth is flat",
		)
	finally:
		tasks_loader.Task = original_task

	assert "Tech news?" in tasks["fetch_news"].description
	assert "old question" in tasks["fetch_news"].description
	assert "The earth is flat" in tasks["research_claim"].description
	assert tasks["fetch_news"] in tasks["analyze_news"].context
