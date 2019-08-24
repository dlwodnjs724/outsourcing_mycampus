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
const loadLog = (url, length, to) => {
    return new Promise((res, rej) => {
        sb.GroupChannel.getChannel(url, (groupChannel, error) => {
            if (error) return
            const log = groupChannel.createPreviousMessageListQuery()
            log.limit = length;
            log.reverse = false;
            log.load((messages, error) => {
                if (error) rej(error);
                res(messages.reduce((acc, cur) => {
                    return acc + strfy(cur)
                }, ""))
            })
        })
    })
}


const findInvitee = (channel) => {
    const first = channel.members[0]
    const second = channel.members[1]

    if (channel.inviter.userId == first.userId) return second
    else return first
}

const setBase = async (chat_list, chat_header, chat_room) => {
    const buttons = [...chat_list.querySelectorAll('button')]
    buttons.forEach(cur => {
        setChannelBtn(cur, chat_header, chat_room)
    })
}

const addChatBtn = async (channel, to) => {
    const _with = channel.members.filter(v => v.userId != sb.currentUser.userId)[0].userId
    to.innerHTML += `<button class="url" url="${channel.url}" with="${_with}">with ${_with}</button><br>`
}

const setChannelBtn = async (button, chat_header, chat_room) => {
    button.addEventListener('click', async e => {
        chat_header.innerHTML = `chat with ${button.getAttribute('with')}`
        chat_room.setAttribute('url', button.getAttribute('url'))
        chat_room.setAttribute('with', button.getAttribute('with'))
        chat_room.innerHTML = await loadLog(button.getAttribute('url'), 10)
        chat_room.scrollTop = chat_room.scrollHeight;
    })
}
const getNext = (Query, to) => {
    return new Promise((res, rej) => {
        Query.next(function (channelList, error) {
            if (error) return;
            res(channelList)
        })
    })
}

const loadChatList = async (to) => {
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

const openChat = (other) => {
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
            resolve(groupChannel.channel)
        })
    })
}

const sb = new SendBird({
    appId: 'A0DB6C4C-7F09-4D64-B43C-0823B2B35256'
});

const ChannelHandler = new sb.ChannelHandler();

ChannelHandler.onMessageReceived = function (channel, message) {
    try {
        if (chat_room.getAttribute('url') == channel.url) {
            chat_room.innerHTML += strfy(message)
            chat_room.scrollTop = chat_room.scrollHeight;
        } else {
            console.log('got message')
        }
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