const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = async function (channel, message) {
    try {
        if ((chat_box.getAttribute('url') == channel.url) && ((chat_box.getAttribute('anon') == 'true') == (channel.customType=="anon"))) {
            chat_box.innerHTML += strfy(message)
            chat_box.scrollTop = chat_box.scrollHeight;
        }
        const channels = await loadChatList()
        await renderChatList(channels, chat_list, chat_header, chat_box)
    } catch (e) {
        alert(`got new message`)
    }
};

ChannelHandler.onUserReceivedInvitation = async function (groupChannel, inviter, invitees) {
    if(sb.currentUser.userId == inviter.userId) return
    try {
        if (chat_box) {
            const channels = await loadChatList()
            await renderChatList(channels, chat_list, chat_header, chat_box)
        }
    } catch (e) {
        alert(`${groupChannel.customType =="anon" ? "anon" : inviter.userId} invited you to chat.`)
    }

};

sb.addChannelHandler(0, ChannelHandler);