const APP_ID = 'd24670d9480a443ebd774621d086a64a';
const TOKEN = sessionStorage.getItem('token');
const CHANNEL = sessionStorage.getItem('room');
let UID = Number(sessionStorage.getItem('UID'));

let NAME = sessionStorage.getItem('name');

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

// index 0 is the microphone and index 1 is the camera
let localTracks = []
let remoteUsers = {}

let joiAndDisplayLocalStream = async () => {
    document.getElementById('room-name').innerText = CHANNEL

    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    try {
        await client.join(APP_ID, CHANNEL, TOKEN, UID)
        // await initLocalStream()
    } catch (error) {
        console.error(error)
        window.open('/video', '_self')
    }

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

    let member = await createMember()

    let player = `<div  class="video-container" id="user-container-${UID}">
                     <div class="video-player" id="user-${UID}"></div>
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`

    document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)

    localTracks[1].play(`user-${UID}`)

    await client.publish([localTracks[0], localTracks[1]])
}

let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video') {
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null) {
            player.remove()
        }

        let member = await getMember(user)

        player = `<div  class="video-container" id="user-container-${user.uid}">
                     <div class="video-player" id="user-${user.uid}"></div>
                     <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                  </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio') {
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for (let track of localTracks) {
        track.stop()
        track.close()
    }

    await client.leave()
    deleteMember()
    window.open('/video', '_self')
}

let toggleCamera = async (e) => {
    if (localTracks[1].muted) {
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let toggleMic = async (e) => {
    if (localTracks[0].muted) {
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    } else {
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let createMember = async () => {
    let response = await fetch(`/video/create_member/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'name': NAME,
            'room_name': CHANNEL,
            'uid': UID,
        })
    });

    let member = await response.json();
    return member;
}

let getMember = async (user) => {
    let response = await fetch(`/video/get_member/?uid=${user.uid}&room_name=${CHANNEL}`);

    let member = await response.json();
    return member;
}

let deleteMember = async () => {
    let response = await fetch(`/video/delete_member/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            'uid': UID,
            'name': NAME,
            'room_name': CHANNEL,
        })
    });
}

joiAndDisplayLocalStream()

window.addEventListener('beforeunload', deleteMember)

document.getElementById('leave-btn').onclick = leaveAndRemoveLocalStream
document.getElementById('camera-btn').onclick = toggleCamera
document.getElementById('mic-btn').onclick = toggleMic