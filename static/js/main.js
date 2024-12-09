const nickname = prompt("Введите имя пользователя:") || "guest";
const room_name = prompt("Введите название комнаты:") || "general";
const ws = new WebSocket(`ws://localhost:8888/websocket?user=${encodeURIComponent(nickname)}&room_name=${encodeURIComponent(room_name)}`);

const messageBox = document.getElementById("message-box");
const messageInput = document.getElementById("message-input");
const sendBtn = document.getElementById("send-btn");

document.getElementById('user').innerText = 'Пользователь: ' + nickname;
document.getElementById('room').innerText = 'Комната: ' + room_name;

ws.onmessage = (event) => {
    console.log(room_name);
    console.log('Message')
    const data = JSON.parse(event.data);
    const messageDiv = document.createElement("div");
    if (data.type === "message") {
        messageDiv.textContent = `${data.user}: ${data.text}`;
    } else if (data.type === "join") {
        messageDiv.textContent = `${data.user} joined the room.`;
    }
    messageBox.appendChild(messageDiv);
};

sendBtn.addEventListener("click", () => {
    const text = messageInput.value;
    console.log(JSON.stringify({ text: text, room: room_name }));
    ws.send(JSON.stringify({ text: text, room: room_name }));
    messageInput.value = "";
});

ws.onopen = (event) => {
    console.log('Connected')
}

ws.onclose = (event) => {
    console.log('Disconnected')
}