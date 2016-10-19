#!/usr/bin/env python
import datetime
import mysql.connector

class DataBaseInfo:
    def __init__(self, ip, port, user, password, database):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.database = database

class FetchData:
    def __init__(self, db_info):
        self.ip = db_info.ip
        self.port = db_info.port
        self.user = db_info.user
        self.password = db_info.password
        self.database = db_info.database

    def fetch_data(self, pattern):
        cnx = mysql.connector.connect(host=self.ip,
                                      port=self.port,
                                      user=self.user,
                                      password=self.password,
                                      database=self.database)
        cursor = cnx.cursor()

        cursor.execute(pattern)

        data = cursor.fetchall()

        cursor.close()
        cnx.close()

        return data

    def fetch_table_header(self, table_name):
        pattern = "SHOW COLUMNS FROM " + table_name
        return self.fetch_data(pattern)


    def pretty_show(self, table_header, data):
        header = []
        for k, v in enumerate(table_header):
            header.append({'value':v[0], 'length':len(v[0])})

        for k, v in enumerate(data):
            for k_s, v_s in enumerate(v):
                if header[k_s]['length'] < len(str(v_s)):
                    header[k_s]['length'] = len(str(v_s))

        for v in header:
            cstr = '{:<%d} '%v['length']
            print(cstr.format(v['value'])),
        print

        print('*'*120)
        for k, v in enumerate(data):
            for k_s, v_s in enumerate(v):
                cstr = '{:<%d} '%header[k_s]['length']
                print(cstr.format(v_s)),
            print

class FetchSpeedData(FetchData):
    def __init__(self, db_info):
        FetchData.__init__(self, db_info)
        self.transfer_node = []
        self.all_node_room = []
        self.all_node_name = {}

    def get_transfer_node(self, tn):
        if not self.transfer_node:
            pattern = 'SELECT host FROM %s GROUP BY host'%(tn)
            data = self.fetch_data(pattern)
            for item in data:
                self.transfer_node.append(item[0])

        return self.transfer_node


    def get_all_node_room(self, table_name):
        if not self.all_node_room:
            pattern = 'SELECT node_room  FROM %s GROUP BY node_room'%(table_name)
            data = self.fetch_data(pattern)
            for item in data:
                self.all_node_room.append(item[0])

        return self.all_node_room

    def get_all_node_name(self, table_name):
        if not self.all_node_name:
            if not self.all_node_room:
                self.get_all_node_room(table_name)

            for item in self.all_node_room:
                self.get_node_name(table_name, item)

        if len(self.all_node_room) == len(self.all_node_name):
            return self.all_node_name

        for item in self.all_node_room:
            if iten not in self.all_node_name:
                self.get_node_name(table_name, item)

        return self.all_node_name

    def get_node_name(self, table_name, node_room):
        if node_room not in self.all_node_name:
            self.all_node_name[node_room] = []
            pattern = 'SELECT node_name FROM %s WHERE node_room="%s" GROUP BY node_name'%(table_name, node_room)
            data = self.fetch_data(pattern)
            for  item in data:
                self.all_node_name[node_room].append(item[0])

        return self.all_node_name[node_room]

    def get_node_room_data(self, table_name, node_room):
        pattern = 'SELECT * FROM %s WHERE node_room="%s"'%(table_name, node_room)

        return self.fetch_data(pattern)

    def get_node_name_data(self, table_name, node_name):
        pattern = 'SELECT * FROM %s WHERE node_name="%s"'%(table_name, node_name)

        return self.fetch_data(pattern)

    def get_nn_ST(self, tn, nn, transfer_node):
        pattern = 'SELECT speed, timestamp  FROM %s WHERE node_name="%s" and host="%s"'%(tn, nn, transfer_node)

        return self.fetch_data(pattern)

    #def get_node_room_ttfb():
    #def get_node_room_speed():

def main():
    db_info = DataBaseInfo('10.0.6.27', '3306', 'root', '123', 'DYN_PARENTS')
    host = '10.0.6.27'
    port = '3306'
    user = 'root'
    passwd = '123'
    db = 'DYN_PARENTS'

#    fd = FetchData(host, port, user, passwd, db)
#    header = fd.fetch_table_header('dyn')
#    data = fd.fetch_data('select * from dyn')
#    fd.pretty_show(header, data)
#    print('-'*120)

    #fd = FetchSpeedData(host, port, user, passwd, db)
    fd = FetchSpeedData(db_info)

    print('get tranfer node')
    tn = fd.get_transfer_node('tmp')
    print(tn)
    print

    print('get_all_node_room')
    nr = fd.get_all_node_room('tmp')
    print(nr)
    print

    print('get_all_node_name')
    nn = fd.get_all_node_name('tmp')
    for k, v in nn.items():
        print(k, v)
    print

    print('get_node_name')
    nn = fd.get_node_name('tmp', 'CUN-CQ-CKG')
    print(nn)
    print

    print('get_node_room_data')
    data = fd.get_node_room_data('tmp', 'CUN-CQ-CKG')
    print(data)
    print

    print('get_node_name_data')
    data = fd.get_node_name_data('tmp', 'CUN-CQ-CKG-005')
    print(data)
    print

if __name__ == "__main__":
    main()
