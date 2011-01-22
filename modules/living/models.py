from django.db import models
from django.contrib.auth.models import User

from living.forms import CreateNewRecordForm
from living.utils import insert_names

# Create your models here.
class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    creater_id = models.IntegerField(db_index=True)
    creater_name = models.CharField(max_length=30)
    subject = models.CharField(max_length=80)
    message = models.TextField(max_length=65536)
    amount = models.FloatField()
    payer_ids = models.CommaSeparatedIntegerField(max_length=1024)
    payer_names = models.CharField(max_length=65536,default='') 
    consumer_ids = models.CommaSeparatedIntegerField(max_length=1024)
    consumer_names = models.CharField(max_length=65536,default='') 
    tags = models.CharField(max_length=100)
    spent_on = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    in_doubt = models.BooleanField(default=False)
    doubter_id = models.IntegerField(default=0)
    doubter_name = models.CharField(max_length=30,default='')
    is_valid = models.BooleanField(default=True)
    
    def create_update_myindex(self):
        if self.payer_ids:
            user_ids = self.payer_ids+','+self.consumer_ids
        else:
            user_ids = self.consumer_ids
        user_ids = [ int(x) for x in user_ids.split(',') ]
        if self.payer_names:
            user_names = self.payer_names+','+self.consumer_names
        else:
            user_names = self.consumer_names
        user_names = user_names.split(',')
        user_data = []
        existed_ids = set([])
        for i in range(len(user_ids)):
            user_id,user_name = user_ids[i],user_names[i]
            if user_id not in existed_ids:
                existed_ids.add(user_id)
                user_data.append( [user_id,user_name] )
        for user_id,user_name in user_data:
            try:
                mi = MyIndex.objects.get(user_id=user_id)
                mi.expense_ids = insert_names(mi.expense_ids,str(self.expense_id))
            except MyIndex.DoesNotExist:
                mi = MyIndex()
                mi.user_id = user_id
                mi.user_name = user_name
                mi.expense_ids = str(self.expense_id)
            mi.save()
            print mi.user_name,mi.expense_ids

    def create_update_tag(self):
        for tag_name in self.tags.split(','):
            try:
                ta = Tag.objects.get(tag_name=tag_name)
                ta.expense_ids = insert_names(ta.expense_ids,str(self.expense_id))
            except Tag.DoesNotExist:
                ta = Tag()
                ta.total = 0
                ta.tag_name = tag_name
                ta.expense_ids = str(self.expense_id)
            ta.total += float(self.amount)
            ta.save()
    
    def create_update_balance(self):
        user_data = []
        if self.payer_ids:
            for payer_id in self.payer_ids.split(','):
                user_data.append([int(payer_id)])
            counter = 0
            payer_names = self.payer_names.split(',')
            for payer_name in payer_names:
                user_data[counter].append(payer_name)
                user_data[counter].append(1./len(payer_names))
                counter += 1
        else:
            counter = 0
        for consumer_id in self.consumer_ids.split(','):
            user_data.append([int(consumer_id)])
        consumer_names = self.consumer_names.split(',')
        for consumer_name in consumer_names:
            user_data[counter].append(consumer_name)
            user_data[counter].append(-1./len(consumer_names))
            counter += 1
        for user_id,user_name,multiplier in user_data:
            try:
                ba = Balance.objects.get(user_id=user_id)
            except Balance.DoesNotExist:
                ba = Balance()
                ba.user_id = user_id
                ba.user_name = user_name
                ba.balance = 0
            ba.balance += float(self.amount) * multiplier
            ba.save()

    def create_from_form(self,form):
        self.subject = form.data.get('subject')
        self.message = form.data.get('message')
        self.amount = form.data.get('amount')
        self.payer_names = form.data.get('payer_names')
        self.consumer_names = form.data.get('consumer_names')
        self.tags = form.data.get('tags')
        self.spent_on = form.data.get('spent_on')
        payer_ids = []
        for name in self.payer_names.split(','):
            payer_ids.append( User.objects.get(username=name).id )
        consumer_ids = []
        for name in self.consumer_names.split(','):
            consumer_ids.append( User.objects.get(username=name).id )
        self.payer_ids = ','.join([ str(x) for x in payer_ids ])
        self.consumer_ids = ','.join([ str(x) for x in consumer_ids ])

    def create_from_recurring(self,recurring):
        rec = recurring
        self.subject = rec.subject
        self.message = rec.message
        self.amount = rec.amount
        self.payer_names = ''
        self.payer_ids = ''
        self.consumer_names = rec.consumer_names
        self.consumer_ids = rec.consumer_ids
        self.tags = rec.tags
    
    def update_relative(self):
        #update relative databases
        self.create_update_myindex()
        self.create_update_tag()
        self.create_update_balance()

class Recurring(models.Model):
    recurring_id = models.AutoField(primary_key=True)
    creater_id = models.IntegerField(db_index=True)
    creater_name = models.CharField(max_length=30)
    subject = models.CharField(max_length=80)
    message = models.TextField(max_length=65536)
    amount = models.FloatField()
    consumer_ids = models.CommaSeparatedIntegerField(max_length=1024)
    consumer_names = models.CharField(max_length=65536,default='') 
    tags = models.CharField(max_length=100)
    started_on = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    last_recurred = models.DateField(default='1970-01-01')
    period = models.IntegerField(default=7)
    in_doubt = models.BooleanField(default=False)
    doubter_id = models.IntegerField(default=0)
    doubter_name = models.CharField(max_length=30,default='')
    is_valid = models.BooleanField(default=True)

    def create_from_form(self,form):
        self.subject = form.data.get('subject')
        self.message = form.data.get('message')
        self.amount = form.data.get('amount')
        self.consumer_names = form.data.get('consumer_names')
        self.tags = form.data.get('tags')
        self.started_on = form.data.get('started_on')
        self.period = form.data.get('period')
        consumer_ids = []
        for name in self.consumer_names.split(','):
            consumer_ids.append( User.objects.get(username=name).id )
        self.consumer_ids = ','.join([ str(x) for x in consumer_ids ])

    def create_update_myindex(self):
        user_ids = self.consumer_ids
        user_ids = [ int(x) for x in user_ids.split(',') ]
        user_names = self.consumer_names
        user_names = user_names.split(',')
        user_data = []
        existed_ids = set([])
        for i in range(len(user_ids)):
            user_id,user_name = user_ids[i],user_names[i]
            if user_id not in existed_ids:
                existed_ids.add(user_id)
                user_data.append( [user_id,user_name] )
        for user_id,user_name in user_data:
            try:
                mi = MyIndex.objects.get(user_id=user_id)
                mi.recurring_ids = insert_names(mi.recurring_ids,str(self.recurring_id))
            except MyIndex.DoesNotExist:
                mi = MyIndex()
                mi.user_id = user_id
                mi.user_name = user_name
                mi.recurring_ids = str(self.recurring_id)
            mi.save()

    def update_relative(self):
        #update relative databases
        self.create_update_myindex()
        self.update_recurring()

    def incr_datestr(self,datestr,delta):
        import datetime
        try:
            dt = datetime.datetime.strptime(datestr,"%Y-%m-%d")
        except TypeError:
            dt = datestr
        dt += datetime.timedelta(days=delta)
        return dt.strftime("%Y-%m-%d")

    def update_recurring(self):
        import datetime
        now = datetime.date.today().strftime("%Y-%m-%d")
        try:
            last = self.last_recurred.strftime("%Y-%m-%d")
        except AttributeError:
            last = self.last_recurred
        if last == "1970-01-01":
            last = self.incr_datestr(self.started_on,-7) 
        if last < now:
            last = self.incr_datestr(last,7)
            while last <= now:
                expense = Expense()
                print last
                expense.create_from_recurring(self)
                expense.spent_on = last
                expense.creater_id = self.creater_id
                expense.creater_name = self.creater_name
                expense.save()
                expense.update_relative()
                last = self.incr_datestr(last,7)
            self.last_recurred = last

class Comment(models.Model):
    TARGET_CHOICES = (
        ('E', 'Expense'),
        ('R', 'Recurring'),
    )
    comment_id = models.AutoField(primary_key=True)
    target_id = models.IntegerField(db_index=True)
    target_name = models.CharField(max_length=1,choices=TARGET_CHOICES)
    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(max_length=30)
    message = models.IntegerField(max_length=65536)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

class MyIndex(models.Model):
    myindex_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(max_length=30,db_index=True)
    expense_ids = models.CommaSeparatedIntegerField(default='',max_length=65536)
    recurring_ids = models.CommaSeparatedIntegerField(default='',max_length=65536)
    comment_ids = models.CommaSeparatedIntegerField(default='',max_length=65536)
    
    def generate_statement(self,offset=0,limit=5):
        class Journal:
            date = None
            subject = None
            dr = 0
            cr = 0
            balance = 0
            def __init__(self):
                self.dr = self.cr = self.balance = 0
        statement = []
        current_balance = 0
        if self.expense_ids:
            all_ids = [ int(x) for x in self.expense_ids.split(',') ]
            expenses = Expense.objects.filter(expense_id__in=all_ids).order_by("spent_on","created_on")
            for exp in expenses:
                j = Journal()
                j.date = exp.spent_on
                j.subject = exp.subject
                if str(self.user_id) in exp.payer_ids:
                    j.dr += exp.amount/len(exp.payer_ids.split(',')) 
                if str(self.user_id) in exp.consumer_ids:
                    j.cr += exp.amount/len(exp.consumer_ids.split(','))
                current_balance += (j.dr-j.cr)
                j.balance = current_balance
                statement.append(j)
        statement.reverse()
        return statement[offset:offset+limit],all_ids

class Tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=30)
    expense_ids = models.CommaSeparatedIntegerField(max_length=65536,default='')
    total = models.FloatField(default=0)

class Balance(models.Model):
    balance_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(db_index=True)
    user_name = models.CharField(max_length=30)
    balance = models.FloatField(default=0)
