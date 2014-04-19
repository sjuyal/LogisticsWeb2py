# coding: utf8
db.define_table('hierarchy_table',
                Field('level1', length=512,requires=IS_NOT_EMPTY()),
                Field('level2', length=512,requires=IS_NOT_EMPTY()),
                Field('level3', length=512,requires=IS_NOT_EMPTY())
                )

db.define_table('history_table',
                Field('city',length=512),
                Field('levelno',length=512),
                Field('productid','integer')
                )

db.define_table('product_info',
                Field('product_id','integer'),
                Field('product_name',length=512,requires=IS_NOT_EMPTY()),
                Field('company_name',length=512),
                Field('receiver_name',length=512,requires=IS_NOT_EMPTY()),
                Field('receiver_email', length=512,default='',requires=(IS_EMAIL())),
                Field('expected_arrival_date','date',default=request.now),
                Field('next_checkpoint',length=512),
                Field('next_checkpoint_level',length=512),
                Field('address',length=512),
                Field('current_pos',length=512),
                Field('current_pos_level',length=512),
                Field('source_place',length=512),
                Field('destination_place',length=512,requires=IS_IN_DB(db,db.hierarchy_table.level3,'%(level3)s')),
                Field('product_status','integer'),
                format='%(name)s')
