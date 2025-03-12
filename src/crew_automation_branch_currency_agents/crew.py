from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import CSVSearchTool
from crewai_tools import FileReadTool

@CrewBase
class CrewAutomationBranchCurrencyAgentsCrew():
    """CrewAutomationBranchCurrencyAgents crew"""

    @agent
    def branch_name_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['branch_name_agent'],
            tools=[CSVSearchTool(), FileReadTool()],
        )

    @agent
    def currency_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['currency_agent'],
            tools=[CSVSearchTool(), FileReadTool()],
        )


    @task
    def branch_mapping_task(self) -> Task:
        return Task(
            config=self.tasks_config['branch_mapping_task'],
            tools=[CSVSearchTool(), FileReadTool()],
        )

    @task
    def currency_filtering_task(self) -> Task:
        return Task(
            config=self.tasks_config['currency_filtering_task'],
            tools=[CSVSearchTool(), FileReadTool()],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the CrewAutomationBranchCurrencyAgents crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
