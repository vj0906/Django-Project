from multiprocessing import context
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.db.models import Sum,F, ExpressionWrapper, fields
from .models import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
import logging

# Create your views here.
def home(request):
    context = {'categories' : Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"api/get_quiz/?category={request.GET.get('category')}")
    return render(request, 'home.html',context)

def quiz(request):
    context= {'category': request.GET.get('category')}
    return render(request, 'quiz.html',context)

def get_quiz(request):
    try:
        category_filter = request.GET.get('category')
        question_objs = Question.objects.all()

        if category_filter:
            question_objs = question_objs.filter(category__category_name__icontains=category_filter)

        data = []
        for question_obj in question_objs:
            data.append({
                "uid": question_obj.uid,
                "category": question_obj.category.category_name,
                "question": question_obj.questions,
                "marks": question_obj.marks,
                "answers": question_obj.get_answer()
            })

        payload = {'status': True, 'data': data}
        return JsonResponse(payload)

    except Exception as e:
        print(e)
        payload = {'status': False, 'error': 'Something went wrong'}
        return JsonResponse(payload)

def score_feedback(request):
    score = request.GET.get('score', 0)  # Default to 0 if score is not present
    total_possible_score = request.GET.get('total_possible_score', 0)

    return render(request, 'score_feedback.html', {'score': score, 'total_possible_score':total_possible_score})

# def signup(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)  # Log in the user after successful signup
#             return redirect('')  # Redirect to the home page
#     else:
#         form = UserCreationForm()
#         print("Not Valid")

#     return render(request, 'signup.html', {'form': form})
logger = logging.getLogger(__name__)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user after successful signup
            return redirect('home')  # Redirect to the home page
        else:
            logger.warning("Form is not valid.")
            logger.debug(form.errors)  # Log form errors for debugging
            print(form.errors)  # Print form errors to console
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def submit_quiz(request):
    if request.method == 'POST':
        try:
            category = request.POST.get('category')
            # Calculate the score based on the selected answers
            selected_answers = request.POST.getlist('selected_answers[]')
            score = sum([int(answer) for answer in selected_answers])

            # Save the quiz submission to the database (assuming you have a UserSubmission model)
            UserSubmission.objects.create(user=request.user, category=category, score=score)

            payload = {'status': True}
        except Exception as e:
            print(e)
            payload = {'status': False, 'error': 'Something went wrong'}
        return JsonResponse(payload)
    else:
        return JsonResponse({'status': False, 'error': 'Invalid request method'})
    
def save_user_score(request):
    if request.method == 'POST':
        try:
            category_name = request.POST.get('category')
            score = int(request.POST.get('score'))
            total_possible_score = int(request.POST.get('total_possible_score'))

            # Get the Category instance
            category = get_object_or_404(Category, category_name=category_name)

            # Create or update the UserQuizScore instance
            user_score, created = UserQuizScore.objects.get_or_create(
                user=request.user,
                category=category,
                defaults={'score': score, 'total_possible_score': total_possible_score}
            )

            if not created:
                # Update the score if the user has already taken a quiz in this category
                user_score.score = score
                user_score.total_possible_score = total_possible_score
                user_score.save()

            payload = {'status': True}
        except Exception as e:
            print(e)
            payload = {'status': False, 'error': 'Something went wrong'}
        return JsonResponse(payload)
    else:
        return JsonResponse({'status': False, 'error': 'Invalid request method'})

def user_dashboard(request):
    user_scores = UserQuizScore.objects.filter(user=request.user)
    quiz_submissions = UserSubmission.objects.filter(user=request.user)

    category_scores = {score.category.category_name: score.score for score in user_scores}
    quiz_results = [{'category': submission.category, 'score': submission.score} for submission in quiz_submissions]

    # Calculate category percentages
    category_percentages = {}
    for category in category_scores:
        total_marks_possible = Question.objects.filter(category__category_name=category).aggregate(sum_marks=models.Sum('marks'))['sum_marks']
        if total_marks_possible:
            percentage = (category_scores[category] / total_marks_possible) * 100
            category_percentages[category] = round(percentage, 2)
        else:
            category_percentages[category] = 0.0  # Set to 0 if there are no marks possible for the category

    context = {
        'user_scores': category_scores,
        'quiz_results': quiz_results,
        'category_percentages': category_percentages,
    }

    return render(request, 'dashboard.html', context)

def category_leaderboard(request, category_name):
    # Retrieve the top 5 scores for the specified category
    top_scores = (
        UserQuizScore.objects
        .filter(category__category_name=category_name)
        .order_by('-score')[:5]
        .annotate(percentage=ExpressionWrapper(F('score') * 100 / F('total_possible_score'), output_field=fields.FloatField()))
    )

    context = {
        'category_name': category_name,
        'top_scores': top_scores,
    }

    return render(request, 'category_leaderboard.html', context)






