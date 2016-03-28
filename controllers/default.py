# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

#@auth.requires_membership('admin')

def display_users():
    list = db(db.auth_user).select()
    return locals()

def show_user():
    user_id = request.args(0,cast=int)
    #print user_id
    user_detail = db(db.auth_user.id==user_id).select()
    tp=db.executesql("SELECT group_id FROM auth_membership WHERE user_id='%d'" % (int(user_id)))
    #print tp[0][0]
    return locals()

def home_admin():
    form1=SQLFORM(db.sets_table).process()
    form2=SQLFORM(db.set_question).process()
    form3=SQLFORM(db.specificQuestion_course).process()
    return locals()

def feedback():
    list = db(db.set_question).select()
    form = SQLFORM(list[0])
    for i in list[1:]:
        temp2 = SQLFORM(i)
        form.append(temp2)
    return locals()

def make_faculty():
    user_id = request.args(0,cast=int)
    #user = db.auth_user[user_id]
    # db.executesql("UPDATE auth_membership SET group_id='%d' WHERE id='%d'" % (1,int(user_id)))
    #id = db.auth_membership.insert(group_id=1,user_id=user_id)
    auth.add_membership(8,user_id)
    auth.del_membership(9,user_id)
    redirect(URL('show_user',args=user_id))


@auth.requires_login()
def test2():
    list = db(db.set_question).select()
    formList = []
    for que in list:
        form = FORM(que.question,BR(),
                    INPUT(_type="radio", _name=que.id, _id=str(que.id)+"A", _value="A"),que.option_A,BR(),
                    INPUT(_type="radio", _name=que.id, _id=str(que.id)+"B", _value="B"),que.option_B,BR(),
                    INPUT(_type="radio", _name=que.id, _id=str(que.id)+"C", _value="C"),que.option_C,BR(),
                    INPUT(_type="radio", _name=que.id, _id=str(que.id)+"D", _value="D"),que.option_D,BR(),
                    INPUT(_type="radio", _name=que.id, _id=str(que.id)+"E", _value="E"),que.option_E,BR()
                   )
        formList.append(form)
    return dict(formList=formList, list=list)

def storeAns():
    db.answers_table.insert(course_id=1, student_id=auth.user.id, question_id=request.vars.id, answer=request.vars.id2)
    return "bla"

@auth.requires_login()
def index():
    if(auth.has_membership('admin')):
        print ">>>>"
        redirect(URL('default','home_admin'))
    elif(auth.has_membership('faculty')):
        redirect(URL('default','home_faculty'))
    else:
        redirect(URL('default','home_student'))
    return locals()

def __add_user_membership(form):
         #group_id = auth.id_group(role=form.vars.user_type)
         #user_id = form.vars.id
         auth.add_membership(9,auth.user_id)

def user():
    auth.settings.register_onaccept = __add_user_membership
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


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
