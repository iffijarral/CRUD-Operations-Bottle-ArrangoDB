from bottle import delete, get, post, put, request, response, static_file, template
import x
from icecream import ic
import uuid
import time
import bcrypt

##############################
@get("/favicon.ico")
def _():
    return static_file("favicon.ico", ".")

##############################
@get("/app.css")
def _():
    return static_file("app.css", ".")

##############################
@get("/mixhtml.js")
def _():
    return static_file("mixhtml.js", ".")

##############################
@get('/phone.svg')
def _():
    return static_file("phone.svg", ".")
##############################
@get("/phones/<key>")
def _(key):    
    try:
        res = x.db({"query":"""
                        FOR user IN users
                        FILTER user._key == @key
                        RETURN user""", 
                        "bindVars":{"key":key}})
        phones = res["result"]
        phones = phones[0]['phones']
        return f"""
            <template mix-target="#phones" mix-replace>                
                <div id="error" class="error_message"> {phones} </div>
            </template>
        """
    except Exception as ex:
        pass
    finally:
        pass

##############################
@get("/")
def _():
    name = request.get_cookie("name", secret="my_secret")
    if name:
        try:
            x.disable_cache()
            users = x.db({"query":"FOR user IN users RETURN user"})
            return template("index", users=users["result"])
        except Exception as ex:
            ic(ex)
            return ex
            # return "System is under maintaninance"
        finally:
            pass
    else:
        response.status = 303
        response.set_header("Location", "/login")
# ##############################
# @get("/")
# def _():
#     try:
#         x.disable_cache()
#         users = x.db({"query":"FOR user IN users RETURN user"})
#         return template("index", users=users["result"])
#     except Exception as ex:
#         ic(ex)
#         return "system under maintainance"         
#     finally:
#         pass
# ##############################
# Get login page
@get("/login")
def _():
    return template("login")

# ##############################
# Get login page
@get("/login/<page>")
def _(page):
    html = template("login")
    return f"""
        <template mix-target="#wrapper" mix-replace>                
            {html}
        </template>
    """

# ##############################
# Perform Login
@post("/login")
def _():
    try:
        # TODO: validate the email and password
        # validate password
        email = x.validate_user_email()
        password = x.validate_user_password()

        # TODO: Connect to the db and check that the email and password are correct
        db = x.db_sqlite()        
        
        # db.execute(SELECT * FROM users WHERE user_email = ? AND user_password = ?, (email, password))
        sql = db.execute("SELECT * FROM users WHERE user_email = ?", (email,))

        user = sql.fetchone()

        if user:
            user_password = user['user_password']

            password = password.encode('utf-8')

            if bcrypt.checkpw(password, user_password):                               
                response.set_cookie("name", user['user_name'], secret="my_secret", httponly=True)            
                return """
                    <template mix-redirect="/">
                    </template>            
                """
            else:
                return """
                    <template mix-target="#error" mix-replace>                
                        <div id="error" class="error_message"> Invalid credentials </div>
                    </template>
                """
        else:
            return """
                <template mix-target="#error" mix-replace>                
                    <div id="error" class="error_message"> Invalid credentials </div>
                </template>
            """
    except Exception as ex:
        print(ex)       

        if "user_password" in str(ex):
            return """
            <template mix-target="#error" mix-replace>                
                <div id="error" class="mix-error"> User password invalid</div>
            </template>            
            """
        if "user_email" in str(ex):
            return """
            <template mix-target="#error" mix-replace>
                <div id="error" class="error_message"> User Email Invalid</div>
            </template>
            """        
        return """
        <template mix-target="#error" mix-replace>
            <div id="error"> System under maintainance</div>
        </template>
        """
    finally:
        if "db" in locals(): db.close()

# ##############################
# Get signup page
@get("/signup")
def _():
    html = template("signup.html")
    return f"""
        <template mix-target="#login" mix-replace>            
            {html}           
        </template>
    """

# ##############################
# Perform signup
@post("/signup")
def _():
    try:
        # TODO: validate the email and password
        # validate email and password
        user_name = x.validate_user_name()             
        user_email = x.validate_user_email()
        user_password = x.validate_user_password()
        
        confirm_password = request.forms.get("confirm_password")

        if user_password != confirm_password:
            return f"""
                <template mix-target="#error" mix-replace>                
                    <div id="error"> Passwords do not match. Please try again. </div>
                </template> 
            """
        
        db = x.db_sqlite()

        user_id = uuid.uuid4().hex        

        user_updated_at = 0

        user_created_at = int(time.time())

        # user_password = b'password' # b infront of 'password' is important
        user_password = x.validate_user_password()

        user_password = user_password.encode('utf-8')

        salt = bcrypt.gensalt()

        hashed_password = bcrypt.hashpw(user_password, salt)

        sql = db.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", (user_id, user_name, user_email, hashed_password, user_created_at,  user_updated_at))        

        db.commit()

        return """            
            <template mix-target="#message" mix-replace>
                <div id="message"> Record inserted </div>
            </template>            
        """
    except Exception as ex:
        error_message = ''
        ic(ex)
        if "user_name" in ex.args[1]:
            error_message += f"<p>User Name is required and must have ({x.USER_NAME_MIN}, {x.USER_NAME_MAX}) characters</p>"
        if "user_last_name" in ex.args[1]:
            error_message += f"<p>User Last Name is required and must have ({x.USER_LAST_NAME_MIN}, {x.USER_LAST_NAME_MAX}) characters</p>"
        if "user_password" in ex.args[1]:
            error_message += "<p> User password invalid </p>"
        if "user_email" in ex.args[1]:
            error_message += "<p> User Email is required and much be a valid email </p>"        
        
        if error_message == '':
            return """
            <template mix-target="#error" mix-replace>
                <div id="error"> System under maintainance </div>
            </template>
            """
        else:
            return f"""
            <template mix-target="#error" mix-replace>
                <div id="error"> {error_message} </div>
            </template>
            """
    finally:
        if "db" in locals(): db.close()

# ##############################
@post("/users")
def _():
    name = request.get_cookie("name", secret="my_secret")
    if name:
        try:
            x.disable_cache()
            user_name = x.validate_user_name()
            user_last_name = x.validate_user_last_name()
            user_username = x.validate_user_username()
            user_gender = x.validate_user_gender()
            ic(user_last_name)
            user = {"name":user_name, "last_name":user_last_name, "username":user_username, "gender":user_gender}
            res = x.db({"query":"INSERT @doc IN users RETURN NEW", "bindVars":{"doc":user}})
            html = template("_user.html", user=res["result"][0])
            form_create_user =  template("_form_create_user.html")
            return f"""
            <template mix-target="#users" mix-top>
                {html}
            </template>
            <template mix-target="#frm_user" mix-replace>
                {form_create_user}
            </template>
            """
        except Exception as ex:
            ic(ex)
            if "user_name" in str(ex):
                return f"""
                <template mix-target="#message">
                    {ex.args[1]}
                </template>
                """            
        finally:
            pass
    else:
        return """
            <template mix-target="#message">
                Access denied
            </template>
        """


##############################
@delete("/users/<key>")
def _(key):
    name = request.get_cookie("name", secret="my_secret")
    if name:
        try:
            ic(key)
            res = x.db({"query":"""
                        FOR user IN users
                        FILTER user._key == @key
                        REMOVE user IN users RETURN OLD""", 
                        "bindVars":{"key":key}})
            print(res)
            return f"""
            <template mix-target="[id='{key}']" mix-replace>
                <div class="mix-fade-out user_deleted mix-error" mix-ttl="2000">User deleted</div>
            </template>
            """
        except Exception as ex:
            ic(ex)
        finally:
            pass
    else:
        return """
            <template mix-target="#message">
                Access denied
            </template>
        """


##############################
@put("/users/<key>")
def _(key):
    name = request.get_cookie("name", secret="my_secret")
    if name:
        try:
            x.disable_cache()
            name = x.validate_user_name()
            last_name = x.validate_user_last_name()
            username = x.validate_user_username()
            gender = x.validate_user_gender()
            
            x.validate_key(key)
            
            res = x.db({"query":"""
                            UPDATE { _key: @key, name: @name, last_name:@last_name, username:@username, gender:@gender } 
                            IN users 
                            RETURN NEW""",
                        "bindVars":{
                            "key": f"{key}",
                            "name":f"{name}",
                            "last_name":f"{last_name}",
                            "username":f"{username}",
                            "gender":f"{gender}"
                        }})
            return f"""
            <template>            
            </template>
            """
        except Exception as ex:
            ic(ex)
            if "user_name" in str(ex):
                return f"""
                <template mix-target="#message">
                    {ex.args[1]}
                </template>
                """            
        finally:
            pass
    else:
        return """
            <template mix-target="#message">
                Access denied
            </template>
        """ 


#########################
@get("/logout")
def _():  
  response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
  response.add_header("Pragma", "no-cache")
  response.add_header("Expires", 0)    
  response.delete_cookie("name")
  response.status = 303
  response.set_header("Location", "/login")
  return   












