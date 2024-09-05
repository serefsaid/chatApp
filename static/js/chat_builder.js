function message_maker(data,owner=false){
    let owner_text = '';
    let message_class = ' ai_message ';
    if(owner){
        owner_text = ' owner ';
        message_class = ' owner_message ';
    }
    return `
    <div class="chat-msg `+owner_text+`">
        <div class="chat-msg-profile">
            <img class="chat-msg-img" src="${data.image_url}" alt="" />
            <div class="chat-msg-date">Message sent ${data.date}</div>
        </div>
        <div class="chat-msg-content">
            <div class="chat-msg-text `+message_class+`">${data.message}</div>
        </div>
    </div>
    `;
}
function get_data(){
    let data_txt = document.getElementById("bot_data_hidden").value;
    data_txt = data_txt.replace(/'/g, '"');
    return JSON.parse(data_txt);
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
const ai_data = get_data();
function generating_animation(type='open'){
    if(type=='open'){
        const chatBox = document.getElementsByClassName('chat-area-main')[0];
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
async function handleSend() {
    const userInput = document.getElementById('user-input').value;
    const chatBox = document.getElementsByClassName('chat-area-main')[0];
    own_message_data = {
        "message":userInput
        ,"image_url":'https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/User-avatar.svg/2048px-User-avatar.svg.png'
        ,"date":get_current_time()
    };
    chatBox.innerHTML += message_maker(own_message_data,true);
    document.getElementById('user-input').value = '';//empty the input
    const messages = create_messages_json();
    generating_animation();
    const botResponse = await sendMessage(userInput,messages);
    generating_animation('close');
    own_message_data = {
        "message":botResponse.message.content
        ,"image_url":ai_data.image_url
        ,"date":iso_to_regular_date(botResponse.created_at)
    };
    chatBox.innerHTML += message_maker(own_message_data);
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