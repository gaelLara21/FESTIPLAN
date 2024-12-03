// Variables
const chatbotButton = document.getElementById('chatbot-button');
const chatbotWindow = document.getElementById('chatbot-window');
const chatbotClose = document.getElementById('chatbot-close');
const chatbotMessages = document.getElementById('chatbot-messages');
const chatbotInput = document.getElementById('chatbot-input');
const chatbotSend = document.getElementById('chatbot-send');

// Abrir el chatbot
chatbotButton.addEventListener('click', () => {
    chatbotWindow.style.display = 'block';
});

// Cerrar el chatbot
chatbotClose.addEventListener('click', () => {
    chatbotWindow.style.display = 'none';
});

// Enviar mensajes
chatbotSend.addEventListener('click', () => {
    const userMessage = chatbotInput.value;
    if (userMessage.trim() !== '') {
        // Mostrar el mensaje del usuario
        const userBubble = document.createElement('div');
        userBubble.textContent = userMessage;
        userBubble.style.textAlign = 'right';
        userBubble.style.margin = '5px 0';
        chatbotMessages.appendChild(userBubble);

        // Simular respuesta automática
        setTimeout(() => {
            const botBubble = document.createElement('div');
            botBubble.textContent = 'Hola ¡Soy Festy-Bot 🎉! ¿cómo puedo ayudarte?';
            botBubble.style.textAlign = 'left';
            botBubble.style.margin = '5px 0';
            chatbotMessages.appendChild(botBubble);

            // Desplazar hacia abajo
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
        }, 1000);

        chatbotInput.value = '';
    }
});
