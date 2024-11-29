from ninja import Schema
from datetime import date
from typing import List

class QuestionSchema(Schema):
    assignment_id: int
    text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    selected_answer: str
    correct_answer: str


class AssignmentSchema(Schema):
    id: int
    title: str
    course_id: int
    due_date: date
    questions: List[QuestionSchema]
