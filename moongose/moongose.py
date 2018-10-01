import requests
import simplejson
import random
import json

class Mongoose(object):
    """
        Welcome to Mongoose
        This Class is inted to help you to Interact with Basilisk
        It has all the methods to comunicate with it.
    """

    def __init__(self,host,port):
        """
        param:
            host: IP or fqdn of bassilisk Server
            port: port of basilisk Server
        """
        self.baseclient = _Baseclient(host,port)
    
    def register(self,username,password):
        """
        Register a new Account to talk to Basilisk
        params:
            Username: Username Account
            Password: Password Account
        """
        method = "POST"
        resource_path = "/signup"
        data = {
            "username":username,
            "password":password
        }
        response = self.baseclient.request(method,resource_path,json=data)

        self.baseclient.token = "Bearer " + response["data"]["token"]

    def login(self,username,password):
        """
        Login with a Exisiting Account to interact o Basilisk Server
        params:
            Username: Userrname Account
            Password: Password Account
        """
        method = "POST"
        resource_path = "/login"
        data = {
            "username":username,
            "password":password
        }
        response = self.baseclient.request(method,resource_path,json=data)

        self.baseclient.token = "Bearer " + response["data"]["token"]

    def create_question(self,question):
        """
        Create a new Question,
        params:
            question: The new Question
        returns object created.
        Admin only
        """
        method = "POST"
        resource_path = "/question"
        data = {
            "question":question,
        }
        response = self.baseclient.request(method,resource_path,json=data)
        return(response["data"])

    def question(self,id):
        """
        Ask for a challenge to Basilisk
        params:
            id: number identifier of a question
        returns string with the Question statement
        """
        method = "GET"
        id=int(id)
        resource_path = "/question/{id}".format(id=id)
        response = self.baseclient.request(method,resource_path)
        return response["question"]

    def get_parameters(self,question_id):
        """
        Get paramaters of a Question
        params:
            question_id: identifier of a Question
        returns paramaters required to resolve the challenge
            it can be a number a string or a list
        """
        method = "GET"
        question_id=int(question_id)
        resource_path = "/question/{id}/parameter".format(id=question_id)
        response = self.baseclient.request(method,resource_path)
        parameter = random.choice(response)
        self.assessment = parameter["id"]
        try:
            return int(parameter["parameters"])
        except:
            pass
        try:
            return json.loads(parameter["parameters"])
        except:
            return parameter["parameters"]
    
    def create_assessment(self,question_id,parameters,answer):
        method = "POST"
        question_id=int(question_id)
        resource_path = "/question/{id}/parameter".format(id=question_id)
        data = {
            "question_id":question_id,
            "parameters":parameters,
            "answer":answer,
        }
        response = self.baseclient.request(method,resource_path,json=data)
        return response
    def verify(self,question_id,answer):
        method = "POST"
        question_id=int(question_id)
        resource_path = "/completed"
        data = {
            "question_id":question_id,
            "assesment_id":self.assessment,
            "answer":answer,
        }
        response = self.baseclient.request(method,resource_path,json=data)
        return response["message"]

    def check_completed(self):
        method = "GET"
        resource_path = "/completed"
        response = self.baseclient.request(method,resource_path)
        completed = [i["question_id"] for i in response]
        completed.sort()
        print("Completed:", completed)

       
class _Baseclient(object):
    def __init__(self, host,port):
        self.host = "http://{}:{}/api".format(host,port)
        self.token = None

    def request(self,method,resource_path,**kwargs):
        path = self.host + resource_path
        if self.token:
            kwargs["headers"]={"Authorization":self.token}

        response = requests.request(method,path,**kwargs)
        
        if 200 <= response.status_code < 210:
            return response.json()
        elif 400 <= response.status_code < 410:
            try:
                error = response.json()
            except simplejson.errors.JSONDecodeError : 
                raise ValueError(response.text)
            if "message" in error:
                raise ValueError(response.json()["message"])
            elif "msg" in error:
                raise ValueError(response.json()["msg"])
            else:
                response.raise_for_status()
        else:
            response.raise_for_status()

    