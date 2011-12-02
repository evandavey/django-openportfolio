import os,sys
import getopt
import hashlib
from traceback import print_exc
from bankstandardiser import BankDownload

DB_HOST='192.168.0.20'
DB_USER='financedb'
DB_PWORD='financedb'
DB='financedb'

DOWNLOAD_PATH='/Users/evandavey/Dropbox/Cochrane Davey/Finances/Bank Downloads/Original Format/'
OUTPUT_PATH='/Users/evandavey/Documents/openportfolio/import/'

def file_md5(filename):
       md5 = hashlib.md5()
       with open(filename,'rb') as f: 
           for chunk in iter(lambda: f.read(128*md5.block_size), ''): 
               md5.update(chunk)
       return md5.hexdigest()

def main(argv=None):
    if argv is None:
        argv=sys.argv

    try:
        srchpath=argv[1]
    except:  
        srchpath=DOWNLOAD_PATH 
   
    try:
         outpath=argv[2]
    except:  
        outpath=OUTPUT_PATH
   
   
    fileExtList=[".csv",".ofx",".qfx"]


    print "Searching: " + srchpath
    print "Output to: " + outpath

    files=os.listdir(srchpath)

    import MySQLdb
    
    try:
        print 'establishing connection to %s@%s' % (DB,DB_HOST) 
        db=MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PWORD,db=DB)
       
        c=db.cursor(MySQLdb.cursors.DictCursor)
    except:
        print_exc()
        return 1
    
    changed_files=[]    
    for f in files:
        try:

            if os.path.splitext(f)[1] in fileExtList:
                chksum=file_md5(os.path.join(srchpath,f))
                
                sql=""" 
                    SELECT * 
                    FROM downloads
                    WHERE 
                        name='%s'
                
                """ % f
                
                #print sql
                c.execute(sql)
                r=c.fetchone()
              
                if r is None:
                    sql=""" 
                        INSERT INTO downloads
                        VALUES ('%s','%s',NULL,NULL) 

                    """ % (f,chksum)
                    
                    try:
                        c.execute(sql)
                        print "Inserted record for %s,%s" % (f,chksum)
                        changed_files.append(f)
                    except:
                        print "Error insert record for %s" % f
                        print_exc()
                else:
                    if r['chksum'] != chksum:
                        print "Checksums differ for %s" % f
                        changed_files.append(f)
                        
                        sql=""" 
                            UPDATE downloads
                            SET chksum='%s'
                            WHERE 
                                name='%s'
                        """ % (chksum,f)
                        
                        try:
                            c.execute(sql)
                            print "Updated checksum for %s,%s" % (f,chksum)
                        except:
                            print "Error updating record for %s" % f
                            print_exc()
                        
                    else:
                        pass
                        #print "%s unchanged" % f
                
        except:
            print_exc()

        mapping={
            'ing-evan':[1,'Evan Davey'],
            'ing-vanessa':[1,'Vanessa Cochrane'],
            'ing-joint':[1,'Evan Davey & Vanessa Cochrane'],
            'ing-accvanessa':[2,'Vanessa Cochrane'],
            'cbacash-evan':[3,'Evan Davey'],
            'cbacash-vanessa':[3,'Vanessa Cochrane'],
            'rabo-142201002687000':[4,'Evan Davey'],
            'rabo-142201002072100':[4,'Evan Davey & Vanessa Cochrane'],

        }


    for f in changed_files:
        mydownload = BankDownload(os.path.join(srchpath,f))
        r=mydownload.load()

        if r:
            print "Load failed for: "+ srchpath+f
        else:

            ofxfile=mydownload.generatefilename()
            
            print "Generated file name: %s" % ofxfile
            
            dt=ofxfile.split('_')[0]
            bank=ofxfile.split('_')[1]
            acc=ofxfile.split('_')[2]

            try:
                k=bank+'-'+acc
                print "Lookup Key: %s" % k

                i_id=mapping[k][0]
                p_id=mapping[k][1]

                nf="%s_%s_%s.ofx" % (i_id,p_id,dt)
                print "New file name: %s" % nf
                
                mydownload.writeofx(os.path.join(OUTPUT_PATH,nf))
            except:
                print "Error processing file %s" % (f)
                pass

        del mydownload
            
        
        
    c.close()
    db.commit()
    db.close()
   
    return 0


main()