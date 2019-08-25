/**
 * 메시지를 innerHTML에 넣기위해 포매팅하는 함수.
 * @param {message} message sb.~~.message? 
 */
const strfy = (message, flag) => {
    if (message._sender.userId == sb.currentUser.userId) return `<div class="me">${message.message}</div>`
    else if (flag == "anon") return `<div class="other">anon_${message._sender.metaData.anonKey} : ${message.message}</div>`
    return `<div class="other">${message._sender.userId} : ${message.message}</div>`
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

const addChannelBtn = (channel, to, flag, rev) => {
    const _with = channel.members.filter(v => v.userId != sb.currentUser.userId)[0]
    if(rev) to.innerHTML = `<li><div class="url" url="${channel.url}" with="${flag=="anon" ? "anon" : _with.userId}" flag="${flag}" anonKey="${_with.metaData.anonKey}">${flag=="norm" ? _with.userId : `anon_${_with.metaData.anonKey}`}</div></li>` +to.innerHTML
    else to.innerHTML += `<li><div class="url" url="${channel.url}" with="${flag=="anon" ? "anon" : _with.userId}" flag="${flag}" anonKey="${_with.metaData.anonKey}">${flag=="norm" ? _with.userId : `anon_${_with.metaData.anonKey}`}</div></li>`
}

const setChannelBtn = async (button, chat_header, chat_room) => {
    button.addEventListener('click', async e => {
        chat_header.innerHTML = `<span>${button.getAttribute('flag')=="norm" ? button.getAttribute('with') : button.getAttribute('flag')+'_'+button.getAttribute('anonKey') }</span>`
        chat_room.setAttribute('url', button.getAttribute('url'))
        chat_room.setAttribute('with', `${button.getAttribute('flag')=="norm" ? button.getAttribute('with') : button.getAttribute('flag')}`)
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

const customCreateChannel = (other, type) => {
    return new Promise( (res, rej) => {
        sb.GroupChannel.createChannelWithUserIds([other], DISTINCT = false, CUSTOM_TYPE = type, function (groupChannel, error) {
            if (error) console.log(error)
            else if (groupChannel.members.length!=2) {
                ((channel) => {
                    return new Promise((res,rej) => {
                        channel.leave(function(response, error) {
                            if (error) {
                                return;
                            }
                        })
                    })
                })(groupChannel)
                rej('no such user')
            }
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
    return await customCreateChannel(other, type)
}
