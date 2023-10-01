from neo4j import GraphDatabase, RoutingControl

# Функция для установки соединения с базой данных
driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "4543444а3"))
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "4543444а3")

# Функция POST для добавления аэропорта
def add_airport(driver, AirportName, City):
    driver.execute_query(
        "MERGE (a:Aeroport {AirportName: $AirportName, City: $City})",
        AirportName=AirportName, City=City
    )

# Функция POST для добавления связи между аэропортами с указанием свойства FlightName
def add_flight(driver, From, To, FlightName):
    driver.execute_query(
        "MATCH (From:Aeroport {AirportName: $From}), (To:Aeroport {AirportName: $To})"
        "MERGE (From)-[r:flight { FlightName:$FlightName}]->(To)",
        From=From, To=To, FlightName = FlightName
    )

# Функция PUT для выполнения PUT-запроса для изменения AirportName
def update_airport_name(driver, AirportName, NewName):
    with driver.session() as session:
        query = (
            "MATCH (a:Aeroport {AirportName: $AirportName}) "
            "SET a.AirportName = $NewName"
        )
        session.run(query, AirportName=AirportName, NewName=NewName)

# Функция GET для вывода связей аэропорта
def print_flights(driver, AirportName):
    records, _, _ = driver.execute_query(
        "MATCH (From:Aeroport {AirportName: $AirportName})-[r:flight]->(To:Aeroport) "
        "RETURN From, r, To",
        AirportName=AirportName
    )
    for record in records:
        print(record["From"], record["r"]["FlightName"], record["To"])

#with GraphDatabase.driver(URI, auth=AUTH) as driver:
    #add_airport(driver, "Vnukovo", "Moscow")
    #add_airport(driver, "Kazan_International_Airport", "Kazan")
    #add_flight(driver, "Kazan_International_Airport", "Vnukovo", "d123")
    #print_flights(driver, " Miami_International ")

while True:
    print("\nВыберите действие:")
    print("1. Добавить аэропорт")
    print("2. Добавить связь между аэропортами")
    print("3. Вывести данные аэропорта")
    print("4. Изменить название у аэропорта")
    print("0. Выйти")

    choice = input("Введите номер действия: ")
    if choice == '1':
        AirportName = input("Введите название аэропорта: ")
        City = input("Введите город: ")
        add_airport(driver, AirportName, City)
        print(f"Аэропорт {AirportName} добавлен.")
    elif choice == '2':
        From = input("Введите название отправного аэропорта: ")
        To = input("Введите название аэропорта назначения: ")
        FlightName = input("Введите название рейса: (например y654)")
        add_flight(driver, From, To, FlightName)
        print(f"Связь между {From} и {To} с рейсом {FlightName} добавлена.")
    elif choice == '3':
        AirportName = input("Введите название аэропорта: ")
        print_flights(driver, AirportName)
    elif choice == '4':
        AirportName = input("Введите название аэропорта: ")
        NewName = input("Введите новое название аэропорта: ")
        update_airport_name(driver, AirportName, NewName)
        print(f"AirportName аэропорта {AirportName} изменен на {NewName}.")
    elif choice == '0':
        break
    else:
        print("Неверный выбор. Попробуйте снова.")