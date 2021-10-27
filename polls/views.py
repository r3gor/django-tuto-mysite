from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from polls.models import Choice, Question
from django.views import generic
from django.utils import timezone
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

class IndexView(generic.ListView):
  template_name = 'polls/index.html'
  context_object_name = 'latest_question_list'

  def get_queryset(self):
    """
    Return the last five published question (not including those set to be
    published in the future). 
    """
    # return Question.objects.order_by('-pub_date')[:5]
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
  model = Question # django genera el context con los fields del question
  template_name = 'polls/detail.html'

  def get_queryset(self): 
    return Question.objects.filter(pub_date__lte=timezone.now()) 

class ResultsView(generic.DetailView):
  model = Question # django genera el context con los fields del question
  template_name = 'polls/result.html'

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
