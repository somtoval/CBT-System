from django.contrib import admin
from .models import Exam, Question, Option, Candidate, Answer

# Inline class for Options to be displayed within the Question admin
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Number of extra option fields to display by default

# Admin for Questions with options inline
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'text')
    inlines = [OptionInline]
    search_fields = ('text',)

# Admin for Exams with display of key details
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'duration', 'date_created')
    search_fields = ('name',)

# # Admin for Candidates with filters for done status and search by name/email
# class CandidateAdmin(admin.ModelAdmin):
#     list_display = ('firstname', 'lastname', 'email', 'exam', 'registration_date', 'score', 'done', 'examcode')
#     list_filter = ('done', 'exam')
#     search_fields = ('firstname', 'lastname', 'email', 'examcode')

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phone', 'exam_list', 'registration_date', 'done')
    list_filter = ('done', 'exams')  # Filter candidates by completed status and exams

    # Method to display related exams in list_display
    def exam_list(self, obj):
        return ", ".join([exam.name for exam in obj.exams.all()])
    
    exam_list.short_description = "Exams"  # Label for the column in the admin list view


# Admin for Answers to track each candidate's answer per question
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'question', 'selected_option')
    search_fields = ('candidate__firstname', 'candidate__lastname', 'question__text')
    list_filter = ('question__exam',)

# Register all models
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Option)
