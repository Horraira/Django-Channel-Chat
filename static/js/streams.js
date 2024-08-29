const APP_ID = 'd24670d9480a443ebd774621d086a64a';
const TOKEN = '007eJxTYJBbyHliSZydWWTOw4/NZ26W74/ZcytH9v5dqfdfZC27DHYpMKQYmZiZG6RYmlgYJJqYGKcmpZibm5gZGaYYWJglmpkkrjS6kNYQyMjgnCXDwsgAgSA+C0NuYmYeAwMAidUfmQ=='
const CHANNEL = 'main'
let UID;

const client = AgoraRTC.createClient({ mode: 'rtc', codec: 'vp8' });

// index 0 is the microphone and index 1 is the camera
let localTracks = []
let remoteUsers = {}
let member = {
    name: "John Doe"  // Example name
};

let joiAndDisplayLocalStream = async () => {
    client.on('user-published', handleUserJoined)
    client.on('user-left', handleUserLeft)

    UID = await client.join(APP_ID, CHANNEL, TOKEN, null)

    localTracks = await AgoraRTC.createMicrophoneAndCameraTracks()

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

joiAndDisplayLocalStream()