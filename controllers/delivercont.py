# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def delivery():
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
    
    prods=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
    #prods = db(product_info.posted_by.belongs(friends)).select(orderby=~product_info.product_id,limitby=(0,10))
    #print prods
    return locals()


def confirm_delivery():
    if not auth.user:
        redirect(URL('index'))
        
    delcount=0
    discount=0
    reccount=0
    if auth.user:
        prods=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & (db.product_info.product_status==4)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in prods:
            delcount=delcount+1;
        
        prods=db((db.product_info.product_status==2) & (db.product_info.next_checkpoint_level==auth.user.levelno) & (db.product_info.next_checkpoint==auth.user.place)).select(orderby=db.product_info.product_id,limitby=(0,10))
        for prod in prods:
            reccount=reccount+1;
            
        prods=db((db.product_info.current_pos==auth.user.place) & (db.product_info.current_pos_level==auth.user.levelno) & ((db.product_info.product_status==1) | (db.product_info.product_status==3))).select(orderby=db.product_info.product_id,limitby=(0,10))
        
        for prod in prods:
            discount=discount+1;
         
        
    record = db.product_info(request.vars.prodid)
    db.product_info.product_id.writable = False
    db.product_info.product_name.writable = False
    db.product_info.company_name.writable = False
    db.product_info.receiver_name.writable=False
    db.product_info.receiver_email.writable=False
    db.product_info.next_checkpoint.writable = False
    db.product_info.next_checkpoint_level.writable = False
    db.product_info.address.writable = False
    db.product_info.destination_place.writable = False
    db.product_info.product_status.writable = False
    db.product_info.current_pos.writable=False
    db.product_info.current_pos_level.writable=False
    record['current_pos']=''
    record['current_pos_level']=''
    record['product_status']=5
    print auth.user.levelno
    print auth.user.place
    form = SQLFORM(db.product_info, record,fields=["product_id","product_name","company_name","receiver_name","receiver_email","next_checkpoint","next_checkpoint_level","address","destination_place","product_status"],submit_button = 'Delivered')
    if form.process().accepted:
       response.flash = 'Details Updated !!'
       redirect(URL('../../default/home'))
    elif form.errors:
       response.flash = 'Error in Data !!'
    return locals()

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
