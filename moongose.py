import requests

class Mongoose(object):
    def __init__(self,host,port):
        self.baseclient = _Baseclient(host,port)
    def register(self,username,password):
        method = "POST"
        resource_path = "/signup"
        data = {
            "username":username,
            "password":password
        }
        response = self.baseclient.request(method,resource_path,json=data)


        print (response)


class _Baseclient(object):
    def __init__(self, host,port):
        self.host = "http://{}:{}/api".format(host,port)
    def request(self,method,resource_path,**kwargs):
        path = self.host + resource_path

        response = requests.request(method,path,**kwargs)
        
        if 200 < response.status_code < 210:
            return response.json()
        elif 400 <= response.status_code < 410:
            raise ValueError(response.json()["message"])
        else:
            response.raise_for_status()
    