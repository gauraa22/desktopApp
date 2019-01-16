import sqlite3
from sqlite3 import Error

class Array:
    def __init__(self,name,mgmt,spa,spb):
        self.name = name
        self.spa = spa
        self.spb = spb
        self.mgmt = mgmt


    def insert_arrays_info(self):
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            c.execute("INSERT INTO arrays VALUES (?,?,?,?)",(self.name,self.mgmt,self.spa,self.spb))
            conn.commit()
        except Error as e:
            print(e)
        finally:
            conn.close()

    @staticmethod
    def get_arrayname(*data):
        val = "No data available"
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            array_name = c.execute(f"SELECT name FROM arrays WHERE {data[0]}=?",(data[1],))
            val = " ".join(a for a in array_name.fetchone()) 
        except Error as e:
            print(e)
        finally:
            conn.close()
            return val.strip()


    @staticmethod
    def data_exists(*data):
        val = False
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            output =  c.execute(f"SELECT * FROM arrays WHERE {data[0]}=?",(data[1],))
            if len(output.fetchall())>0:
                val = True
        except Error as e:
            print(e)
        finally:
            conn.close()
            return val

    @staticmethod
    def get_all_data():
        val = "No data available"
        try:
            conn = sqlite3.connect('arrayTest.db')
            c = conn.cursor()
            arrays_info = c.execute(f"SELECT * FROM arrays")
            for i in arrays_info.fetchall():
                print(i)

        except Error as e:
            print(e)
        finally:
            conn.close()
            return val.strip()


# test = Array("JF-D1681","10.109.196.41","10.109.196.42","10.109.196.43")
# test.insert_arrays_info()

Array.get_all_data()
    

