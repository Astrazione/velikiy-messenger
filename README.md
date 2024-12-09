# OTRPO lab 7
## Установка необходимых библиотек
```bash
pip install tornado redis python-dotenv
```

## О приложении
Данное приложение представляет собой мессенджер, позволяющий обмениваться
текстовыми сообщениями в разных комнатах пользователями с разными идентификаторами
на основе фреймворка Tornado с помощью технологии Redis Pub/Sub
и протокола WebSocket.

## Подготовка к запуску
Перед запуском скриптов необходимо в файле `params.env` указать переменные среды:
порт и адрес хоста Redis и приложения. Перед запуском приложения база данных должна быть готова принимать запросы.

## Запуск
Входная точка программы `app.py`.

При подключении через браузер пользователю необходимо указать nickname и название комнаты, к которой он хотел бы подключиться. 
Если пользователь откажется вводить данные, автоматически будут установлены значения "guest" и "general".

После "регистрации" пользователь увидит свой nickname и комнату, а также сам чат,
содержащий сообщения с момента входа в комнату.
Пользователь может написать и отправить сообщение, которые увидят все участники комнаты.