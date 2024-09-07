const userInput = document.getElementById('user-input');
const conversationArea = document.getElementsByClassName('conversation-area')[0];
const chatBox = document.getElementsByClassName('chat-area-main')[0];
function get_data(){
    let data_txt = document.getElementById("bot_data_hidden").value;
    data_txt = data_txt.replace(/'/g, '"');
    return JSON.parse(data_txt);
}
const ai_data = get_data();
function chat_maker(data,active=false){
    let active_str = active ? 'active' : '';
    return `
    <div onclick="window.location.href=window.location.origin+'/chat/${data.nickname}'" class="msg `+active_str+`">
        <img class="msg-profile" src="${data.image_url}" alt="" />
        <div class="msg-detail">
            <div class="msg-username">${data.name}</div>
            <div class="msg-content">
                <span class="msg-message">Today</span>
                <span class="msg-date" style="display:none">20m</span>
            </div>
        </div>
    </div>
    `;
}
function message_maker(data,owner=false){
    let owner_text = '';
    let message_class = ' ai_message ';
    let image_url = '';
    if(owner){
        image_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/User-avatar.svg/2048px-User-avatar.svg.png';
        owner_text = ' owner ';
        message_class = ' owner_message ';
    }else{
        image_url = ai_data.image_url;
    }
    return `
    <div class="chat-msg `+owner_text+`">
        <div class="chat-msg-profile">
            <img class="chat-msg-img" src="${image_url}" alt="" />
            <div class="chat-msg-date">Message sent ${data.date}</div>
        </div>
        <div class="chat-msg-content">
            <div class="chat-msg-text `+message_class+`">${data.message}</div>
        </div>
    </div>
    `;
}
document.addEventListener("keypress", (event)=>{
    if(event.key=='Enter'){
        handleSend()
    }
});
function get_current_time(){
    const dateObj = new Date();

    const day = dateObj.getDate();
    const month = dateObj.getMonth() + 1;
    const year = dateObj.getFullYear();
    const hours = dateObj.getHours();
    const minutes = dateObj.getMinutes();
    const seconds = dateObj.getSeconds();

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}
function iso_to_regular_date(isoDate){
    const dateObj = new Date(isoDate);

    const day = dateObj.getDate();
    const month = dateObj.getMonth() + 1;
    const year = dateObj.getFullYear();
    const hours = dateObj.getHours();
    const minutes = dateObj.getMinutes();
    const seconds = dateObj.getSeconds();

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}
function generating_animation(type='open'){
    if(type=='open'){
        chatBox.innerHTML += `
        <div class="chat-msg" id="generating_animation">
            <div class="chat-msg-profile">
                <img class="chat-msg-img" src="${ai_data.image_url}" alt="" />
                <div class="chat-msg-date">generating..</div>
            </div>
            <div class="chat-msg-content">
                <div class="chat-msg-text">...</div>
            </div>
        </div>
        `;
    }else{
        document.getElementById('generating_animation').remove();
    }
    return 0;
}
function add_message(data,owner=false){
    chatBox.innerHTML += message_maker(data,owner);
}
function add_chat(data,active=false){
    conversationArea.innerHTML = chat_maker(data,active)+conversationArea.innerHTML;
}
async function handleSend() {
    let userInputValue = userInput.value
    own_message_data = {
        "message":userInputValue
        ,"date":get_current_time()
    };
    add_message(own_message_data,true);
    document.getElementById('user-input').value = '';//empty the input
    const messages = create_messages_json();
    generating_animation();
    const botResponse = await sendMessage(userInputValue,messages,own_message_data.date);
    generating_animation('close');
    ai_message_data = {
        "message":botResponse.message.content
        ,"date":iso_to_regular_date(botResponse.created_at)
    };
    add_message(ai_message_data);
}
function create_messages_json(){
    const owner_messages = Array.prototype.slice.call( document.getElementsByClassName("owner_message") )
    const ai_messages = Array.prototype.slice.call( document.getElementsByClassName("ai_message") )
    let messages = []
    owner_messages.forEach((message,index) => {
        messages.push({role:'user',content:owner_messages[index].innerHTML});
        if(ai_messages[index]){
            messages.push({role:'assistant',content:ai_messages[index].innerHTML});
        }                
    })
    return messages
}