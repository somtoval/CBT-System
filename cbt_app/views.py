# from django.shortcuts import render
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Candidate, Exam, Question, Option, Answer
# from .serializers import CandidateSerializer, QuestionSerializer, ExamSerializer, OptionSerializer

# from rest_framework import generics

# @api_view(['GET'])
# def get_candidates_by_exam(request, exam_id):
#     try:
#         # Check if the exam exists
#         exam = Exam.objects.get(id=exam_id)
#     except Exam.DoesNotExist:
#         return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

#     # Filter candidates by the specified exam
#     candidates = Candidate.objects.filter(exam=exam)
#     serializer = CandidateSerializer(candidates, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# class CandiateView(generics.ListCreateAPIView):
#     queryset = Candidate.objects.all()
#     serializer_class = CandidateSerializer

#     # Method Override: create (Overridding the create method to customize the behavior of the POST request.)
#     def create(self, request, *args, **kwargs):
#         # The get_serializer method initializes the serializer (CandidateSerializer) with the data sent in the request.
#         # The data=request.data argument passes the incoming JSON payload to the serializer for validation and processing.
#         serializer = self.get_serializer(data=request.data)
        
#         # This validates the data against the rules defined in the CandidateSerializer. If the data is invalid a ValidationError is raised. Django REST Framework handles this error and returns an appropriate HTTP 400 Bad Request response.
#         serializer.is_valid(raise_exception=True)

#         # This method calls the serializer's save method to create and save the new Candidate object in the database.
#         self.perform_create(serializer)

#         # The get_success_headers method generates headers for the response, such as the Location header, which points to the URL of the newly created object.
#         headers = self.get_success_headers(serializer.data)
#         return Response(
#             {"message": "Candidate created successfully", "data": serializer.data},
#             status=status.HTTP_201_CREATED,
#             headers=headers,
#         )

# # Returns, Updates, Deletes a specific question 
# class QuestionView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
#     queryset = Question.objects.all()
#     serializer_class = QuestionSerializer

# #  Returns and create all questions associated with a particular exam
# @api_view(['GET', 'POST'])
# def QuestionsView(request, exam_id):
#     if request.method == 'GET':
#         try:
#             # Check if the exam exists
#             exam = Exam.objects.get(id=exam_id)
#         except Exam.DoesNotExist:
#             return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Filter candidates by the specified exam
#         questions = Question.objects.filter(exam=exam)
#         serializer = QuestionSerializer(questions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         data = request.data
#         data['exam'] = Exam.objects.get(id=data['exam'])
#         serializer = QuestionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'Message': 'Question Created'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# @api_view(['GET', 'POST'])
# def OptionView(request, question_id):
#     if request.method == 'GET':
#         try:
#             # Check if the question exists
#             question = Question.objects.get(id=question_id)
#         except Question.DoesNotExist:
#             return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Filter candidates by the specified exam
#         options = Option.objects.filter(question=question)
#         serializer = OptionSerializer(options, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         data = request.data
#         data['question'] = Question.objects.get(id=data['question'])
#         serializer = OptionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'Message': 'Option Created'}, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Candidate, Exam, Question, Option
from .serializers import CandidateSerializer, QuestionSerializer, ExamSerializer, OptionSerializer


@api_view(['GET'])
def get_candidates_by_exam(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

    candidates = Candidate.objects.filter(exams=exam)
    serializer = CandidateSerializer(candidates, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CandidateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer

    # Method Override: create (Overridding the create method to customize the behavior of the POST request.)
    def create(self, request, *args, **kwargs):
        # The get_serializer method initializes the serializer (CandidateSerializer) with the data sent in the request.
        # The data=request.data argument passes the incoming JSON payload to the serializer for validation and processing.
        serializer = self.get_serializer(data=request.data)
        # This validates the data against the rules defined in the CandidateSerializer. If the data is invalid a ValidationError is raised. Django REST Framework handles this error and returns an appropriate HTTP 400 Bad Request response.
        serializer.is_valid(raise_exception=True)
        # This method calls the serializer's save method to create and save the new Candidate object in the database.
        self.perform_create(serializer)
        # The get_success_headers method generates headers for the response, such as the Location header, which points to the URL of the newly created object.
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Candidate created successfully", "data": serializer.data},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

class QuestionView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

@api_view(['GET', 'POST'])
def questions_view(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        return Response({"error": "Exam not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        questions = Question.objects.filter(exam=exam)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        data['exam'] = exam.id
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Question created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def option_view(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        options = Option.objects.filter(question=question)
        serializer = OptionSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        data = request.data
        data['question'] = question.id
        serializer = OptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Option created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
