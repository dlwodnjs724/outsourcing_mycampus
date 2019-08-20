const sb = new SendBird({ appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256' });

const ChannelHandler = new sb.ChannelHandler();
ChannelHandler.onMessageReceived = function (channel, message) {
    chatroom.innerHTML = chatroom.innerHTML +`${message._sender.userId} : ${message.message}<br>`
};

sb.addChannelHandler(0, ChannelHandler);
