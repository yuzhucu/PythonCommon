# -*- coding:utf-8 -*-
############################################################################
# 程序：通用程序处理
# 功能：抽取常用功能封装为函数
# 创建时间：2016/11/26
# 更新时间：2016/11/26
# 使用库：requests、BeautifulSoup4、MySQLdb
# 作者：yuzhucu
#############################################################################

import time
import MySQLdb

class MySQL:
    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

    #数据库初始化
    def _init_(self,ip,username,pwd,schema):
        try:
            self.db = MySQLdb.connect(ip,username,pwd,schema)
            print self.getCurrentTime(),u"MySQL DB Connect Success"
            self.cur = self.db.cursor()
        except MySQLdb.Error,e:
             print self.getCurrentTime(),u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1])

    #插入数据
    def insertData(self, table, my_dict):
         try:
             self.db.set_character_set('utf8')
             cols = ', '.join(my_dict.keys())
             values = '"," '.join(my_dict.values())
             sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, '"'+values+'"')
             try:
                 result = self.cur.execute(sql)
                 insert_id = self.db.insert_id()
                 self.db.commit()
                 #判断是否执行成功
                 if result:
                     return insert_id
                 else:
                     return 0
             except MySQLdb.Error,e:
                 #发生错误时回滚
                 self.db.rollback()
                 #主键唯一，无法插入
                 if "key 'PRIMARY'" in e.args[1]:
                     print self.getCurrentTime(),u"Primary Key Constraint，No Data Insert:",e.args[0], e.args[1]
                     #return 0
                 #elif "MySQL server has gone away" in e.args :
                 #    _init_()
                 else:
                     print self.getCurrentTime(),u"Data Insert Failed: %d: %s" % (e.args[0], e.args[1])
         except MySQLdb.Error,e:
             print self.getCurrentTime(),u"MySQLdb Error:%d: %s" % (e.args[0], e.args[1])

if __name__=="__main__":
   mySQL=MySQL()
   mySQL._init_('localhost','root','root','fang')


