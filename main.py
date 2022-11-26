import pymysql
from app import app
from config import mysql
from flask import jsonify
from flask import flash, request
import json

@app.route('/create', methods=['POST'])
def create_emp(): 
    req = request.data
    _json =  json.loads(req)
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']
    _address = _json['address']	

    if _name and _email and _phone and _address and request.method == 'POST':
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO emp(name, email, phone, address) VALUES(%s, %s, %s, %s)"
        bindData = (_name, _email, _phone, _address)            
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        respone = jsonify('Employee added successfully!')
        print(respone)
        respone.status_code = 200

        cursor.close() 
        conn.close()
    
        return respone
    else:
        return showMessage()         
     
@app.route('/emp')
def emp():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id, name, email, phone, address FROM emp")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        print(respone)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close() 
        conn.close()  

@app.route('/emp/<int:emp_id>')
def emp_details(emp_id):
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT id, name, email, phone, address FROM emp WHERE id =%s", emp_id)
    empRow = cursor.fetchone()
    respone = jsonify(empRow)
    respone.status_code = 200
        
    cursor.close() 
    conn.close() 

    return respone
        
@app.route('/update', methods=['PUT'])
def update_emp():
    req = request.data
    _json =  json.loads(req)
    _id = _json['id']
    _name = _json['name']
    _email = _json['email']
    _phone = _json['phone']
    _address = _json['address']
    if _name and _email and _phone and _address and _id and request.method == 'PUT':			
        sqlQuery = "UPDATE emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
        bindData = (_name, _email, _phone, _address, _id,)
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        respone = jsonify('Employee updated successfully!')
        respone.status_code = 200

        print(cursor.rowcount, "record(s) affected")
        cursor.close() 
        conn.close() 
            
        return respone
    else:
        return showMessage()

@app.route('/delete/<int:emp_id>', methods=['DELETE'])
def delete_emp(emp_id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM emp WHERE id =%s", (emp_id,))
		conn.commit()
		respone = jsonify('Employee deleted successfully!')
		respone.status_code = 200
		return respone
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
        
       
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port= 5100,
        debug=True
    )