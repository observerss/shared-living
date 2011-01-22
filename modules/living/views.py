# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.http import Http404

from django.contrib.auth.models import User

from living.models import Expense,Recurring,Comment,MyIndex
from living.forms import CreateNewRecordForm

@login_required
def index(request,template_name="living/index.html",**kwargs):
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def create_new_record(request, template_name="living/create_new_record.html"
, **kwargs):
    if request.method == "GET":
        form = CreateNewRecordForm()
        import datetime
        form.data['spent_on'] = datetime.date.today().strftime("%Y-%m-%d")
    elif request.method == "POST":
        form = CreateNewRecordForm(request.POST)
        if form.is_valid():
            exp = Expense()
            exp.create_from_form(form)
            exp.creater_name = request.user.username
            exp.creater_id = request.user.id
            exp.save()
            exp.update_relative()
            return HttpResponseRedirect('done/')
    kwargs['form'] = form
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def view_expenses(request, template_name="living/view_expenses.html",**kwargs):
    offset,limit = 0,5
    try:
        mi = MyIndex.objects.get(user_name=request.user.username)
        if request.is_ajax():
            offset = int(request.POST["offset"]) 
            template_name="living/view_expenses_more.html"
        print offset,offset+limit
        expense_ids = [ int(x) for x in mi.expense_ids.split(',',limit+offset+1)[offset:offset+limit] ]
        print expense_ids
        expenses = Expense.objects.filter(expense_id__in=expense_ids).order_by("-spent_on","-created_on")
    except MyIndex.DoesNotExist:
        expenses = []
    kwargs['expenses'] = expenses
    kwargs['offset'] = offset
    kwargs['limit'] = limit
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))
    
def view_expense_id(request, expense_id, template_name="living/view_expense_id.html",**kwargs):
    try:
        expense = Expense.objects.get(expense_id=expense_id)
    except Expense.DoesNotExist:
        raise Http404
    kwargs['expense'] = expense
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

def view_expense_id_ajax_comment_view(request):
    comments = Comment.objects.filter(target_id=target_id,target_name="E").order_by("-created_on")[:20]
    pass
