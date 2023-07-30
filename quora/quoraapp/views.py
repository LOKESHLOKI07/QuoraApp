from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from .forms import QuestionForm, AnswerForm, ReplyForm
from .models import Question, Answer, Like

def home(request):
    questions = Question.objects.all()
    return render(request, 'home.html', {'questions': questions})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.created_by = request.user
            question.save()
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

@login_required
def post_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.created_by = request.user
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'post_answer.html', {'form': form, 'question': question})

@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    try:
        Like.objects.get(user=request.user, answer=answer).delete()
    except Like.DoesNotExist:
        Like.objects.create(user=request.user, answer=answer)
    return redirect('question_detail', question_id=answer.question.id)

@login_required
def like_question(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
        like = Like.objects.get(question=question, user=request.user)
        like.user.remove(request.user)
    except Like.DoesNotExist:
        Like.objects.create(question=question)
        question.likes.add(request.user)
    return redirect('question_detail', question_id=question_id)


def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return render(request, 'logout.html')

def user_registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')  # Get the username from the form
            raw_password = form.cleaned_data.get('password1')  # Get the raw (unhashed) password from the form
            # Authenticate the newly registered user and log them in
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})

# The reverse function should be used like this:
def some_function(request):
    question_id = 123
    url = reverse('question_detail', kwargs={'question_id': question_id})
    # Do something with the generated URL

def question_detail(request, question_id):
    # Retrieve the question using the question_id or return 404 if not found
    question = get_object_or_404(Question, pk=question_id)

    # You can add additional logic here if needed, such as retrieving answers related to this question

    return render(request, 'question_detail.html', {'question': question})

@login_required
def profile(request):
    return render(request, 'home.html')

@login_required
def reply_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.question = question
            reply.save()
            return redirect('question_detail', question_id=question.id)
    else:
        form = ReplyForm()

    return render(request, 'reply_question.html', {'question': question, 'form': form})