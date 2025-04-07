from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field
from typing import List, Tuple


class LessonInfo(BaseModel):
    cours_topic: str
    current_chapter: str
    course_prerequisites: List[str]


class LessonContents(BaseModel):
    contents_markdown: str = Field(..., description="contents of the lesson in markdown")


class NextChapterOptions(BaseModel):
    winner: str
    voting: List[Tuple[str, int]]


class Lesson(BaseModel):
    info: LessonInfo
    contents: LessonContents
    options: NextChapterOptions



@CrewBase
class ClassroomCrew():
    """Classroom crew"""

    @agent
    def teacher_content_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['teacher_content_specialist'],
            tools=[],
        )

    @agent
    def student_interaction_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['student_interaction_specialist'],
            tools=[],
        )

    @agent
    def discussion_moderator_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['discussion_moderator_expert'],
            tools=[],
        )


    @task
    def generate_lesson_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_lesson_content_task'],
            tools=[],
        )

    @task
    def simulate_student_qa_task(self) -> Task:
        return Task(
            config=self.tasks_config['simulate_student_qa_task'],
            tools=[],
        )

    @task
    def process_voting_and_filter_task(self) -> Task:
        return Task(
            config=self.tasks_config['process_voting_and_filter_task'],
            tools=[],
        )

    @task
    def log(self) -> Task:
        return Task(
            config=self.tasks_config['log'],
            output_json=Lesson
        )


    @crew
    def crew(self) -> Crew:
        """Creates the Classroom crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
