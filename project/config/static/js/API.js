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
const loadLog = (channel, length, to) => {
    const log = channel.createPreviousMessageListQuery()
    log.limit = length;
    log.reverse = false;
    return new Promise((res, rej) => {
        log.load((messages, error) => {
            if (error) rej(error);
            res(messages.reduce((acc, cur) => {
                return acc + strfy(cur)
            }, ""))
        })
    })
}

const showLog = (channel, length, to) => {}

const findInvitee = (channel) => {
    const first = channel.members[0]
    const second = channel.members[1]

    if (channel.inviter.userId == first.userId) return second
    else return first
}

const getNext = (Query, to) => {
    return new Promise((res, rej) => {
        const list = []
        Query.next(function (channelList, error) {
            if (error) return;
            for (c of channelList) {
                list.push({
                    "with": c.members.filter(v => v.userId != sb.currentUser.userId)[0].userId,
                    "url": c.url
                })
            }
            if (to) to.innerHTML = list.map(cur => `<button class="url" value="${cur.url}" name="${cur.with}">with ${cur.with}</button><br>`).join('')
            res(channelList)
        })
    })
}

const loadChatList = async (sb, to) => {
    const CLQ = sb.GroupChannel.createMyGroupChannelListQuery()
    CLQ.includeEmpty = true;
    if (CLQ.hasNext) {
        return await getNext(CLQ, to)
    };
}

const leaveChat = (channel) => {
    return new Promise((resolve, reject) => {
        channel.leave(function (response, error) {
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
                try {
                    await leaveChat(groupChannel.channel)
                } catch (e) {
                    alert(e)
                }
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
        chat_room.innerHTML += strfy(message)
        chat_room.scrollTop = chat_room.scrollHeight;
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