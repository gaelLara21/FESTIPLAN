const chatbotButton = document.getElementById("chatbot-button");
const chatbotWindow = document.getElementById("chatbot-window");
const chatbotClose = document.getElementById("chatbot-close");
const chatbotSend = document.getElementById("chatbot-send");
const chatbotInput = document.getElementById("chatbot-input");
const chatbotMessages = document.getElementById("chatbot-messages");

// Mostrar/ocultar el chatbot
chatbotButton.addEventListener("click", () => {
    chatbotWindow.style.display = "block";
});

chatbotClose.addEventListener("click", () => {
    chatbotWindow.style.display = "none";
});

// Función para enviar un mensaje
function sendMessage(message, fromUser = false) {
    const messageDiv = document.createElement("div");
    messageDiv.classList.add(fromUser ? "user-message" : "bot-message");
    messageDiv.innerHTML = message;
    chatbotMessages.appendChild(messageDiv);
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;  // Auto-scroll
}

// Función para obtener respuesta del chatbot (simulando el comportamiento con eventos)
chatbotSend.addEventListener("click", () => {
    const userMessage = chatbotInput.value.trim();
    if (userMessage) {
        sendMessage(userMessage, true);
        chatbotInput.value = "";
        
        // Simulamos la respuesta del chatbot
        if (userMessage.toLowerCase().includes("eventos")) {
            sendMessage("¿Te gustaría saber más sobre nuestros eventos? ¿Cuál te interesa?");
        } else if (userMessage.toLowerCase().includes("crear evento")) {
            sendMessage("¡Genial! Para crear un evento, necesitas estar registrado. ¿Te gustaría registrarte?");
        } else if (userMessage.toLowerCase().includes("mis eventos")) {
            $.ajax({
                url: "/mis_eventos",
                type: "GET",
                success: function(data) {
                    if (data.length > 0) {
                        data.forEach(evento => {
                            sendMessage(`Evento: ${evento.titulo}, Fecha: ${evento.fecha}`);
                        });
                    } else {
                        sendMessage("Aún no tienes eventos creados.");
                    }
                },
                error: function() {
                    sendMessage("Lo siento, hubo un problema al obtener tus eventos.");
                }
            });
        } else {
            sendMessage("Lo siento, no entendí tu solicitud. ¿Puedes reformular?");
        }
    }
});

// Opcional: puedes agregar un mensaje de bienvenida
sendMessage("Hola, soy Festy-Bot 🤖. ¿En qué puedo ayudarte hoy?");