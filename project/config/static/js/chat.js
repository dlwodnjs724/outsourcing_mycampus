const t_btn = document.getElementById('t_submit')
const m_btn = document.getElementById('m_submit')
const chatroom = document.getElementById('chatroom')
const url = []

const params = new sb.GroupChannelParams();
params.isDistinct = true;
params.name = 'test';

t_btn.addEventListener('click', e => {
    params.addUserIds([document.getElementById('target').value]);
    sb.GroupChannel.createChannel(params, function (groupChannel, error) {
        if (error) return;
        url.push(groupChannel.url)
    });
})

m_btn.addEventListener('click', e => {
    sb.GroupChannel.getChannel(url[0], function (groupChannel, error) {
        if (error) return;
        groupChannel.sendUserMessage(document.getElementById('message').value, function (userMessage,
            error) {
            if (error) return;
            chatroom.innerHTML = chatroom.innerHTML +`${userMessage._sender.userId} : ${userMessage.message}<br>`
        });

    });
})