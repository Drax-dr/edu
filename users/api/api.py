# from ninja import NinjaAPI
# from core.models import UserProfile, Course, Assignment, Question, Enrollment
# from django.contrib.auth.models import User
# from core.schemas import UserSchema, CourseSchema, AssignmentSchema, QuestionSchema

# api = NinjaAPI()

# @api.get("/courses/", response=list[CourseSchema])
# def list_courses(request):
#     return Course.objects.all()

# @api.post("/assignments/", response=AssignmentSchema)
# def create_assignment(request, data: AssignmentSchema):
#     course = Course.objects.get(id=data.course_id)
#     assignment = Assignment.objects.create(
#         title=data.title, course=course, due_date=data.due_date
#     )
#     return assignment

# @api.get("/assignments/{course_id}", response=list[AssignmentSchema])
# def list_assignments(request, course_id: int):
#     assignments = Assignment.objects.filter(course_id=course_id)
#     return assignments

# @api.post("/questions/", response=QuestionSchema)
# def create_question(request, data: QuestionSchema):
#     assignment = Assignment.objects.get(id=data.assignment_id)
#     question = Question.objects.create(
#         assignment=assignment,
#         text=data.text,
#         option_a=data.option_a,
#         option_b=data.option_b,
#         option_c=data.option_c,
#         option_d=data.option_d,
#         correct_answer=data.correct_answer,
#     )
#     return question
