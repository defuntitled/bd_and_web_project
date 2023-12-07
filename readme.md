# Yet filesystem Disk Open API

### Функционал

- ручка /nodes/{id} позволяет по id получить информацию об объекте в файловой системе в формате json
- ручка /imports позволяет добавить объект в файловую систему (информацию следует передовать в формате json)
- ручка /delete/{id} позволяет удалить информацию из файловой системы

### Данные и API
Описание сущностей и путей приложения приведены в файле ```openapi.yaml```


**Как развернуть**

	git clone https://github.com/defuntitled/bd_and_web_project
	cd bd_and_web_project 
	docker-compose up

**Список используемых технологий**
- Flask для разработки логики сервиса
- Сервер Gunicorn + Nginx
- Sqlalchemy + sqlite для хранения данных
- Docker
