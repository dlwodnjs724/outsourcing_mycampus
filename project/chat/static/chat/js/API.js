const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = async function (channel, message) {
    try {
        if (chat_box.getAttribute('url') == channel.url) {
            chat_box.innerHTML += strfy(message, chat_box.getAttribute('flag'))
            chat_box.scrollTop = chat_box.scrollHeight;
        } else {
            const channels = await loadChatList()
            chat_list.innerHTML=""
            channels.forEach(cur => addChannelBtn(cur, chat_list, cur.customType))
            const buttons = [...chat_list.querySelectorAll('.url')]
            buttons.forEach(cur => {
                setChannelBtn(cur, chat_header, chat_box)
            })
        }
    } catch (e) {
        alert(`got message`)
    }
};

ChannelHandler.onUserReceivedInvitation = async function (groupChannel, inviter, invitees) {
    try {
        if(chat_box){
            if (sb.currentUser.userId != inviter.userId) {
                const buttons = document.getElementsByClassName('url')
                addChannelBtn(groupChannel, chat_list, groupChannel.customType, rev)
                setChannelBtn(buttons[buttons.length - 1], chat_header, chat_box)
            }
            else{
                console.log('sibal')
            }
        }
    } catch (e) {
        alert(`${groupChannel.customType =="anon" ? "anon" : inviter.userId} invited you to chat.`)
    }

};

sb.addChannelHandler(0, ChannelHandler);