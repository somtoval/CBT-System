from rest_framework import serializers
from .models import Candidate, Question, Exam, Option

# class ExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exam
#         fields = ['id', 'name', 'description', 'duration']

# class CandidateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Candidate
#         fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'exam', 'registration_date', 'score', 'done']

# from rest_framework import serializers
# from .models import Candidate, Question, Exam

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'name', 'description', 'duration']

# class CandidateSerializer(serializers.ModelSerializer):
#     exam_ids = serializers.ListField(
#         child=serializers.IntegerField(), write_only=True, required=False
#     )  # Accept a list of exam IDs for registration
#     exams = ExamSerializer(many=True, read_only=True)  # Display exams in detail on retrieval

#     class Meta:
#         model = Candidate
#         fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'exam_ids', 'exams', 'registration_date', 'score', 'done']

#     def create(self, validated_data):
#         # Extract exam IDs and create a candidate
#         exam_ids = validated_data.pop('exam_ids', [])
#         candidate = Candidate.objects.create(**validated_data)
#         # Set the exams for the candidate
#         candidate.exams.set(Exam.objects.filter(id__in=exam_ids))
#         return candidate

#     def update(self, instance, validated_data):
#         # Handle update logic, including updating exams
#         exam_ids = validated_data.pop('exam_ids', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
#         if exam_ids is not None:
#             instance.exams.set(Exam.objects.filter(id__in=exam_ids))
#         return instance


class CandidateSerializer(serializers.ModelSerializer):
    exams = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Exam.objects.all()
    )  # Handle exams as a list of primary keys

    class Meta:
        model = Candidate
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'exams', 'registration_date', 'score', 'done']
        read_only_fields = ['id', 'registration_date', 'examcode', 'score', 'done']

    # The default ModelSerializer.create does not handle many-to-many relationships properly during creation. It requires a separate step to associate many-to-many related objects.
    def create(self, validated_data):
        # Handle many-to-many relationships
        exams = validated_data.pop('exams', [])
        candidate = Candidate.objects.create(**validated_data)
        candidate.exams.set(exams)
        return candidate


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'exam', 'text']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'
