# -*- coding: utf-8 -*-
from zope.app.component.hooks import getSite

from vindula.myvindula.user import ModelsFuncDetails

def to_utf8(value):
    return unicode(value, 'utf-8') 


def userupdate(event):
    """ Handler for User Login in Site """
    membership = getSite().portal_membership
    user_login = membership.getAuthenticatedMember()
    user_id = to_utf8(user_login.getId())
    
    if not ModelsFuncDetails().get_FuncDetails(user_id):
        D = {}
        D['username'] = user_id
        D['name'] = to_utf8(user_login.getProperty('fullname'))
        D['email'] = to_utf8(user_login.getProperty('email'))
        ModelsFuncDetails().set_FuncDetails(**D)