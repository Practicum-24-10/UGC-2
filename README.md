# UGC-2

### Запуск приложения
- Создать файл .env в директории backend/ по примеру backend/.env.example и из корня проекта выполнить команду:
```
docker compose -f backend/docker-compose.yml up
```

### Запуск приложения для разработки (с проброской портов и монтированием директории приложения)
- Создать файл .env в директории backend/ по примеру backend/.env.example и из корня проекта выполнить команду:
```
docker compose -f backend/docker-compose.yml -f backend/docker-compose.override.yml up
```

### Результаты исследования Mongo vs Postgres:

По результатам исследования было загружено 20 миллионов записей в каждую базу данных.
В процессе записи производилось постоянное чтение рандомных записей.

![Результаты записи](https://github.com/Practicum-24-10/UGC-2/blob/main/storage_research/wright.png)

![Результаты чтения](https://github.com/Practicum-24-10/UGC-2/blob/main/storage_research/read.png)

### Вывод:
По результатам видно что в чтении база данных `Postgres` сильно проигрывает без оптимизации. 
`MongoDb`, напротив, "из коробки" почти не потеряла в скорости чтения.
