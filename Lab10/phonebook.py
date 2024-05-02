import psycopg2
import csv


conn = psycopg2.connect(
    host="localhost",
    database="asset",
    user="postgres",
    password="nurlan2006",
    port = 54322
)
cur = conn.cursor()
if conn.closed:
    print("Соединение с базой данных закрыто.")
else:
    print("Приложение подключено к базе данных.")



def inputData():
    name = input("Введите ваше имя: ")
    number = input("Введите ваш номер телефона: ")
    cur.execute('INSERT INTO phonebook("person_name", "phone_number") VALUES (%s, %s);', (name, number))
    conn.commit()


def update_contact(PersonName, PhoneNumber):
    cur.execute('UPDATE phonebook SET "phone_number" = %s WHERE "person_name" = %s;', (PhoneNumber, PersonName))
    conn.commit()


def deleteData():
    personName = input("Какое имя вы хотите удалить?\n")
    cur.execute(f'DELETE FROM phonebook WHERE "person_name" = %s;', (personName,))
    conn.commit()


def deleteAllData():
    cur.execute('DELETE FROM phonebook;')
    conn.commit()


while True:
    print("Что вы хотите сделать?\n\
          1. Ввести данные вручную\n\
          2. Обновить существующий контакт\n\
          3. Удалить данные по имени\n\
          4. Удалить все данные из таблицы\n\
          5. Выход")

    choice = input("Введите номер действия (1-7):\n")
    if choice == '1':
        inputData()
    elif choice == '2':
        name = input("Введите имя и новый номер через пробел: ").split()
        update_contact(*name)
    elif choice == '3':
        deleteData()
    elif choice == '4':
        deleteAllData()
    elif choice == '5':
        break

cur.close()
conn.close()