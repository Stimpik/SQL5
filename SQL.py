import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE phones;
        DROP TABLE clients;
        """)

        cur.execute(
            """CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            client_name VARCHAR(40) NOT NULL,
            client_surname VARCHAR(40) NOT NULL,
            client_email VARCHAR(40) NOT NULL UNIQUE);
                   
            CREATE TABLE IF NOT EXISTS phones (
            phone_id SERIAL PRIMARY KEY,
            client_id INTEGER REFERENCES clients(client_id),
            phone_number VARCHAR(25) NOT NULL UNIQUE);
        """)
        conn.commit()


def add_client(conn, name, surname, email, phone=None):
    with conn.cursor() as cur:
        cur.execute(
            """INSERT INTO clients(client_name, client_surname, client_email)
            VALUES (%s, %s, %s) RETURNING client_id;
        """, (name, surname, email))
        id = cur.fetchone()
        conn.commit()
        if phone != None:
            cur.execute(
                """INSERT INTO phones(client_id, phone_number)
                VALUES (%s, %s);
            """, (id, phone))
            conn.commit()


def add_phone(conn, client_id, phone_number):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phones(client_id, phone_number)
                VALUES (%s, %s);
            """, (client_id, phone_number))
        conn.commit()


def change_client(conn, client_id, name, surname, email, phone=None):
    with conn.cursor() as cur:
        cur.execute("""UPDATE clients SET client_name = %s, client_surname = %s, client_email = %s
        WHERE client_id = %s;
        """, (name, surname, email, client_id))
        conn.commit()
        cur.execute('SELECT COUNT(phone_number) from phones WHERE client_id = %s', client_id)
        if phone == None:
            pass

        elif cur.fetchone()[0] == 0:
            add_phone(conn, client_id, phone)

        else:
            cur.execute('SELECT COUNT(phone_number) from phones WHERE client_id = %s', client_id)
            if cur.fetchone()[0] == 1:
                cur.execute('UPDATE phones SET phone_number = %s WHERE client_id = %s', (phone, client_id))
                conn.commit()
            else:
                cur.execute('SELECT phone_number, phone_id from phones WHERE client_id = %s', client_id)
                for num in cur.fetchall():
                    print(f'Номер телефона {num[0]}, id телефона {num[1]}')
                print('Укажите id того телефона, который вы хотите заменить: ')
                id = str(input())
                cur.execute('UPDATE phones SET phone_number = %s WHERE phone_id = %s', (phone, id))
                conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s AND phone_number = %s;", (client_id, phone))
        conn.commit()


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM phones WHERE client_id = %s;", client_id)
        cur.execute("DELETE FROM clients WHERE client_id = %s", client_id)
        conn.commit()


def find_info(conn, value):
    with conn.cursor() as cur:
        cur.execute("""SELECT client_name, client_surname, client_email, phone_number FROM clients
                    JOIN phones ON clients.client_id = phones.client_id WHERE client_name = %s OR client_surname = %s OR client_email = %s OR phone_number = %s""",
                    (value, value, value, value))
        for client in cur.fetchall():
            print(
                f'Имя : {client[0]}, Фамилия: {client[1]}, адрес электронной почты {client[2]}, номер телефона: {client[3]}')


with psycopg2.connect(database="sqldb", user="postgres", password="qwerty15") as conn:
# create_db(conn)
# add_client(conn, )
# add_phone(conn, )
# change_client(conn, )
# delete_phone(conn, )
# delete_client(conn, )
# find_info(conn, )
