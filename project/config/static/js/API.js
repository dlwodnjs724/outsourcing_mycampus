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
const findInvitee = (channel) => {
    const first = channel.members[0]
    const second = channel.members[1]

    if (channel.inviter.userId == first.userId) return second
    else return first
}

const loadChatList = (sb, to) => {
    const list = []
    const CLQ = sb.GroupChannel.createMyGroupChannelListQuery()
    CLQ.includeEmpty = true;
    if (CLQ.hasNext) {
        CLQ.next(function (channelList, error) {
            if (error) return;
            for (c of channelList) {
                list.push(c.members.filter(v => v.userId != sb.currentUser.userId)[0].userId)
            }
            if (to) to.innerHTML = list.map(cur => `<a href="./${cur}">with ${cur}</a><br>`).join('')
            else return list
        })
    };
}

const leaveChat = (channel) => {
    return new Promise( (resolve, reject) => {
        channel.leave(function(response, error) {
            if (error) return
            reject('no such user')
        })
    })
}

const openChat = (sb, other) => {
    const params = new sb.GroupChannelParams();
    params.addUserIds([other]);
    if (sb.currentUser.userId == other) throw new Error('recursive')
    return new Promise(async (resolve, reject) => {
        sb.GroupChannel.createDistinctChannelIfNotExist(params, async function (groupChannel, error) {
            if (error) reject(error)
            if (!groupChannel.isCreated) reject('already exist')
            const invitee = findInvitee(groupChannel.channel)
            if (!invitee) {
                try { await leaveChat(groupChannel.channel) }
                catch (e) { alert(e) }
            }
            resolve('created')
        })
    })
}

const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = function (channel, message) {
    try {
        chatroom.innerHTML += strfy(message)
        chatroom.scrollTop = chatroom.scrollHeight;
    } catch {
        console.log('got message')
    }
};

ChannelHandler.onUserReceivedInvitation = function (groupChannel, inviter, invitees) {
    if (sb.currentUser.userId != inviter.userId) {
        console.log('invited')
    }
};

sb.addChannelHandler(0, ChannelHandler);