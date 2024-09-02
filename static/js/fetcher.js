async function sendMessage(last_prompt,messages) {
    const bot_nickname = window.location.pathname.split('/')[2];
    const response = await fetch(window.location.origin+'/responder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ last_prompt: last_prompt,messages:messages,bot_nickname:bot_nickname })
    });
    const data = await response.json();
    return data;
}