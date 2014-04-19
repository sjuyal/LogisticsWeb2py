# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def findParent(search):
    recs=db(search==db.hierarchy_table.level3).select().first()
    parent=recs.level2
    return parent

def tracking():
    msg=""
    flag=""
    print 'heree'
    if request.vars.prodid:
        print 'hellllo'
        prodid=request.vars.prodid
        if is_number(prodid):
            x=int(prodid)-10000;
            print x
            record = db.product_info(x)
            if record:
                #print record
                source=record['source_place']
                flag='hi'
                destination=record['destination_place']
                
                l=[]
                l.append(source)
                if findParent(source)==findParent(destination):
                    if source!=destination:
                        l.append(destination)
                else:
                    if source!=findParent(source):
                        l.append(findParent(source))
                    l.append(findParent(destination))
                    if destination!=findParent(destination):
                        l.append(destination)
                        
                current=record['current_pos']
                status=record['product_status']
                nextchk=record['next_checkpoint']
                expdate=record['expected_arrival_date']
                print current
                print nextchk
                if status==4:
                    msg="Product is out for delivery"
                elif status==5:
                    msg="Product is delivered"
                elif status==1 or (status==2 and current==nextchk):
                     msg="Shipment is yet to leave "+current+" facility"
                elif status==2:
                     msg="Shipment is headed from "+current+" towards " +nextchk+" facility"
                else:
                    msg="Shipment is currently at "+current+" facility"
            else:
                response.flash = T("Product id entered is invalid")
        else:
            response.flash = T("Product id entered is invalid")
    return locals()

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome!! :D")
    return dict(message=T('Please proceed following these instructions!!!!'))

def home():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    if auth.user:
        delcount=0
        discount=0
        reccount=0
        prods=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in prods:
            delcount=delcount+1;
        
        prods=db((db.product_info.product_status==2) & (db.product_info.next_checkpoint_level==auth.user.levelno) & (db.product_info.next_checkpoint==auth.user.place)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in prods:
            reccount=reccount+1;
            
        prods=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & ((db.product_info.product_status==1) | (db.product_info.product_status==3))).select(orderby=db.product_info.product_id,limitby=(0,10))
        
        for prod in prods:
            discount=discount+1;
            
         
        
        return locals();
    else:
        redirect(URL('index'))


def new_entry():
    if auth.user:
        delcount=0
        discount=0
        reccount=0  
        pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in pros:
            delcount=delcount+1;
            
        pros=db((db.product_info.product_status==2) & (db.product_info.next_checkpoint_level==auth.user.levelno) & (db.product_info.next_checkpoint==auth.user.place)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in pros:
            reccount=reccount+1;
                
        pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) &( (db.product_info.product_status==1) | (db.product_info.product_status==3))).select(orderby=db.product_info.product_id,limitby=(0,10))
            
        for prod in pros:
            discount=discount+1;

        message=""
        form = SQLFORM(db.product_info, fields=["id","product_name","company_name","receiver_name","receiver_email","expected_arrival_date","address","destination_place"])
        
        if form.process().accepted:
            x=form.vars.id;
            print x
            print auth.user.place
            db(db.product_info.id == x).update(source_place=auth.user.place)
            db(db.product_info.id == x).update(current_pos=auth.user.place)
            db(db.product_info.id == x).update(current_pos_level=auth.user.levelno)
            db(db.product_info.id == x).update(product_status=1)
            y=x+10000
            db(db.product_info.id == x).update(product_id=y)
            response.flash = 'Entry Created!!'
        elif form.errors:
            response.flash = 'Error in Data !!'
        return locals()
    else:
        redirect(URL('index'))

def profile():
    if not auth.user:
        redirect(URL('index'))
 
    delcount=0
    discount=0
    reccount=0  
    pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
    for prod in pros:
        delcount=delcount+1;
        
    pros=db((db.product_info.product_status==2) & (db.product_info.next_checkpoint_level==auth.user.levelno) & (db.product_info.next_checkpoint==auth.user.place)).select(orderby=db.product_info.product_id,limitby=(0,10))
    for prod in pros:
        reccount=reccount+1;
            
    pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & ((db.product_info.product_status==1) | (db.product_info.product_status==3))).select(orderby=db.product_info.product_id,limitby=(0,10))
        
    for prod in pros:
        discount=discount+1;
        
       
    record = db.auth_user(auth.user.id)
    db.auth_user.id.writable = False
    form = SQLFORM(db.auth_user, record,fields=["first_name","last_name","email","gender","birth_date","phoneno"],submit_button = 'Update')
    
    if form.process().accepted:
       response.flash = 'Details Updated !!'
    elif form.errors:
       response.flash = 'Error in Data !!'
    return locals()
        
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    delcount=0
    discount=0
    reccount=0  
    if auth.user:
        
        pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in pros:
            delcount=delcount+1;
            
        pros=db((db.product_info.product_status==2) & (db.product_info.next_checkpoint_level==auth.user.levelno) & (db.product_info.next_checkpoint==auth.user.place)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in pros:
            reccount=reccount+1;
                
        pros=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & ((db.product_info.product_status==1) | (db.product_info.product_status==3))).select(orderby=db.product_info.product_id,limitby=(0,10))
            
        for prod in pros:
            discount=discount+1;
        
    form=auth()
    message=request.args(0)
    print "hello"
    print message
    if auth.user and message=="login":
        redirect(URL('home'))
    elif auth.user or message=="login" or message=="register" or message=="request_reset_password" or message=="reset_password" or message=="change_password":
        form=auth()
        message=request.args(0)
        print message
        return locals()
    else:
        redirect(URL('index'))

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
