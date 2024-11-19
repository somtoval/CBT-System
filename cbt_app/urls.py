from django.urls import path
from . import views

urlpatterns = [
    # Individual Question CRUD view
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question-detail'),
    
    # List and create questions for a specific exam
    path('questions/<int:exam_id>/', views.questions_view, name='exam-questions'),
    
    # List and create options for a specific question
    path('options/<int:question_id>/', views.option_view, name='question-options'),
    
    # Get candidates registered for a specific exam
    path('candidates/<int:exam_id>/', views.get_candidates_by_exam, name='exam-candidates'),
    
    # Create and list candidates
    path('create-candidate/', views.CandidateView.as_view(), name='create-candidate'),
]
