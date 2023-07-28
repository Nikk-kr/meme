import bcrypt

'''
userDetai = {
    'id', 'name', 'contact', 'email', 'password'
}
'''
# users = [] # In memory usage
 
def userExists(userData,cursor):
    '''
        @brief:
    '''
    # Execute SQL Query
    sql_query = f'''
                    SELECT * FROM users;
                '''
    try:
        cursor.execute(sql_query)

        users = cursor.fetchall()
    except Exception as e:
        print("Error: ",e)

    print("Users: ")
    print(users)

    email = userData['email'] # collect user's email

    for user in users:
        if user[2] == email:
            # email found
            return {'response' : True, 'user' : user}

    # email not found    
    return {'response' : False, 'user' : {}}


def registerUser(userData,cursor):
    '''
        @brief:
        @param:
        @return:
    '''
    # check whether email id is registered or not !
    checkUser = userExists(userData,cursor)

    if(checkUser['response']):
        # user exist !
        # return response dictionary
        return {'statusCode' : 503, 'message' : 'alreadyregistered'}
    else:
        # store the data !
        # users.append(userData)  In memory execution

        sql_query = f'''
                        INSERT INTO users(name, email, password, contact) 
                        VALUES ('{userData['name']}', '{userData['email']}', '{userData['password']}', '{userData['contact']}');
                    '''
        
        try:
            # Execute SQL query
            cursor.execute(sql_query)

        except Exception as e:
            print("Error: ",e)

        # return response dictionary
        return {'statusCode' : 200, 'message' : 'registered'}


def loginUser(userData,cursor):
    
    checkUser = userExists(userData,cursor)

    print("user: ")
    print(checkUser)

    if(checkUser['response']):
        # user exist and check form password with stored password

           # userData['password'] == checkUser['user'][3]
        db_password = checkUser['user'][3]
        if bcrypt.checkpw(userData['password'].encode(), db_password.encode()):
            #return response dictionary
            return {'statusCode' : 200, 'message' : 'loggedin'}
        else:
            # if password doesn't match
            return {'statusCode' : 503, 'message' : 'passworderror'}
    else:
        # return response dictionary
        return {'statusCode' : 503, 'message' : 'alreadyregistered'}
