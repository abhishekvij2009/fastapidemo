from fastapi import FastAPI ,Request, Response
import config as rds
import pymysql
import uvicorn
import config
from pydantic import BaseModel
from typing import Optional
import json

app = FastAPI()

Department  = {"Mechanical":"Cloud","IT":"Informatica","EC":"Pipeline","Chemical":"Road"}
conn = pymysql.connect(
        host= rds.host, 
        port =  rds.port,
        user = rds.user, 
        password = rds.password,
        db = rds.db,
        ) 
      
class Employee(BaseModel):
    Emp_ID: int
    Emp_Name: str
    Emp_Qualification: str

#add comment
@app.api_route("/employee-details/{id}", methods=["GET"])
def get_employee_details (id:int):
        cursor=conn.cursor()
        getemploy= "select * from employee3 where id = "+ str(id)
        cursor.execute(getemploy)
        results = cursor.fetchone()
        return results

@app.api_route("/post-details/{postid}", methods=["POST"])        
def post(postid: int , employee : Employee):
        newlist = []
        cursor=conn.cursor()
        getemploy2= "select id from employee3"
        cursor.execute(getemploy2)
        result = cursor.fetchall()
        for list in result:
                newlist.extend(list)
        if postid in newlist:
                return "yes it exist"
        cursor=conn.cursor()       
        sql = "INSERT INTO employee3 (id, EMP_ID,Emp_Name,Emp_Qualification,dep) VALUES (%s, %s,%s, %s,%s)"
        val = (postid, employee.Emp_ID, employee.Emp_Name,employee.Emp_Qualification,Department[employee.Emp_Qualification])
        cursor.execute(sql, val)
        conn.commit
        return "200"
        
                        

                
