function sendMessage(){
    const input = document.getElementById('chat_input');
    const message = input.value.trim(); //kullanıcının girdiği veri.
    
   

    if(message) {
        addMessageToChat(message , 'user-message');
        input.value='';

        fetch('/new_chat' , {

            method: 'POST' , 
            headers: {
                'Content-Type':'application/json',
            },
            body:JSON.stringify({user_message:message,bot_message:"This is answer from BOT!!"}),
        })
    
        .then(response => response.json())
        .then(data => {
            console.log('Received bot message', data.Bot_message)
            addMessageToChat(data.Bot_message,'bot-message') //return jsonfiy'daki "Bot_message" dan geliyor.
        })
        .catch(error => console.error('HaTa:',error));
    
}
}


// Mesajı Chat'e yazdırır.
function addMessageToChat(message,className){

    tmpMessage = message
    if(className == 'bot-message' ){
        tmpMessage=marked.parse(message)
    }
    const  chatContainer = document.getElementById('chat_container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message',className);
    messageElement.innerHTML=tmpMessage;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop=chatContainer.scrollHeight;

}




function handleKeyDown(event){
     if(event.key === 'Enter'){
         event.preventDefault(); // Sayfanın yenilenmesini engeller
         sendMessage();
    }
 }

