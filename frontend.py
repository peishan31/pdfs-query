css = '''
<style>
.chat-message {
    padding: 0.8rem;
    border-radius: 1rem;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.chat-message.user {
    background-color: #E0F7FA;
}

.chat-message.bot {
    background-color: #ECEFF1;
    justify-content: flex-start;
}

.chat-message .avatar {
    width: 50px;
    height: 50px;
}

.chat-message .avatar img {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    object-fit: cover;
}

.chat-message .message {
    padding: 0.8rem;
    border-radius: 1rem;
    margin: 0 0.5rem;
    color: #555;
    font-family: 'Quicksand', sans-serif;
    max-width: 80%;
    word-wrap: break-word;
}

button {
    border: none;
    padding: 0.5rem 1rem;
    margin: 0.5rem;
    border-radius: 1rem;
    background-color: #FFCDD2;
    color: #555;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

button:hover {
    background-color: #F8BBD0;
}
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/X8c6vRx/robot.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{message}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/7vhdqyt/user.png">
    </div>    
    <div class="message">{{message}}</div>
</div>
'''