# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from django.http import HttpResponseRedirect
from django.http import Http404

from django.contrib.auth.models import User

from living.models import Expense,Recurring,Comment,MyIndex,Balance,Tag
from living.forms import CreateNewRecordForm,CreateNewRecurringForm

@login_required
def index(request,template_name="living/index.html",**kwargs):
    try:
        balance = Balance.objects.get(user_id=request.user.id)
    except Balance.DoesNotExist:
        balance = Balance()
    kwargs['balance'] = balance
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def create_new_record(request, template_name="living/create_new_record.html"
, **kwargs):
    if request.method == "GET":
        form = CreateNewRecordForm()
        import datetime
        form.data['spent_on'] = datetime.date.today().strftime("%Y-%m-%d")
        try:
            last_expense = Expense.objects.filter(creater_id=request.user.id).order_by("-created_on")[0]
            form.data['payer_names'] = last_expense.payer_names
            form.data['consumer_names'] = last_expense.consumer_names
        except:
            pass
    elif request.method == "POST":
        form = CreateNewRecordForm(request.POST)
        if form.is_valid():
            exp = Expense()
            exp.create_from_form(form)
            exp.creater_name = request.user.username
            exp.creater_id = request.user.id
            exp.save()
            exp.update_relative()
            return HttpResponseRedirect(reverse('living_view_expense_id',args=[exp.expense_id]))
    kwargs['form'] = form
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def view_expenses(request, template_name="living/view_expenses.html",**kwargs):
    offset,limit = 0,5
    kwargs['has_no_more']='Yes'
    try:
        mi = MyIndex.objects.get(user_id=request.user.id)
        if request.is_ajax():
            offset = int(request.POST["offset"]) 
            template_name="living/view_expenses_more.html"
        if mi.expense_ids:
            all_ids = mi.expense_ids.split(',')
            expense_ids = [ int(x) for x in all_ids[offset:offset+limit] ]
            expenses = Expense.objects.filter(expense_id__in=expense_ids).order_by("-spent_on","-created_on")
            if offset+limit<=len(all_ids):
                kwargs['has_no_more']=''
        else:
            expenses = []
    except MyIndex.DoesNotExist:
        expenses = []
    kwargs['expenses'] = expenses
    kwargs['offset'] = offset
    kwargs['limit'] = limit
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))
    
def view_expense_id(request, expense_id, template_name="living/view_expense_id.html",**kwargs):
    try:
        expense = Expense.objects.get(expense_id=expense_id)
        expense.spent_on = expense.spent_on.strftime("%Y-%m-%d")
    except Expense.DoesNotExist:
        raise Http404
    kwargs['expense'] = expense
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def create_new_recurring(request, template_name="living/create_new_recurring.html", **kwargs):
    if request.method == "GET":
        form = CreateNewRecurringForm()
        import datetime
        form.data['started_on'] = datetime.date.today().strftime("%Y-%m-%d")
        form.data['period'] = 7
        try:
            last_expense = Recurring.objects.filter(creater_id=request.user.id).order_by("-created_on")[0]
            form.data['consumer_names'] = last_expense.consumer_names
        except:
            pass
    elif request.method == "POST":
        form = CreateNewRecurringForm(request.POST)
        if form.is_valid():
            rec = Recurring()
            rec.create_from_form(form)
            rec.creater_name = request.user.username
            rec.creater_id = request.user.id
            rec.save()
            rec.update_relative()
            return HttpResponseRedirect(reverse('living_view_recurring_id',args=[rec.recurring_id]))
    kwargs['form'] = form
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def view_recurrings(request, template_name="living/view_recurrings.html",**kwargs):
    offset,limit = 0,5
    kwargs['has_no_more']='Yes'
    try:
        mi = MyIndex.objects.get(user_id=request.user.id)
        if request.is_ajax():
            offset = int(request.POST["offset"]) 
            template_name="living/view_recurrings_more.html"
        if mi.recurring_ids:
            all_ids = mi.recurring_ids.split(',')
            recurring_ids = [ int(x) for x in all_ids[offset:offset+limit] ]
            recurrings = Recurring.objects.filter(recurring_id__in=recurring_ids).order_by("-started_on","-created_on")
            if offset+limit<=len(all_ids):
                kwargs['has_no_more']=''
        else:
            recurrings = []
    except MyIndex.DoesNotExist:
        recurrings = []
    kwargs['recurrings'] = recurrings
    kwargs['offset'] = offset
    kwargs['limit'] = limit
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))
    
def view_recurring_id(request, recurring_id, template_name="living/view_recurring_id.html", **kwargs):
    try:
        recurring = Recurring.objects.get(recurring_id=recurring_id)
        recurring.started_on = recurring.started_on.strftime("%Y-%m-%d")
    except Expense.DoesNotExist:
        raise Http404
    kwargs['recurring'] = recurring
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))

@login_required
def view_statement(request, template_name="living/view_statement.html",**kwargs):
    offset,limit = 0,5
    kwargs['has_no_more']='Yes'
    try:
        if request.is_ajax():
            offset = int(request.POST["offset"]) 
            template_name="living/view_statement_more.html"
        mi = MyIndex.objects.get(user_id=request.user.id)
        statement,all_ids = mi.generate_statement(offset=offset,limit=limit)
        kwargs['statement'] = statement 
        if offset+limit<=len(all_ids):
            kwargs['has_no_more']=''
    except MyIndex.DoesNotExist:
        kwargs['statement'] = [] 
    try:
        balance = Balance.objects.get(user_id=request.user.id)
    except Balance.DoesNotExist:
        balance = Balance()
    kwargs['balance'] = balance 
    kwargs['offset'] = offset
    kwargs['limit'] = limit
    return render_to_response(template_name,kwargs,context_instance=RequestContext(request))
