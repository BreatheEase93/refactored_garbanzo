import os
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080
BASE_DIR = "pages_html"  # Папка, где лежат все файлы сайта


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Определяем путь к файлу
        if self.path == "/":
            file_path = os.path.join(BASE_DIR, "contacts.html")
        else:
            # Убираем начальный "/" и собираем путь
            file_path = os.path.join(BASE_DIR, self.path.lstrip("/"))

        # 2. Пытаемся открыть и отправить файл
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            self.send_response(200)

            # 3. Указываем правильный тип контента
            if file_path.endswith(".css"):
                self.send_header("Content-type", "text/css")
            elif file_path.endswith(".html"):
                self.send_header("Content-type", "text/html; charset=utf-8")

            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        print(f"Получены данные от пользователя:\n{post_data}")

        # 4. Отправляем ответ браузеру, чтобы он не "завис" в ожидании
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        response = f"<h1>Спасибо!</h1><p>Данные получены: {post_data}</p><a href='/'>Назад</a>"
        self.wfile.write(response.encode('utf-8'))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()