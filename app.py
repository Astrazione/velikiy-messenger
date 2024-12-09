import logging
import os

import tornado.ioloop
import tornado.web
import tornado.websocket
import redis
import asyncio
import json

from dotenv import load_dotenv

env = load_dotenv('params.env')
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

# Загрузка переменных окружения
APP_HOST = os.getenv("APP_HOST")
APP_PORT = int(os.getenv("APP_PORT"))
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# Хранилище подключений
connections = {}


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


class ChatWebSocketHandler(tornado.websocket.WebSocketHandler):
    redis_pub = None
    redis_sub = None
    username = None
    room_name = None

    def initialize(self, redis_pub):
        self.redis_pub = redis_pub
        self.redis_sub = redis_pub.pubsub()

    def check_origin(self, origin) -> bool:
        return True

    async def open(self):
        self.username = self.get_argument("user", "guest")
        self.room_name = self.get_argument("room_name", "general")
        connections[self.username] = self

        self.redis_sub.subscribe(self.room_name)

        logging.info(f"User {self.username} connected to {self.room_name}")
        self.redis_pub.publish(self.room_name, json.dumps({"type": "join", "user": self.username}))

        asyncio.create_task(self.listen_to_redis())

    async def on_message(self, message):
        data = json.loads(message)
        room = data.get("room", 'general')
        self.redis_pub.publish(room, json.dumps({"type": "message", "user": self.username, "text": data["text"]}))

    async def listen_to_redis(self):
        while True:
            message = self.redis_sub.get_message(ignore_subscribe_messages=True)
            if message:
                data = json.loads(message["data"].decode("utf-8"))
                await self.write_message(data)
            await asyncio.sleep(1)

    def on_close(self):
        if self.username in connections:
            del connections[self.username]
        logging.info(f"User {self.username} disconnected.")

    def is_user_in_room(self, user):
        return


async def make_app():
    redis_conn = redis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    redis_pub = redis_conn

    return tornado.web.Application([
            (r"/", MainHandler),
            (r"/websocket", ChatWebSocketHandler, {"redis_pub": redis_pub}),
        ],
        static_path='static'
    )

if __name__ == "__main__":
    app = asyncio.run(make_app())
    app.listen(APP_PORT)
    logging.info(f"Server started on http://localhost:{APP_PORT}")
    tornado.ioloop.IOLoop.current().start()
