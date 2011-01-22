"""
Living 
"""


from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from living.views import index,create_new_record,view_expenses,view_expense_id

urlpatterns = patterns('',
    url(r'^create/expense/$', create_new_record, {}, name='living_create_new_record' ),
    url(r'^create/expense/done/$', direct_to_template, 
        {'template':'living/create_new_record_done.html'}, name='living_create_new_record_done' ),
    url(r'^expense/$',view_expenses,{},name='living_view_records'),
    url(r'^expense/(?P<expense_id>\d+)/$',view_expense_id,{},name='living_view_expense'),
    url(r'^$', index, {}, name='living_index' ),
)
