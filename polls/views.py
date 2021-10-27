from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from polls.models import Choice, Question

"""
TODO: Fix the RACE CONDITION:

The code for our vote() view does have a small problem. It first gets 
the selected_choice object from the database, then computes the new 
value of votes, and then saves it back to the database. If two users
of your website try to vote at exactly the same time, this might go
wrong: The same value, let’s say 42, will be retrieved for votes. Then, 
for both users the new value of 43 is computed and saved, but 44 
would be the expected value.

This is called a race condition. If you are interested, you can read 
Avoiding race conditions using F() to learn how you can solve this issue.

"""

def index(request):
  latest_question_list = Question.objects.order_by('-pub_date')[:5]
  return render(request, 'polls\index.html', {'latest_question_list': latest_question_list})

def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/detail.html', context={'question': question})

def results(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  return render(request, 'polls/result.html', {'question': question})

def vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  try:
    selected_choice = question.choice_set.get(pk=request.POST['choice'])
  except (KeyError, Choice.DoesNotExist):
    return render(request, 'polls/detail.html', {
      'question': question,
      'error_message': "You didn't select a choice.",
    })
  else:
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))