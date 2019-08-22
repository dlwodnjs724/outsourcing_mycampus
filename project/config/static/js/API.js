/**
 * 메시지를 innerHTML에 넣기위해 포매팅하는 함수.
 * @param {message} message sb.~~.message? 
 */
const strfy = (message) => {
    return `${message._sender.userId} : ${message.message}<br>`
}
/**
 * 채널의 채팅 로그 10개 불러와서 쿼리 리턴해주는 함수.
 * @param {channel} channel sb.GroupChannel 인스턴스?
 */
const loadLog = (channel) => {
    const log = channel.createPreviousMessageListQuery()
    log.limit = 10;
    log.reverse = false;
    return log
}

const sb = new SendBird({ appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256' });

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = function (channel, message) {
    chatroom.innerHTML += strfy(message)
    chatroom.scrollTop = chatroom.scrollHeight;
};

ChannelHandler.onUserReceivedInvitation = function(groupChannel, inviter, invitees) {
    if(sb.currentUser.userId != inviter.userId) {
        sb.currentUser.createMetaData({
            [inviter.userId]: groupChannel.url
        })
    }
};

sb.addChannelHandler(0, ChannelHandler);