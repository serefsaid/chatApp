async function handleSend() {
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<p>User: <span class="user_message">${userInput}</span></p>`;
    const messages = create_messages_json();
    const botResponse = await sendMessage(userInput,messages);
    console.log(botResponse);

    chatBox.innerHTML += `<p>${botResponse.model}: <span class="ai_message">${botResponse.message}</span></p>`;
}
function create_messages_json(){
    const user_messages = Array.prototype.slice.call( document.getElementsByClassName("user_message") )
    const ai_messages = Array.prototype.slice.call( document.getElementsByClassName("ai_message") )
    let messages = []
    user_messages.forEach((message,index) => {
        messages.push({role:'user',content:user_messages[index].innerHTML});
        if(ai_messages[index]){
            messages.push({role:'assistant',content:ai_messages[index].innerHTML});
        }                
    })
    return messages
}