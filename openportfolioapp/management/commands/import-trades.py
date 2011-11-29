from django.core.management.base import BaseCommand, CommandError
import os
from openportfolioapp.models import Investment,Portfolio,TradeDataFile

class Command(BaseCommand):
    args = ''
    help = 'Imports trade files from the import dir for bulk processing'

    def handle(self, *args, **options):

        IMPORT_DIR='import'

        files=os.listdir(IMPORT_DIR)

        for f in files:
            
            try:
                i_id=f.split('_')[0]
                p_id=f.split('_')[1]
            
            except:
            
                self.stdout.write('%s is not in the expected format\n' % f)    
                continue
            
            try:
                i=Investment.objects.filter(pk=i_id)[0]
		    
            except:
		        
		        self.stdout.write('No investment match found for %s\n' % f)
		        continue
		        
            try:
                p=Portfolio.objects.get(name=p_id)
                
            except:

		        self.stdout.write('No portfolio match found for %s\n' % f)
		        continue
		    
		        
            self.stdout.write('File %s has data for %s, investment %s\n' % (f,p,i))
            
            #delete old trade files 
            try:
                tf=TradeDataFile.objects.filter(file_name=os.path.join(IMPORT_DIR,f)).delete()
            except:
                pass
            
            tf=TradeDataFile()
            tf.portfolio=p
            tf.investment=i
            tf.file_name=os.path.join(IMPORT_DIR,f)
            
            try:
                tf.save()
                self.stdout.write('..successfully saved the trade file\n')
                
            except:
                self.stdout.write('..error saving the trade file\n')
            
            
            
            