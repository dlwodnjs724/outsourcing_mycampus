const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = async function (channel, message) {
    const pattern = /<button id="match(_m)?To(\w+)">match<\/button>/
    const matches = message.message.match(pattern)
    try {
        let m_user = ''
        let m_flag = false
        let m_tmp = ''
        if (matches) {
            m_flag = true
            m_tmp = matches[1] ? matches[1] : ""
            m_user = matches[2]
        }
        if ((chat_box.getAttribute('url') == channel.url) && ((chat_box.getAttribute('anon') == 'true') == (channel.customType == "anon"))) {
            chat_box.innerHTML += strfy(message)
            chat_box.scrollTop = chat_box.scrollHeight;
            chat_box_m.innerHTML += strfy(message)
            chat_box_m.scrollTop = chat_box_m.scrollHeight;
            if (m_flag) {
                document.getElementById(`match${m_tmp}To${m_user}`).addEventListener('click', async e => {
                    try {
                        await openAChat(m_user, 'anon')
                        const channels = await loadChatList()
                        const users = await loadUsers()
                        const btns = await renderChatList(channels, chat_list, chat_header, chat_box)
                        const btn = findChatBtn(btns, users, m_user, 'anon')
                        btn.click()
                    } catch (_e) {
                        if (_e.message == 1) alert('alreat existing')
                        else alert(_e)
                        e.stopPropagation()
                    }
                })
            }
        }
        const channels = await loadChatList()
        await renderChatList(channels, chat_list, chat_header, chat_box)
        await renderChatList(channels, chat_list_m, chat_header_m, chat_box_m)

    } catch (e) {
        if(message._sender.userId=='adm' && matches){
            alert('왜 초대하는데 채팅창에 없냐')
        }
        else if (e.message == "chat_box is not defined" || e.message == "chat_box_m is not defined") alert('got new msg')
        
    }
};

ChannelHandler.onUserReceivedInvitation = async function (groupChannel, inviter, invitees) {
    if (sb.currentUser.userId == inviter.userId) return
    try {
        if (chat_box) {
            const channels = await loadChatList()
            await renderChatList(channels, chat_list, chat_header, chat_box)
            await renderChatList(channels, chat_list_m, chat_header_m, chat_box_m)
        }
    } catch (e) {
        alert(`${groupChannel.customType =="anon" ? "anon" : inviter.userId} invited you to chat.`)
    }

};

sb.addChannelHandler(0, ChannelHandler);