"""
Living 
"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from living.views import index
from living.views import create_new_record,view_expenses,view_expense_id
from living.views import create_new_recurring,view_recurrings,view_recurring_id
from living.views import view_statement

urlpatterns = patterns('',
    # Create
    url(r'^create/expense/$', create_new_record, {}, name='living_create_new_record' ),
    url(r'^create/recurring/$', create_new_recurring, {}, name='living_create_new_recurring'),

    # View
    url(r'^expense/$',view_expenses,{},name='living_view_records'),
    url(r'^expense/(?P<expense_id>\d+)/$',view_expense_id,{},name='living_view_expense_id'),
    url(r'^recurring/$',view_recurrings,{},name='living_view_recurrings'),
    url(r'^recurring/(?P<recurring_id>\d+)/$',view_recurring_id,{},name='living_view_recurring_id'),
    url(r'^$', index, {}, name='living_index' ),


    # Statemtns
    url(r'^statement/$',view_statement,{},name='living_view_statement'),
)
