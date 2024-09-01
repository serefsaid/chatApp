async function sendMessage(last_prompt,messages) {
    const response = await fetch('http://localhost:5000/responder', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ last_prompt: last_prompt,messages:messages })
    });
    const data = await response.json();
    return data;
}