/**
 * 메세지를 입력받고 chat_box의 innerHTML로 들어갈 chat div 양식의 문자열을 반환하는 함수
 * @param {message} message sb.~~.message? 
 * @returns string 
 */
const strfy = (message) => {
    const time = new Date(message.createdAt).toISOString()
    if (message._sender.userId == sb.currentUser.userId) return `<div class="chat me"> ${message.message}</div>`
    return `<div class="chat other"> ${message.message}</div>`
}
/**
 * 채널의 채팅 로그 10개 불러와서 쿼리 리턴해주는 함수.
 * @param {channel} channel sb.GroupChannel 인스턴스?
 * @return {String} 포매팅 된 10개의 채팅 로그
 */
const loadLog = (url, length) => {
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

/**
 * 입력 시간 부터 현재 시간까지 지난 시간을 s,m,d,w 단위로 출력해준다.
 * @param {Date} ms 밀리세컨드
 * @returns 지난 시간을 나타내는 문자열 "N s(m,d,w)"
 */
const getTimePassed = (ms) => {
    const mSec = (Date.now() - new Date(ms)) / 1000
    if (mSec < 0) return '0s'
    else if (mSec < 60) return `${Math.floor(mSec)}s`
    else if (mSec < 3600) return `${Math.floor(mSec/60)}m`
    else if (mSec < 86400) return `${Math.floor(mSec/3600)}h`
    else if (mSec < 604800) return `${Math.floor(mSec/86400)}d`
    else return `${Math.floor(mSec/604800)}w`
}

/**
 * @description 각 채널로 연결해주는 엘리먼트를 리턴해주는 함수
 * @param {channel} channel sb channel 객체
 * @returns element html양식의 문자열.
 */
const createChannelBtn = (channel) => {
    const _with = channel.members.filter(v => v.userId != sb.currentUser.userId)[0]
    const flag = channel.customType == 'anon' ? true : false
    const html = `
    <li>
        <div class="url ChannelBtn" url="${channel.url}" with="${flag? "anon" : _with.userId}" anonKey="${_with.metaData.anonKey}">
            <div class="prof">
                ${flag? '<img src="{% static "/svg/Anon.svg" %}" >' :"<img src="+_with.profileUrl+">"}
            </div>
            <div class="two-line">
                <div class="fst">
                    <div class="partner">
                        ${flag? `anon${_with.metaData.anonKey}` : _with.userId}
                    </div>
                    <div class="last-time">
                        ${channel.lastMessage==null ? "" : getTimePassed(channel.lastMessage.createdAt)}
                    </div>
                </div>
                <div class="sec">
                    <div class="last-msg">
                        ${channel.lastMessage==null ? "" : channel.lastMessage.message}
                    </div>
                </div>
            </div>
        </div>
    </li>
    `
    return html
}

/**
 * @description to 의 innerHTML에 elements를 추가해준다.
 * @param {String} elements html양식의 문자열.
 * @param {Element} to innerHTML에 엘리먼트를 추가할 요소
 */
const addChannelBtn = (elements, to) => {
    elements.forEach( cur => {
        to.innerHTML += cur
    })
}

/**
 * 채널버튼의 이벤트리스너를 세팅하는 함수. 클릭되면 chat_header와 chat_box의 값을 수정해 채팅방을 연결해준다.
 * @param {Element} button 버튼 엘리먼트
 * @param {Element} chat_header chat_header
 * @param {Element} chat_box chat_box
 */
const setChannelBtn = async (button, chat_header, chat_box) => {
    button.addEventListener('click', async e => {
        chat_a.style.display = 'none';
        chat_m.style.display = 'flex';
        chat_back.style.display = 'block';
        chat_header.innerHTML = `<span>${button.querySelector('.partner').innerHTML}</span>`
        chat_box.setAttribute('url', button.getAttribute('url'))
        chat_box.setAttribute('with', `${button.querySelector('.partner').innerHTML}`)
        chat_box.setAttribute('anon', button.getAttribute('with') == 'anon' ? true : false)
        chat_box.innerHTML = await loadLog(button.getAttribute('url'), 10)
        chat_box.scrollTop = chat_box.scrollHeight;
    })
}


/**
 * @description 현재 유저에 연결된 채널 목록을 메시지가 최근에 온 순으로 정렬해서 반환하는 함수
 * @returns 정렬된 채널목록
 */
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

/**
 * @description 채널목록 엘리먼트들을 렌더링해주고 이벤트리스너 등록 후에 첫번째 엘리먼트를 리턴
 * @param {channels} channels 
 * @param {Element} chat_list 
 * @param {Element} chat_header 
 * @param {Element} chat_box 
 */
const renderChatList = async (channels, chat_list, chat_header, chat_box, last) => {
    if (channels.length) {
        chat_list.innerHTML = ""
        const elements = channels.map(cur => createChannelBtn(cur))
        addChannelBtn(elements, chat_list)
        const buttons = [...chat_list.querySelectorAll('.url')]
        buttons.forEach(async cur => {
            await setChannelBtn(cur, chat_header, chat_box)
        })
        return buttons
    }
}

/**
 * @description 스스로 혹은 존재하지 않는 유저를 초대할 경우 해결해주는 createChannel 함수
 * @param {sting} other 채팅 연결하려는 userId
 * @param {string} type 익명,실명 타입
 * @returns {Promise} 그룹이 에러 없이 생성되면 생성된 그룹채널을 반환
 */
const customCreateChannel = (other, type) => {
    return new Promise((res, rej) => {
        sb.GroupChannel.createChannelWithUserIds([other], DISTINCT = false, CUSTOM_TYPE = type, function (groupChannel, error) {
            if (error) rej(error)
            else if (groupChannel.members.length != 2) {
                ((channel) => {
                    return new Promise((res, rej) => {
                        channel.leave(function (response, error) {
                            if (error) return
                        })
                    })
                })(groupChannel)
                rej('no such user')
            }
            res(groupChannel)
        })
    })
}


/**
 * @description 에러 처리하고 두 유저사이에는 익명,실명 각각 한가지 타입의 채팅만 만들어주는 함수
 * @param {sting} other 채팅 연결하려는 userId
 * @param {string} type 익명,실명 타입
 * @returns {channel} 생선된 채널
 */
const openAChat = async (other, type) => {
    if (other == sb.currentUser.userId) throw new Error('self inviting is not allowed')
    const channels = await loadChatList(other)
    const targets = channels.filter(cur => {
        if (cur.members.filter(_cur => _cur.userId == other).length) return cur
    })
    if (targets.length == 2) throw new Error(1)
    else if (targets.length == 1 && targets[0].customType == type) throw new Error(2)
    return await customCreateChannel(other, type)
}

const findChatBtn = (btns, users, other, type) => {
    if (type != 'norm' && type != 'anon') return btns[0]
    const arr = btns.filter( cur => {
        if(type == 'norm'){
            return (cur.getAttribute('with') == other) 
        }
        else {
            return ((users.filter(cur => cur.userId == other)[0].metaData["anonKey"] == cur.getAttribute('anonkey')) && cur.getAttribute('with') != users.filter(cur => cur.userId == other)[0].userId)
        }
    })
    console.log(arr)
    return arr[0]

}

const loadUsers = async () => {
    return new Promise ((res,rej) => {
        const UserQ = sb.createApplicationUserListQuery()
        UserQ.next((users, err) => {
            if (err) rej('no users')
            else res(users)
        })
    })
    
} 