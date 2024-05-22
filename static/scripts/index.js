document.addEventListener('DOMContentLoaded', function() {
    const messagesElement = document.getElementById('messages');
    if (messagesElement) {
        const messages = JSON.parse(messagesElement.textContent);
        messages.forEach(message => {
            alert(`${message.tags}: ${message.message}`);
        });
    }
});
