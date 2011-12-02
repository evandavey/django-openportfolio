from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os,shutil
from openportfolioapp.models import Investment,Portfolio,TradeDataFile

class Command(BaseCommand):
    args = 'import dir'
    help = 'Imports trade files from the import dir for bulk processing'

    def handle(self, *args, **options):

        verbosity = options.get('verbosity', 1)
    
        if len(args) < 1:
			raise CommandError('Requires arguments %s' % self.args)
        
        
        MEDIA_ROOT= options.get('media_root', settings.MEDIA_ROOT)
        
        
        IMPORT_DIR=os.path.join(MEDIA_ROOT,args[0])
        DEST_DIR=os.path.join('datafiles','trades')

        try:
            files=os.listdir(IMPORT_DIR)
        except:
            raise CommandError('Failed to access %s' % IMPORT_DIR)
            
        if verbosity > 0:
            self.stdout.write('Importing %d files from %s to {{MEDIA_ROOT}}\%s' % (len(files),IMPORT_DIR,DEST_DIR))

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
           
           
            oldf=os.path.join(IMPORT_DIR,f)
            newf=os.path.join(DEST_DIR,f)

            #delete old trade files 
            try:
                tf=TradeDataFile.objects.filter(file_name=newf).delete()
            except:
                pass
           
            
            try: 
                shutil.move(oldf,os.path.join(MEDIA_ROOT,newf))
            
                tf=TradeDataFile()
                tf.portfolio=p
                tf.investment=i
                tf.file_name=newf
            
            
                tf.file_name.open()
                print tf.file_name
                tf.save()
                self.stdout.write('..successfully saved the trade file\n')
            
            except:
                import traceback
                self.stdout.write('..error saving %s, skipping\n' % oldf)
                self.stdout.write('%s' % traceback.print_exc())
            
            
            