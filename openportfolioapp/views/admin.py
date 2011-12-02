from django.core import management

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
import datetime

#management.call_command('flush', verbosity=0, interactive=False)
#management.call_command('loaddata', 'test_data', verbosity=0)



def daily(request):
    
    #management.call_command('import-trades', 'import',verbosity=1)
    messages.add_message(request, messages.SUCCESS, 'Daily process has been run')
    
    return redirect('/admin')
    
    
    #