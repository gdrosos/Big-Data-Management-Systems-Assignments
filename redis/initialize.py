import app
import logging


def init_sqlite_db():
    conn = app.get_db_connection()
    cursor_obj = conn.cursor()
 
    # USERS table
    cursor_obj.execute("DROP TABLE IF EXISTS USERS")
    user_table = """ 
                CREATE TABLE USERS (
                    userID INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(127) NOT NULL,
                    age INTEGER,
                    gender CHAR(1),
                    email VARCHAR(255)
                ); 
                """
    cursor_obj.execute(user_table)
    user_insert = """
    INSERT INTO USERS (userID, name, age, gender, email)
    VALUES
        ("1","Scott Compton",84,"M","pede.suspendisse@hotmail.ca"),
        ("2","Kasper Dixon",18,"M","mollis.lectus@hotmail.edu"),
        ("3","Iliana Hancock",75,"M","mi.pede@aol.couk"),
        ("4","Sade Guzman",40,"M","mi.ac.mattis@outlook.net"),
        ("5","Avram Anderson",44,"F","amet.consectetuer.adipiscing@google.org"),
        (6,"Carol Medina",83,"M","magna.malesuada.vel@hotmail.couk"),
        (7,"Yuli Dillon",54,"F","tempor.est.ac@yahoo.edu"),
        (8,"Alyssa Quinn",38,"M","tempus.risus@aol.ca"),
        (9,"Lars Hatfield",81,"F","elit.fermentum.risus@google.com"),
        (10,"Zorita Mason",18,"M","ultrices.vivamus@hotmail.com"),
        (11,"Kennedy Cross",73,"F","ante.dictum@aol.edu"),
        (12,"Ella Barr",52,"F","ut@outlook.edu"),
        (13,"Nora Henderson",85,"F","aenean.eget@icloud.org"),
        (14,"Maggie Church",33,"M","dolor.sit@google.net"),
        (15,"Christian Hart",28,"F","consectetuer.adipiscing@icloud.couk"),
        (16,"Coby Hall",25,"F","tempus@google.couk"),
        (17,"Ahmed Chandler",44,"F","aenean.eget@icloud.com"),
        (18,"Hector Dixon",50,"M","vel.pede@outlook.org"),
        (19,"Ima Johnston",83,"M","tristique.pharetra.quisque@icloud.couk"),
        (20,"Hop Chase",76,"F","id.mollis.nec@hotmail.net");"""
    cursor_obj.execute(user_insert)

    # MEETINGS table
    cursor_obj.execute("DROP TABLE IF EXISTS MEETINGS")
    # Creating table users
    meeting_table = """ 
                CREATE TABLE MEETINGS (
                    meetingID INTEGER PRIMARY KEY AUTOINCREMENT,
                    title VARCHAR(127) NOT NULL,
                    description VARCHAR(255),
                    isPublic BOOLEAN
                ); 
                """
    cursor_obj.execute(meeting_table)
    meeting_insert = """
    INSERT INTO MEETINGS (meetingID,title,description,isPublic)
    VALUES
        (10,"ullamcorper","velit justo nec ante. Maecenas","0"),
        (11,"fringilla","sapien imperdiet ornare.","0"),
        (12,"ipsum","Praesent eu nulla at sem molestie sodales. Mauris","0"),
        (13,"auctor,","vulputate dui", "0"),
        (14,"libero","semper et, lacinia vitae", "0"),
        (15,"arcu.","Vivamus nisi. Mauris nulla. Integer urna.","0"),
        (16,"ligula.","montes, nascetur", "0"),
        (17,"egestas","Curae Phasellus ornare. Fusce mollis. Duis sit","0"),
        (18,"natoque","pede. Praesent eu","0"),
        (19,"mauris","dolor. Donec fringilla. Donec feugiat metus sit amet","0"),
        (20,"Curabitur","et pede.","0"),
        (21,"adipiscing","et pede. Nunc sed orci lobortis augue scelerisque mollis.","1"),
        (22,"sit","Aliquam ornare, libero at auctor ullamcorper", "1"),
        (23,"tempor","amet metus. Aliquam erat volutpat. Nulla facilisis. Suspendisse commodo","1"),
        (24,"sodales","a neque. Nullam ut nisi a odio","1"),
        (25,"vestibulum,","pellentesque","1"),
        (26,"eget","nisl sem, consequat nec","1"),
        (27,"Proin","Nulla facilisi. Sed neque. Sed eget","1"),
        (28,"tortor","neque. Sed eget lacus. Mauris non","1"),
        (29,"neque.","senectus et netus et malesuada","1");
    """
    cursor_obj.execute(meeting_insert)


    # AUDIENCE table
    cursor_obj.execute("DROP TABLE IF EXISTS AUDIENCE")
    audience = """ 
                CREATE TABLE AUDIENCE (
                    meetingID INTEGER NOT NULL,
                    userEmail VARCHAR(128) NOT NULL,
                    PRIMARY KEY(meetingID, userEmail)
                    FOREIGN KEY(meetingID) REFERENCES MEETINGS(meetingID)
                    FOREIGN KEY(userEmail) REFERENCES USERS(email)
                ); 
                """

    cursor_obj.execute(audience)
    audience_insert = '''
    INSERT INTO AUDIENCE (meetingID,userEmail)
    VALUES
        (13,"pede.suspendisse@hotmail.ca"),
        (17,"pede.suspendisse@hotmail.ca"),
        (12,"pede.suspendisse@hotmail.ca"),
        (15,"dolor.sit@google.net"),
        (17,"dolor.sit@google.net"),
        (15,"id.mollis.nec@hotmail.net"),
        (14,"id.mollis.nec@hotmail.net"),
        (16,"id.mollis.nec@hotmail.net");'''
    cursor_obj.execute(audience_insert)


    # MEETING_INSTANCES table
    cursor_obj.execute("DROP TABLE IF EXISTS MEETING_INSTANCES")
    meeting_instances = """ 
                CREATE TABLE MEETING_INSTANCES (
                    meetingID INTEGER NOT NULL,
                    orderID INTEGER NOT NULL,
                    fromdatetime VARCHAR(30),
                    todatetime VARCHAR(30),
                    isActive BOOLEAN,
                    PRIMARY KEY(meetingID, orderID)
                    FOREIGN KEY(meetingID) REFERENCES MEETINGS(meetingID)
            ); """

    cursor_obj.execute(meeting_instances)
    meeting_instances_insert = """INSERT INTO MEETING_INSTANCES (meetingID,orderID,fromdatetime, todatetime, isActive)
    VALUES
    (15,1,"25-07-2022 09:33:13","25-07-2022 10:33:13",0),
    (15,2,"07-05-2022 04:40:24","07-05-2022 05:40:24",0),
    (15,3,"05-06-2022 04:15:06","05-06-2022 05:15:06",0),
    (14,4,"02-06-2022 06:07:34","02-06-2022 07:07:34",0),
    (14,5,"17-03-2022 10:06:46","17-03-2022 11:06:46",0),
    (14,6,"31-01-2022 11:33:33","31-01-2022 12:33:33",0),
    (14,7,"07-07-2022 03:56:31","07-07-2022 04:56:31",0),
    (14,8,"14-05-2022 05:30:41","14-05-2022 06:30:41",0),
    (14,9,"27-01-2022 03:21:48","27-01-2022 04:21:48",0),
    (14,10,"22-02-2022 10:28:25","22-02-2022 11:28:25",0),
    (16,11,"23-05-2022 01:45:10","23-05-2022 02:45:10",0),
    (17,12,"07-04-2022 12:40:18","07-04-2022 13:40:18",0),
    (18,13,"28-05-2022 06:31:03","28-05-2022 07:31:03",0),
    (15,14,"03-04-2022 02:02:56","03-04-2022 03:02:56",0),
    (19,15,"26-02-2022 01:20:00","26-02-2022 02:20:00",0),
    (10,16,"16-05-2022 12:49:04","16-05-2022 13:49:04",0),
    (10,17,"10-01-2022 10:35:45","10-01-2022 11:35:45",0),
    (10,18,"14-06-2022 04:43:12","14-06-2022 05:43:12",0),
    (11,19,"24-07-2022 02:11:14","24-07-2022 03:11:14",0),
    (10,20,"03-03-2022 11:38:19","03-03-2022 12:38:19",0);"""
    cursor_obj.execute(meeting_instances_insert)

    cursor_obj.execute("DROP TABLE IF EXISTS EVENTS_LOG")
    log = """ 
        CREATE TABLE EVENTS_LOG (
            eventID INTEGER PRIMARY KEY AUTOINCREMENT,
            userID INTEGER NOT NULL,
            eventType VARCHAR(16),
            timestamp VARCHAR(25),
            FOREIGN KEY(userID) REFERENCES USERS(userID)
        ); """
    cursor_obj.execute(log)

    log_insert = """ 
    INSERT INTO EVENTS_LOG(eventID, userID, eventType, timestamp)
    VALUES
        (1,1,'join',1652084078),
        (2,1,'leave',1652084088), 
        (3,2,'join',1652084078),
        (4,2,'leave',1652084178);
    """
    cursor_obj.execute(log_insert)
    conn.commit()
    conn.close()
    return


def load_db_to_redis():
    # empty all contents previously stored after init
    # app.cache.flushdb()
    conn = app.get_db_connection()
    cursor_obj = conn.cursor()
    try:
        # load users to redis
        users = cursor_obj.execute("SELECT * FROM USERS").fetchall()
        for userID, name, age, gender, email in users:
            app.cache.hmset(f'user:{userID}', {
                "name": name,
                "age": age,
                "gender": gender,
                "email": email
            })
        users = None
        
        meetings = cursor_obj.execute("""
        SELECT * FROM MEETING_INSTANCES""").fetchall()
        for meetingID, orderID, fromDt, toDt, active in meetings:
            meeting_signature = f"{meetingID}:{orderID}"
            app.cache.hmset(f'meeting:{meeting_signature}', {
                "from": fromDt,
                "to": toDt,
                "isActive": active,
            })
            pass
        meetings = None

        # list of active
        meetings = cursor_obj.execute("""
        SELECT i.meetingID, i.orderID, a.userEmail
        FROM 
        MEETING_INSTANCES as i, AUDIENCE as a
        WHERE 
        i.meetingID = a.meetingID""").fetchall()
        print(meetings)
        print("===============")
        for meetingID, orderID, email in meetings:
            meeting_signature = f"{meetingID}:{orderID}"
            app.cache.sadd(f'meeting:{meeting_signature}:audience', email)
        meetings = None


        audience = cursor_obj.execute("SELECT * FROM AUDIENCE").fetchall()
        for meetingID, email in audience:
            app.cache.rpush(f'meeting:{meetingID}', email)
        audience = None
    except Exception as exc:
        logging.critical(exc)
    logging.info("OK")
    logging.info(app.cache.get("user:*"))
    for key in app.cache.scan_iter("meeting:*"):
        k = print(str(key).replace("b'","").replace("'",""))
        # print(app.cache.get(k))
