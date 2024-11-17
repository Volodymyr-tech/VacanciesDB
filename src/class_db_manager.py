import psycopg2

class DBManager:


    def __init__(self):
        self.__host="localhost"
        self.__database="almacen"
        self.__user="postgres"
        self.__password="GGWP96"


    def get_conn_db(self):
        try:
            # Подключаемся к базе данных PostgreSQL
            conn = psycopg2.connect(
                host=self.__host,
                database=self.__database,
                user=self.__user,
                password=self.__password
            )
            print(f"Установлено подключение к {self.__database}")
            return conn

        except Exception as error:
            print("Ошибка подключения:", error)
            return None


    def create_table(self):
        conn = self.get_conn_db()
        print(conn)
        cur = conn.cursor()

        cur.execute("CREATE TABLE employers (employer_id varchar PRIMARY KEY, company_name VARCHAR, vacancies_url VARCHAR, address varchar);")

        cur.execute("INSERT INTO employers (employer_id, company_name, vacancies_url, address ) VALUES (%s, %s,  %s, %s)", ('4949', 'Procter & Gamble', 'https://hh.ru/vacancy/110222029', 'Алматы'))

        cur.execute("SELECT * FROM employers;")
        res = cur.fetchone()
        print(res)
        conn.commit()


    def close_conn(self):
        pass









if __name__ == "__main__":

    connection = DBManager()
    con = connection.create_table()
    print(con)