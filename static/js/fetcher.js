const bot_nickname = window.location.pathname.split('/')[2];
async function sendMessage(last_prompt,messages,date) {
    const response = await fetch(window.location.origin+'/responder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ last_prompt: last_prompt,messages:messages,bot_nickname:bot_nickname,date:date })
    });
    const data = await response.json();
    console.log(data)
    return data;
}
async function clearChatHistory() {
    const response = await fetch(window.location.origin+'/clear_model_chat_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bot_nickname:bot_nickname })
    });
    const data = await response.json();
    return data;
}