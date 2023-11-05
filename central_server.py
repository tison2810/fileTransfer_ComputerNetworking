import socket
from Base import Base
from persistence import *


class CentralServer(Base):
    def __init__(self, serverhost='localhost', serverport=40000):
        super(CentralServer, self).__init__(serverhost, serverport)

        # get registered user list
        self.peerList = get_all_users()

        # manage online user list
        self.onlineList = {} 

        # manage online user list have file which have been searched
        self.shareList = {}

        # define handlers for received message of central server
        handlers = {
            'PEER_REGISTER': self.peer_register,
            'PEER_LOGIN': self.peer_login,
            'PEER_SEARCH': self.peer_search,
            'PEER_LOGOUT': self.peer_logout,
            'FILE_REPO': self.peer_upload,
            'DELETE_FILE': self.delete_file,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)

    ## ==========implement protocol for user registration - central server==========##
    def peer_register(self, msgdata):
        # received register info (msgdata): peername, host, port, password (hashed)
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        
        # register error if peer name has been existed in central server
        # otherwise add peer to managed user list of central server
        if peer_name in self.peerList:
            self.client_send((peer_host, peer_port),
                             msgtype='REGISTER_ERROR', msgdata={})
            print(peer_name, " has been existed in central server!")
        else:
            # add peer to managed user list
            self.peerList.append(peer_name)
            # save to database
            add_new_user(peer_name, peer_password)
            self.client_send((peer_host, peer_port),
                             msgtype='REGISTER_SUCCESS', msgdata={})
            print(peer_name, " has been added to central server's managed user list!")
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - central server==========##
    def peer_login(self, msgdata):
        # received login info (msgdata): peername, host, port, password (hashed)
        peer_name = msgdata['peername'] 
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        # login error if peer has not registered yet or password not match
        # otherwise add peer to online user list
        if peer_name in self.peerList:
            # retrieve password
            peer_password_retrieved = get_user_password(peer_name)
            if str(peer_password) == peer_password_retrieved:
                
                # add peer to online user list
                self.onlineList[peer_name] = tuple((peer_host, peer_port))
                self.client_send((peer_host, peer_port),
                                 msgtype='LOGIN_SUCCESS', msgdata={})

                # update ipaddress and port using by this peer
                update_user_address_port(peer_name, peer_host, peer_port)
                
                # noti
                print(peer_name, " has been added to central server's online user list!")

            else:
                self.client_send((peer_host, peer_port),
                                 msgtype='LOGIN_ERROR', msgdata={})
                print("Password uncorrect!")
        else:
            self.client_send((peer_host, peer_port),
                             msgtype='LOGIN_ERROR', msgdata={})
            print(peer_name, " has not been existed in central server!")
    ## ===========================================================##

    ## =========implement protocol for finding user list who have file searched==============##
    def peer_search(self, msgdata):
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        file_name = msgdata['filename']
        user_list = search_file_name(file_name)

        for peername in user_list:
            if peer in self.onlineList:
                peer_info = self.onlineList[peername]
                self.shareList[peername] = {'hostname': peer_info['ip'], 'port': peer_info['port']}

        data = {'online_user_list_have_file': self.shareList}

        self.client_send((peer_host, peer_port),
                         msgtype='LIST_USER_SHARE_FILE', msgdata=data)
        print(peer_name, " has been sent latest online user list!")
        self.shareList.clear()

    ## ================implement protocol for log out & exit=============##
    def peer_logout(self, msgdata):
        peer_name = msgdata['peername']
        # delete peer out of online user list 
        if peer_name in self.onlinelist:
            del self.onlinelist[peer_name]
            # noti
            print(peer_name, " has been removed from central server's online user list!")
    ## ===========================================================##

    ## ================implement protocol for peer upload file=============##
    def peer_upload(self, msgdata):
        peer_name = msgdata['peername']
        file_name = msgdata['filename']
        add_new_file(peer_name, file_name)
    ## ===========================================================##


    ##=================implement protocol for peer delete file=============##
    def delete_file(self, msgdata):
        peer_name = msgdata['peername']
        file_name = msgdata['filename']
        delete_file(peer_name, file_name)
if __name__ == '__main__':
    server = CentralServer()
    server.input_recv()
