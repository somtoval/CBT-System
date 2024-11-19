from django.db import models
import random
import string

# Exam Model: Represents an exam, e.g., "Entrance Exam", containing multiple subjects.
class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    duration = models.DurationField()  # Store duration as a time interval
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Question Model: Represents each question of an exam.
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()  # The question text

    def __str__(self):
        return f"{self.exam.name} - {self.text[:50]}"  # Display part of the question text


# Option Model: Represents options for each question.
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)  # Option text
    is_correct = models.BooleanField(default=False)  # Marks if this option is the correct answer

    def __str__(self):
        return f"{self.text} ({'Correct' if self.is_correct else 'Incorrect'})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'text'],
                name='unique_option_per_question'
            )
        ]


# Candidate Model: Links each candidate to an exam.
class Candidate(models.Model):
    firstname = models.CharField(max_length=200, blank=True, null=True)
    lastname = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    examcode = models.CharField(max_length=5, unique=True, editable=False)  # Unique 5-character alphanumeric code
    exams = models.ManyToManyField(Exam, related_name="candidates")
    registration_date = models.DateTimeField(auto_now_add=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    done = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.examcode:
            self.examcode = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


# Answer Model: Stores users' selected options for each question.
class Answer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="answers", null=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="answers")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['candidate', 'question'],
                name='unique_answer_per_candidate_per_question'
            )
        ]

    def __str__(self):
        return f"{self.candidate.firstname} {self.candidate.lastname} - {self.question.text[:50]} - {self.selected_option.text}"
