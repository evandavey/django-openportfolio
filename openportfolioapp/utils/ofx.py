from BeautifulSoup import BeautifulStoneSoup
from datetime import *

def clean_ofx_str(str):

    str=str.replace("\t","")
    str=str.replace("\n","")
    str=str.replace("\r","")

    return str


def parse_ofx_date(dt):

	#handle YYYYMMDD0000 format
	#print len(dt)
	if len(dt) == 14:
		#print 'long date found'
		dt = datetime.strptime(dt, "%Y%m%d000000")
	else:
		dt = datetime.date(datetime.strptime(dt, "%Y%m%d"))


	#print dt
	#dt = time.strftime("%Y%m%d", dt)

	return dt

class Ofx(object):
    pass

class Account(object):
    def __init__(self):
        self.number = ''
        self.routing_number = ''
        self.statement = None
        self.currency = ''

class Statement(object):
    def __init__(self):
        self.start_date = ''
        self.end_date = ''
        self.transactions = []

class Transaction(object):
    def __init__(self):
        self.name = ''
        self.type = ''
        self.date = ''
        self.amount = ''
        self.id = ''
        self.memo = ''
        self.payee = ''

class Institution(object):
    pass

class OfxParser(object):
    @classmethod
    def parse(cls_, file_handle):
        ofx_obj = Ofx()
        
        
        ofx = BeautifulStoneSoup(file_handle)
        stmtrs_ofx = ofx.find('stmtrs')
        if stmtrs_ofx:
            ofx_obj.bank_account = cls_.parseStmtrs(stmtrs_ofx)
        
        #westpac has "CCSTMTRS"
        else:
            stmtrs_ofx = ofx.find('ccstmtrs')
            if stmtrs_ofx:
                ofx_obj.bank_account = cls_.parseStmtrs(stmtrs_ofx)


        return ofx_obj

    @classmethod
    def parseStmtrs(cls_, stmtrs_ofx):
        ''' Parse the <STMTRS> tag and return an Account object. '''
        account = Account()
        acctid_tag = stmtrs_ofx.find('acctid')
        if hasattr(acctid_tag, 'contents'):
            try:
                account.number = acctid_tag.contents[0]
            except:
                account.number=""
                
        bankid_tag = stmtrs_ofx.find('bankid')
        if hasattr(bankid_tag, 'contents'):
            try:
                account.routing_number = bankid_tag.contents[0]
            except:
                account.routing_number=""

        curr_tag = stmtrs_ofx.find('curdef')
        if hasattr(curr_tag, 'contents'):
            try:
                account.currency = curr_tag.contents[0]
            except:
                account.currency = ""

        if stmtrs_ofx:
            account.statement = cls_.parseStatement(stmtrs_ofx)
        return account
    
    @classmethod
    def parseStatement(cls_, stmt_ofx):
        '''
        Parse a statement in ofx-land and return a Statement object.
        '''
        statement = Statement()
        dtstart_tag = stmt_ofx.find('dtstart')
        if hasattr(dtstart_tag, "contents"):
            statement.start_date = dtstart_tag.contents[0]
        dtend_tag = stmt_ofx.find('dtend')
        if hasattr(dtend_tag, "contents"):
            statement.end_date = dtend_tag.contents[0].strip()
        ledger_bal_tag = stmt_ofx.find('ledgerbal')
        if hasattr(ledger_bal_tag, "contents"):
            balamt_tag = ledger_bal_tag.find('balamt')
        if stmtrs_ofx:
            account.statement = cls_.parseStatement(stmtrs_ofx)
        return account
    
    @classmethod
    def parseStatement(cls_, stmt_ofx):
        '''
        Parse a statement in ofx-land and return a Statement object.
        '''
        statement = Statement()
        dtstart_tag = stmt_ofx.find('dtstart')
        if hasattr(dtstart_tag, "contents"):
            statement.start_date = dtstart_tag.contents[0]
        dtend_tag = stmt_ofx.find('dtend')
        if hasattr(dtend_tag, "contents"):
            statement.end_date = dtend_tag.contents[0].strip()
        ledger_bal_tag = stmt_ofx.find('ledgerbal')
        if hasattr(ledger_bal_tag, "contents"):
            balamt_tag = ledger_bal_tag.find('balamt')
            if hasattr(balamt_tag, "contents"):
                statement.balance = balamt_tag.contents[0]
        avail_bal_tag = stmt_ofx.find('availbal')
        if hasattr(avail_bal_tag, "contents"):
            balamt_tag = avail_bal_tag.find('balamt')
            if hasattr(balamt_tag, "contents"):
                statement.available_balance = balamt_tag.contents[0]
        for transaction_ofx in stmt_ofx.findAll('stmttrn'):
            statement.transactions.append(cls_.parseTransaction(transaction_ofx))
        return statement

    @classmethod
    def parseTransaction(cls_, txn_ofx):
        '''
        Parse a transaction in ofx-land and return a Transaction object.
        '''
        transaction = Transaction()

        type_tag = txn_ofx.find('trntype')
        if hasattr(type_tag, 'contents'):
            transaction.type = type_tag.contents[0].lower()

        name_tag = txn_ofx.find('name')
        if hasattr(name_tag, "contents"):
            try:
                transaction.payee = name_tag.contents[0]
            except:
                transaction.payee = ""

        memo_tag = txn_ofx.find('memo')
        if hasattr(memo_tag, "contents"):
            transaction.memo = memo_tag.contents[0]

        amt_tag = txn_ofx.find('trnamt')
        if hasattr(amt_tag, "contents"):
            transaction.amount = amt_tag.contents[0]

        date_tag = txn_ofx.find('dtposted')
        if hasattr(date_tag, "contents"):
            transaction.date = date_tag.contents[0]

        id_tag = txn_ofx.find('fitid')
        if hasattr(id_tag, "contents"):
            transaction.id = id_tag.contents[0]

        return transaction


def ofx_export ( path, data):
    """
        Creates an ofx file
		path: path to save the file
   		data: data array
		
    """

    accounts={}
    today = datetime.now().strftime('%Y%m%d')
    for row in data:

        uacct="%s-%s" % (row["bankid"],row["accountid"])
        acct = accounts.setdefault(uacct,{})

        acct['BANKID'] = row["bankid"]
        acct['ACCTID'] = row["accountid"]
        acct['TODAY'] = today

        acct['CURDEF'] = row["currency"]

        trans=acct.setdefault('trans',[])

        tran = {}
        tran['DTPOSTED']=row["date"]
        tran['TRNAMT']=row["value"]
        tran['FITID']=row["transid"]
        tran['PAYEE']=row["payee"]
        tran['MEMO']=row["memo"]
        tran['CHECKNUM']=''

        tran['TRNTYPE'] = tran['TRNAMT'] >0 and 'CREDIT' or 'DEBIT'
        trans.append(tran)


    # output

    out=open(path,'w')

    out.write (
        """
        <OFX>
            <SIGNONMSGSRSV1>
               <SONRS>
                <STATUS>
                    <CODE>0</CODE>
                        <SEVERITY>INFO</SEVERITY>
                    </STATUS>
                    <DTSERVER>%(DTSERVER)s</DTSERVER>
                <LANGUAGE>ENG</LANGUAGE>
            </SONRS>
            </SIGNONMSGSRSV1>
            <BANKMSGSRSV1><STMTTRNRS>
                <TRNUID>%(TRNUID)d</TRNUID>
                <STATUS><CODE>0</CODE><SEVERITY>INFO</SEVERITY></STATUS>

        """ % {'DTSERVER':today,
              'TRNUID':int(time.mktime(time.localtime()))}
    )

    for acct in accounts.values():
        out.write(
            """
            <STMTRS>
                <CURDEF>%(CURDEF)s</CURDEF>
                <BANKACCTFROM>
                    <BANKID>%(BANKID)s</BANKID>
                    <ACCTID>%(ACCTID)s</ACCTID>
                    <ACCTTYPE>CHECKING</ACCTTYPE>
                </BANKACCTFROM>
                <BANKTRANLIST>
                    <DTSTART>%(TODAY)s</DTSTART>
                    <DTEND>%(TODAY)s</DTEND>

            """ % acct
        )

        for tran in acct['trans']:
            out.write (
                """
                        <STMTTRN>
                            <TRNTYPE>%(TRNTYPE)s</TRNTYPE>
                            <DTPOSTED>%(DTPOSTED)s</DTPOSTED>
                            <TRNAMT>%(TRNAMT)s</TRNAMT>
                            <FITID>%(FITID)s</FITID>

                """ % tran
            )
            if tran['CHECKNUM'] is not None and len(tran['CHECKNUM'])>0:
                out.write(
                """
                            <CHECKNUM>%(CHECKNUM)s</CHECKNUM>
                """ % tran
                )
            out.write(
                """
                            <NAME>%(PAYEE)s</NAME>
                            <MEMO>%(MEMO)s</MEMO>
                """ % tran
            )
            out.write(
                """
                        </STMTTRN>
                """
            )

        out.write (
            """
                </BANKTRANLIST>
                <LEDGERBAL>
                    <BALAMT>0</BALAMT>
                    <DTASOF>%s</DTASOF>
                </LEDGERBAL>
            </STMTRS>
            """ % today
        )

    out.write ( "</STMTTRNRS></BANKMSGSRSV1></OFX>" )
    out.close()