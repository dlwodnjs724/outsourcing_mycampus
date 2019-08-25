const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = function (channel, message) {
    try {
        if (chat_room.getAttribute('url') == channel.url) {
            chat_room.innerHTML += strfy(message, chat_room.getAttribute('flag'))
            chat_room.scrollTop = chat_room.scrollHeight;
        } else alert(`got message from ${channel.customType=='anon' ? "anon" : message._sender.userId}`)
    } catch (e) {
        alert(`got message`)
    }
};

ChannelHandler.onUserReceivedInvitation = async function (groupChannel, inviter, invitees) {
    try {
        if (sb.currentUser.userId != inviter.userId) {
            try {
                const buttons = document.getElementsByClassName('url')
                addChannelBtn(groupChannel, chat_list)
                setChannelBtn(buttons[buttons.length - 1], chat_header, chat_room)
            } catch (e) {
                alert(e)
            }
        }
    } catch (e) {
        alert(`${groupChannle.customType =="anon" ? "anon" : inviter.userId} invited you to chat.`)
    }

};

sb.addChannelHandler(0, ChannelHandler);