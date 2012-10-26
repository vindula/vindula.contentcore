# -*- coding: utf-8 -*-

from storm.locals import *
from storm.locals import Store

from vindula.contentcore.base import BaseStore


class ModelsLog(Storm, BaseStore):
    __storm_table__ = 'vin_contentcore_log'

    id = Int(primary=True)
    valor_old = Unicode()
    valor_new = Unicode()
    date_creation = DateTime()
    instance_id = Int()
    forms_id = Int() 
    fields = Unicode()
    
    
    
    def set_log(self,**kwargs):
        # adicionando...
        log = ModelsLog(**kwargs)
        self.store.add(log)
        self.store.flush()
    

