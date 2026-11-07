import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Item {
    id: root
    property QtObject theme

    ListModel { id: chatModel }

    function loadHistory() {
        chatModel.clear()
        const msgs = backend.getCurrentMessages()
        for (let i = 0; i < msgs.length; i++) {
            chatModel.append({ role: msgs[i].role, text: msgs[i].content, time: msgs[i].time })
        }
    }

    Component.onCompleted: { loadHistory(); inputArea.forceActiveFocus(); }

    // ---------- Linke Sidebar (System & Tools) -----------------------
    Rectangle {
        id: leftSidebar
        anchors.top: parent.top; anchors.left: parent.left; anchors.bottom: parent.bottom
        anchors.margins: 16
        width: 260
        color: theme.bgCard
        radius: theme.radius
        border.color: theme.border
        border.width: 1

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16

            // Sidebar Header
            RowLayout {
                Layout.fillWidth: true
                spacing: 8
                Rectangle { width: 8; height: 8; radius: 4; color: backend.ollamaOk ? theme.ok : theme.danger }
                Text {
                    text: "SYSTEM STATUS"
                    color: theme.textDim
                    font.family: theme.fontMono
                    font.pixelSize: 10
                    font.letterSpacing: 1
                }
            }

            // Kompakte Status-Karten
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 8
                StatusCard { Layout.fillWidth: true; theme: root.theme; label: "Model"; value: "qwen3:14b" }
                StatusCard { Layout.fillWidth: true; theme: root.theme; label: "CPU"; value: Math.round(backend.cpuPercent) + " %" }
                StatusCard { Layout.fillWidth: true; theme: root.theme; label: "Memory"; value: Math.round(backend.ramPercent) + " %" }
                StatusCard { Layout.fillWidth: true; theme: root.theme; label: "Voice"; value: "Piper TTS" }
            }

            Item { Layout.fillHeight: true }

            // Kleiner, dezenter Kern am unteren Rand der Sidebar
            EvoxCore {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: 60
                Layout.preferredHeight: 60
                state: backend.state
                accentColor: theme.accent
            }
        }
    }

    // ---------- Rechter Hauptbereich (Chat) --------------------------
    Rectangle {
        id: mainChatArea
        anchors.top: parent.top; anchors.left: leftSidebar.right; anchors.right: parent.right; anchors.bottom: parent.bottom
        anchors.topMargin: 16; anchors.bottomMargin: 16; anchors.rightMargin: 16; anchors.leftMargin: 16
        color: theme.bgCard
        radius: theme.radius
        border.color: theme.border
        border.width: 1

        // Header
        Item {
            id: chatHeader
            anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; height: 56
            Text {
                anchors.left: parent.left; anchors.leftMargin: 24; anchors.verticalCenter: parent.verticalCenter
                text: "EVOX Assistant"
                color: theme.text; font.family: theme.fontMain; font.pixelSize: 16; font.weight: Font.DemiBold
            }
            Button {
                anchors.right: parent.right; anchors.rightMargin: 20; anchors.verticalCenter: parent.verticalCenter; text: "Clear Chat"
                onClicked: { chatModel.clear(); backend.clearHistory(); }
                background: Rectangle { radius: theme.radiusSm; color: parent.down ? theme.bgCardHi : "transparent"; border.color: theme.border; border.width: 1 }
                contentItem: Text { text: parent.text; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 11; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                implicitHeight: 28; implicitWidth: 80
            }
            Rectangle { anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; height: 1; color: theme.border }
        }

        // Chat Liste
        ListView {
            id: chatList
            anchors.top: chatHeader.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: inputContainer.top
            anchors.margins: 24; clip: true; spacing: 24; model: chatModel
            ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; width: 6 }

            delegate: Item {
                width: chatList.width; height: delegateColumn.implicitHeight
                Column {
                    id: delegateColumn; width: parent.width; spacing: 6
                    Row {
                        spacing: 12
                        Text {
                            text: model.role === "user" ? "You" : model.role === "assistant" ? "EVOX" : "System"
                            color: model.role === "user" ? theme.textDim : model.role === "assistant" ? theme.accent : theme.warning
                            font.family: theme.fontMain; font.pixelSize: 13; font.weight: Font.Bold
                        }
                        Text { text: model.time; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 11; anchors.verticalCenter: parent.verticalCenter }
                    }
                    Text {
                        width: parent.width; text: model.text; color: theme.text; font.family: theme.fontMain; font.pixelSize: 14; wrapMode: Text.Wrap; lineHeight: 1.3
                    }
                }
            }
            onCountChanged: Qt.callLater(() => positionViewAtEnd())
        }

        // Eingabefeld (Schwebend im Chat)
        Item {
            id: inputContainer
            anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.margins: 24
            height: 52

            Rectangle {
                anchors.fill: parent
                radius: theme.radius
                color: theme.bg
                border.color: inputArea.activeFocus ? theme.accent : theme.border
                border.width: 1
                Behavior on border.color { ColorAnimation { duration: 200 } }

                TextArea {
                    id: inputArea
                    anchors.left: parent.left; anchors.right: sendButton.left; anchors.top: parent.top; anchors.bottom: parent.bottom
                    anchors.leftMargin: 16; anchors.rightMargin: 8; topPadding: 15; bottomPadding: 15; leftPadding: 0; rightPadding: 0
                    placeholderText: backend.state === "thinking" ? "EVOX is thinking..." : "Ask EVOX anything..."
                    placeholderTextColor: theme.textFaint; color: theme.text; font.family: theme.fontMain; font.pixelSize: 14
                    background: null; wrapMode: TextArea.Wrap; enabled: backend.state === "idle"

                    Keys.onPressed: (event) => {
                        if (event.key === Qt.Key_Return && !(event.modifiers & Qt.ShiftModifier)) {
                            event.accepted = true; sendMessage();
                        }
                    }
                }

                Rectangle {
                    id: sendButton
                    anchors.right: parent.right; anchors.rightMargin: 8; anchors.verticalCenter: parent.verticalCenter
                    width: 80; height: 36; radius: theme.radiusSm
                    color: backend.state === "idle" ? (sendMouse.containsMouse ? theme.accent : theme.bgCardHi) : "transparent"
                    
                    Text {
                        anchors.centerIn: parent; text: "Send"
                        color: sendMouse.containsMouse && backend.state === "idle" ? theme.bg : (backend.state === "idle" ? theme.text : theme.textFaint)
                        font.family: theme.fontMain; font.pixelSize: 13; font.weight: Font.DemiBold
                    }
                    MouseArea {
                        id: sendMouse; anchors.fill: parent; hoverEnabled: true; enabled: backend.state === "idle"; cursorShape: Qt.PointingHandCursor; onClicked: sendMessage()
                    }
                }
            }
        }
    }

    // ... (Connections & sendMessage bleiben identisch) ...
    Connections {
        target: backend
        function onHistoryReloaded() { loadHistory() }
        function onResponseChunk(chunk) {
            if (chatModel.count > 0 && chatModel.get(chatModel.count - 1).role === "assistant") {
                const last = chatModel.count - 1; const prev = chatModel.get(last).text
                chatModel.setProperty(last, "text", prev + chunk)
            }
        }
        function onResponseFinished(fullText) {
            if (chatModel.count > 0 && chatModel.get(chatModel.count - 1).role === "assistant") {
                chatModel.setProperty(chatModel.count - 1, "text", fullText)
            }
        }
        function onResponseError(err) { console.log(err) /* Fehlerbehandlung */ }
        function onSystemMessageAdded(msg) {
            chatModel.append({ role: "system", text: msg, time: Qt.formatTime(new Date(), "HH:mm") })
        }
    }

    function sendMessage() {
        const t = inputArea.text.trim()
        if (!t || backend.state !== "idle") return
        const now = Qt.formatTime(new Date(), "HH:mm")
        chatModel.append({ role: "user", text: t, time: now })
        chatModel.append({ role: "assistant", text: "", time: now })
        inputArea.text = ""
        backend.sendMessage(t)
    }
}