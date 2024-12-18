document.addEventListener('alpine:init', () => {
            Alpine.data('chat', () => ({
                messages: [],
                newMessage: '',
                user: document.querySelector('input[name="username"]').value,
                roomName:  window.location.pathname.split('/')[2] || null,
                chatSocket: null,

                initChat() {
                    if (this.roomName) {
                        this.addMessages(this.roomName)
                        this.initWebSocket(this.roomName)
                    }
                },

                addMessages (newRoomName) {
                    fetch(`/chat/${newRoomName}/`)
                    .then(async res => {
                        const data = await res.json()
                        if (res.ok) {
                            this.messages = Object.keys(data['messages']).map(date => {
                                return {date: date, messages: data['messages'][date]}
                            })
                        }
                    })
                },

                initWebSocket(newRoomName) {
                    if (this.chatSocket) {
                        this.chatSocket.close()
                    }

                    this.chatSocket = new WebSocket(
                        'ws://' + window.location.host + '/ws/chat/' + this.roomName + '/'
                    )

                    this.chatSocket.onmessage = (e) => {
                        const data = JSON.parse(e.data)
                        const newMessage = {
                            date: data.date,
                            messages: [{
                            sender: this.user,
                            text: data.text.trim(),
                            message_id: data.message_id
                            }]
                        }
                        if (newMessage.date === this.messages[this.messages.length-1].date) {
                            this.messages[this.messages.length-1].messages.push(newMessage.messages[0])
                        } else {this.messages.push(newMessage)}
                    }

                    this.chatSocket.onclose = () => {
                        console.log('Chat closed')
                    }
                },

                changeChatRoom(newRoomName) {
                    if (window.location.pathname !== `/chat/${newRoomName}/`) {
                        history.pushState(null, '', `/chat/${newRoomName}/`)
                        this.roomName =  newRoomName
                        this.messages = []
                        this.initWebSocket(newRoomName)
                        this.addMessages(newRoomName)
                    }
                },

                sendMessage() {
                if (this.newMessage.trim() !== '') {
                    this.chatSocket.send(JSON.stringify({
                        room_name: this.roomName,
                        sender: this.user,
                        text: this.newMessage.trim()
                    }))
                    this.newMessage = ''
                    }
                }
            }))
            Alpine.data('chat_list', () => ({
                chats: [],
                getChatList () {
                    fetch(`/chats/list/`)
                    .then(async res => {
                        const data = await res.json()
                        console.log(data)
                        if (res.ok) {
                            this.chats = data
                        }
                    })
                },
            }))
        })