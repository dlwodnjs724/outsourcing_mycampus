/**
 * 메시지를 innerHTML에 넣기위해 포매팅하는 함수.
 * @param {message} message sb.~~.message? 
 */
const strfy = (message, flag) => {
    if (message._sender.userId == sb.currentUser.userId) return `you : ${message.message}<br>`
    else if (flag == "anon") return `anon : ${message.message}<br>`
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
                    return acc + strfy(cur, groupChannel.customType)
                }, ""))
            })
        })
    })
}

const setBase = async (chat_list, chat_header, chat_room) => {
    const buttons = [...chat_list.querySelectorAll('button')]
    buttons.forEach(cur => {
        setChannelBtn(cur, chat_header, chat_room)
    })
}

const addChannelBtn = (channel, to, flag) => {
    const _with = channel.members.filter(v => v.userId != sb.currentUser.userId)[0].userId
    to.innerHTML += `<button class="url" url="${channel.url}" with="${_with}" flag="${flag}">with ${flag=="norm" ? _with : "anon"}</button><br>`
}

const setChannelBtn = async (button, chat_header, chat_room) => {
    button.addEventListener('click', async e => {
        chat_header.innerHTML = `chat with ${button.getAttribute('flag')=="norm" ? button.getAttribute('with') : button.getAttribute('flag') }`
        chat_room.setAttribute('url', button.getAttribute('url'))
        chat_room.setAttribute('with', button.getAttribute('with'))
        chat_room.setAttribute('flag', button.getAttribute('flag'))
        chat_room.innerHTML = await loadLog(button.getAttribute('url'), 10)
        chat_room.scrollTop = chat_room.scrollHeight;
    })
}


const loadChatList = async () => {
    const CLQ = sb.GroupChannel.createMyGroupChannelListQuery()
    CLQ.includeEmpty = true;
    CLQ.order = 'latest_last_message'
    if (CLQ.hasNext) {
        return await ((Q) => {
            return new Promise((res, rej) => {
                Q.next((channelList, error) => {
                    if (error) rej(error);
                    res(channelList)
                })
            })
        })(CLQ)
    };
}

const C_C = (other, type) => {
    return new Promise( (res, rej) => {
        sb.GroupChannel.createChannelWithUserIds([other], DISTINCT = false, CUSTOM_TYPE = type, function (groupChannel, error) {
            if (error) console.log(error)
            res(groupChannel)
        })
    })
}

const openAChat = async (other, type) => {
    if (other == sb.currentUser.userId) throw new Error('param err')
    const channels = await loadChatList(other)
    const targets = channels.filter(cur => {
        if (cur.members.filter(_cur => _cur.userId == other).length) return cur
    })
    if (targets.length == 2) throw new Error('already 2 chat')
    else if (targets.length == 1 && targets[0].customType == type) throw new Error(`already existing ${type} chat`)
    const ret =  await C_C(other, type)
    console.log(ret)
    return ret
}
