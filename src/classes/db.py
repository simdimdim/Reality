import os
import plyvel

datadir=str(os.path.abspath(str(__file__.split('src')[0])+'data/db')+'/')

dht='dht'
ip='ipv4'
class db():
    def __init__(self,name,paranoid_checks=True, write_buffer_size=None,
                 lru_cache_size=None,block_size=None,
                 compression='snappy'):
        self.dbname=str(name)
        self.location=bytes(datadir+self.dbname,'ascii')
        setattr(self,self.dbname,
                plyvel.DB(self.location,create_if_missing=True))
   
    def iterate(self,db,startkey,stopkey,include_start=True,include_stop=True,
                include_key=True,include_value=True,reverse=False):
        return getattr(self,self.db).iterator(starkey,include_start,stopkey,include_stop,
                           include_key=True,include_value=True,reverse=False)
    
    def seek(self,iterate,*args,**kwargs):
        key=kwarg.get('key', None)
        db=kwarg.get('db', self.dbname)
        iterator=iterate(*args)
        if key is not None:
            return getattr(self,db).iterator.seek(key)
        else:
            return getattr(self,db).iterator.seek_to_start()
        
    def batchwrite(self,*key_value_pairs,**prefix):
        prefix = prefix.get('prefix', self.dbname)
        print(*key_value_pairs)
        with getattr(self,prefix).write_batch() as dbwb:
            for key in range(1,501):
                print(key)
                dbwb.put(bytes(key,'ascii'),bytes(key,'ascii')*20)
            #raise ValueError("Something went wrong!")
        getattr(self,self.dbname).close()
        #self.destroy()
    #Creates prefixed database
    def prefix(self,prefix):
        setattr(self,str(prefix),str(prefix))
        print(str(self.prefix),getattr(self,prefix))
        setattr(self,str(prefix),
                getattr(self,self.dbname).prefixed_db(bytes(prefix,'ascii')))
        #check
        #print(getattr(self,prefix).get(bytes(1,'ascii')))
        print(self.prefix,getattr(self,prefix))

    #Destroy the whole thing        
    def destroy(self,other=None):
        if other is None:
            plyvel.destroy_db(self.location)
        else:
            plyvel.destroy_db(other)
    #Close db
    def close(self,db=None):
        if db is None:
            db=self.dbname
        getattr(self,str(db)).close()
        
dht=db(dht,block_size=1024)
dht.prefix(ip)
#dht.batchwrite(b'1545',b'555468',prefix=ip)
for k,v in dht.iterate(1,600):
    print(k,v)
help(dht)
dht.close()
dht.destroy()
