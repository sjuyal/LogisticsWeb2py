# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import *
mail = Mail()                                  # mailer
auth = Auth(globals(),db)                      # authentication/authorization
crud = Crud(globals(),db)                      # for CRUD helpers using auth
service = Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

mail.settings.server = 'smtp.gmail.com:587'
mail.settings.sender = 'Admin Courier Logistics'
mail.settings.login = 'admcourierlogistics@gmail.com:centauri'
auth.settings.login_next = URL('home')
auth.settings.profile_next = URL('home')
auth.settings.reset_password_next = URL('home')
auth.settings.hmac_key = None
auth.settings.actions_disabled = ['register','profile']


is_phone=IS_MATCH('^\d{10}$',error_message="10 digit mobile number Example: 9999123456")

db.define_table('auth_user',
                Field('first_name', length=512,requires=IS_NOT_EMPTY() ),
                Field('last_name', length=512,default=''),
                Field('email', length=512,default='',requires=(IS_EMAIL(),IS_NOT_IN_DB(db,'auth_user.email'))),
                Field('password', 'password', readable=False, label='Password', requires=[CRYPT(auth.settings.hmac_key)]),
                Field('gender',requires=IS_IN_SET(('male','female','other'))),
                Field('birth_date','date'),
                Field('phoneno',length=512,requires=is_phone),
                Field('levelno',length=1,requires=IS_IN_SET((1,2,3))),
                Field('place',length=512,requires=IS_NOT_EMPTY()),
                Field('registration_key', length=512,writable=False, readable=False,default=''),
                Field('registration_id', length=512,writable=False, readable=False,default=''),
                Field('reset_password_key', length=512,writable=False, readable=False, default='',
                      label=auth.messages.label_reset_password_key),
                format='%(first_name)s %(last_name)s',
                )

db.auth_user.birth_date.requires=IS_NOT_IN_DB(db((db.auth_user.first_name==request.vars.first_name)&
                                                 (db.auth_user.last_name==request.vars.last_name)),
                                              'auth_user.birth_date')


auth.define_tables()                           # creates all needed tables
auth.settings.mailer = mail                    # for user email verification
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.messages.verify_email = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['verify_email'])+'/%(key)s to verify your email'
auth.settings.reset_password_requires_verification = True
auth.messages.reset_password = 'Click on the link http://'+request.env.http_host+URL(r=request,c='default',f='user',args=['reset_password'])+'/%(key)s to reset your password'
## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
