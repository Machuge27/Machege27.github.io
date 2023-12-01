class Chatbox{
    constructor(){
        this.args={
            openButton:document.querySelector('.chatbot__button'),
            chatButton:document.querySelector('.chatbot__support'),
            sendButton:document.querySelector('.send__button'),
        }
        this.state=false;
        this.message=[];
    }
    display(){
        const {openButton,Chatbox,sendButton}=this.args
        openButton.addEventListener("click",()=>this.toggleState(chatbox))
        sendButton.addEventListener("click",()=>this.onSendButton(chatbox))
        const node=chatbox.querySelector("input");
        node.addEventListener("keyup",({key})=>{
            if(key==="Enter"){
    this.onSendButton(chatbox)
 }        
})

    }
    toggleState(chatbox){
        this.state=!this.state
        //shows on hides the box
        if(this.state){
            chatbox.classList.add("chatbox--active")
        }else{
            chatbox.classList.remove("chatbox--active")
        }
    }onSendButton(chatbox){
        var textField=chatbox.querySelector("input");
        let text1=textField.value
        if(text1===""){
            return;
        }
        let msg1={name:"User",message:text1}
        this.message.push(msg1);
        //http://127.0.0.1:5000
        fetch($SCRIPT_ROOT+"/predict",{
            method:"POST",
            body:JSON.stringify({message:text1}),
            mode:"cars",
            headers:{
                "Content-type":"application/json"
            },
        })//Promise<response
        .then(r=>r.json())//Promise<any>
        .then(r=>{
            let msg2={name:"Sam",message:r.answer};
            this.message.push(msg2)
            this.updateChatText(chatbox)
            textField.value=""
        }).catch((error)=>{
            console.log("Error:",error)
            this.updateChatText(chatbox)
            textField.value=""
        })
    }
    updateChatText(){
        var html=""
        this.message.slice().reverse().forEach(function(item){
            if(item.name==="Sam"){
                html+="<div class='messages__item messages__item--visitor'>"+item.message+"</div>"
            }else{
                html+="<div class='messages__item messages__item--operator'>"+item.message+"</div>"
            }
        });
        const chatmessage=chatbox.querySelector(".chatbox__messages");
        chatmessage.inneHTML=html
    }
}
const chatbox=new Chatbox()
chatbox.display() 