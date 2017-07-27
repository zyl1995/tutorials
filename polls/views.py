from django.shortcuts import render, get_object_or_404
from polls.models import Question, Choice
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import  RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

# def index(request):
#     question_list = Question.objects.order_by('-publish_data')[:5]
#     # output = ','.join([p.question_text for p in question_list])
#     # return HttpResponse(output)
#     # template = loader.get_template('polls/index.html')
#     # context = RequestContext(request,{
#     #     'question_list':question_list,
#     # })
#     # return HttpResponse(template.render(context))
#     context = {'question_list':question_list}
#     return render(request, 'polls/index.html', context)
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.filter(publish_data__lte=timezone.now()).order_by('-publish_data')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(publish_data__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
# Create your views here.

def detail(request, question_id):
    # try:
    #question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)
    # except Question.DoesNotExist:
    #     raise  Http404("Question does not exist")
    return render(request,'polls/detail.html',{'question':question})
    # return HttpResponse("You're looking at question %s." %question_id)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})
    # response = "You're looking at resluts of question %s."
    # return HttpResponse(response %question_id)

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        select_choice =p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',
                {'question':p,'error_message':'You did not select a choice'}
        )
    else:
        select_choice.votes += 1
        select_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    #return HttpResponse("You're voting on question %s." % question_id)