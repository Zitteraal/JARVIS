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
            chatModel.append({
                role: msgs[i].role,
                text: msgs[i].content,
                time: msgs[i].time
            })
        }
    }

    Component.onCompleted: {
        loadHistory()
        inputArea.forceActiveFocus()
    }

    // ---------- Linke Status-Spalte ----------------------------------
    ScrollView {
        id: leftPanel
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        anchors.leftMargin: 24
        width: 280
        clip: true
        ScrollBar.vertical.policy: ScrollBar.AlwaysOff

        ColumnLayout {
            width: leftPanel.availableWidth
            spacing: 10

            StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "Ollama"
                value: backend.ollamaMessage
                valueColor: backend.ollamaOk ? theme.ok : theme.danger
                accentBar:  backend.ollamaOk ? theme.ok : theme.danger
            }
            StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "Mikrofon"
                value: "inaktiv · Phase 3"
                valueColor: theme.textDim
                accentBar:  theme.textFaint
            }
             StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "Sprachausgabe"
                value: "Piper TTS · Aktiv"
                valueColor: theme.ok
                accentBar:  theme.ok
            }
            StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "CPU"
                value: Math.round(backend.cpuPercent) + " %"
                accentBar: theme.accent
            }
            StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "RAM"
                value: Math.round(backend.ramPercent) + " %"
                accentBar: theme.gold
            }
            StatusCard {
                Layout.fillWidth: true
                theme: root.theme
                label: "Erinnerungen"
                value: backend.memoryCount + " gespeichert"
                accentBar: theme.info
            }

            Item { Layout.fillHeight: true }

            Button {
                Layout.fillWidth: true
                text: "VERBINDUNG PRÜFEN"
                onClicked: backend.refreshOllamaStatus()
                background: Rectangle {
                    radius: theme.radiusSm
                    color: parent.down ? theme.bgCardHi : theme.bgCard
                    border.color: theme.border
                    border.width: 1
                }
                contentItem: Text {
                    text: parent.text
                    color: theme.textDim
                    font.family: theme.fontMono
                    font.pixelSize: 10
                    font.letterSpacing: 1.6
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                implicitHeight: 34
            }
        }
    }

    // ---------- Rechte Chat-Spalte -----------------------------------
    Rectangle {
        id: rightPanel
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        anchors.rightMargin: 24
        width: 420
        radius: theme.radius
        color: theme.bgCard
        border.color: theme.border
        border.width: 1

        Item {
            id: rightHeader
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 44

            Text {
                anchors.left: parent.left
                anchors.leftMargin: 16
                anchors.verticalCenter: parent.verticalCenter
                text: "KONVERSATION"
                color: theme.textDim
                font.family: theme.fontMono
                font.pixelSize: 10
                font.letterSpacing: 2
            }

            Button {
                anchors.right: parent.right
                anchors.rightMargin: 12
                anchors.verticalCenter: parent.verticalCenter
                text: "NEU"
                onClicked: {
                    chatModel.clear()
                    backend.clearHistory()
                }
                background: Rectangle {
                    radius: theme.radiusSm
                    color: parent.down ? theme.bgCardHi : "transparent"
                    border.color: theme.border
                    border.width: 1
                }
                contentItem: Text {
                    text: parent.text
                    color: theme.textFaint
                    font.family: theme.fontMono
                    font.pixelSize: 9
                    font.letterSpacing: 1.2
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                implicitHeight: 24
                implicitWidth: 60
            }

            Rectangle {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 12
                anchors.rightMargin: 12
                height: 1
                color: theme.border
            }
        }

        ListView {
            id: chatList
            anchors.top: rightHeader.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.topMargin: 8
            anchors.bottomMargin: 8
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            clip: true
            spacing: 10
            model: chatModel

            ScrollBar.vertical: ScrollBar {
                policy: ScrollBar.AsNeeded
                width: 6
            }

            delegate: Item {
                width: chatList.width
                height: delegateColumn.implicitHeight

                Column {
                    id: delegateColumn
                    width: parent.width
                    spacing: 4

                    Row {
                        spacing: 8
                        Text {
                            text: model.role === "user" ? "DU" :
                                  model.role === "assistant" ? "J.A.R.V.I.S." : "SYSTEM"
                            color: model.role === "user" ? theme.gold :
                                   model.role === "assistant" ? theme.accent :
                                   theme.danger
                            font.family: theme.fontMono
                            font.pixelSize: 9
                            font.letterSpacing: 1.6
                            font.weight: Font.DemiBold
                        }
                        Text {
                            text: model.time
                            color: theme.textFaint
                            font.family: theme.fontMono
                            font.pixelSize: 9
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }

                    Text {
                        width: parent.width
                        text: model.text
                        color: theme.text
                        font.family: theme.fontMain
                        font.pixelSize: 13
                        wrapMode: Text.Wrap
                        lineHeight: 1.15
                    }

                    Rectangle {
                        width: parent.width
                        height: 1
                        color: theme.border
                        opacity: 0.5
                    }
                }
            }

            onCountChanged: Qt.callLater(() => positionViewAtEnd())
        }
    }

    // ---------- Mittelbereich: Neural Core + Input -------------------
    Item {
        id: centerArea
        anchors.top: parent.top
        anchors.left: leftPanel.right
        anchors.right: rightPanel.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 20
        anchors.rightMargin: 20

        NeuralCore {
            id: neuralCore
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: Math.max(20, (parent.height - height - 160) * 0.35)
            width:  Math.min(parent.width, parent.height - 200) * 0.72
            height: width
            state:  backend.state
            accentColor: theme.accent
            goldColor:   theme.gold
        }

        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: neuralCore.bottom
            anchors.topMargin: 6
            spacing: 4
            Text {
                text: backend.state === "thinking" ? "DENKT NACH" :
                      backend.state === "error"    ? "FEHLER" :
                      "BEREIT"
                color: backend.state === "error" ? theme.danger : theme.gold
                font.family: theme.fontMono
                font.pixelSize: 11
                font.letterSpacing: 3
                anchors.horizontalCenter: parent.horizontalCenter
            }
            Text {
                text: backend.ollamaOk
                    ? "Alle Systeme nominal."
                    : "Ollama nicht erreichbar."
                color: theme.textDim
                font.family: theme.fontMain
                font.pixelSize: 12
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        Rectangle {
            id: inputBox
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 24
            anchors.horizontalCenter: parent.horizontalCenter
            width:  Math.min(parent.width * 0.9, 680)
            height: 58
            radius: theme.radius
            color: theme.bgCard
            border.color: inputArea.activeFocus ? theme.accentDim : theme.border
            border.width: 1

            Behavior on border.color { ColorAnimation { duration: 200 } }

            TextArea {
                id: inputArea
                anchors.left: parent.left
                anchors.right: sendButton.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: 16
                anchors.rightMargin: 8
                topPadding: 18
                bottomPadding: 12
                leftPadding: 0
                rightPadding: 0
                placeholderText: backend.state === "thinking"
                    ? "J.A.R.V.I.S. verarbeitet …"
                    : "Befehl oder Nachricht eingeben …"
                placeholderTextColor: theme.textFaint
                color: theme.text
                font.family: theme.fontMain
                font.pixelSize: 14
                background: null
                wrapMode: TextArea.Wrap
                enabled: backend.state === "idle"

                Keys.onPressed: (event) => {
                    if (event.key === Qt.Key_Return && !(event.modifiers & Qt.ShiftModifier)) {
                        event.accepted = true
                        sendMessage()
                    }
                }
            }

            Rectangle {
                id: sendButton
                anchors.right: parent.right
                anchors.rightMargin: 8
                anchors.verticalCenter: parent.verticalCenter
                width: 90
                height: 42
                radius: theme.radiusSm
                color: sendMouse.containsMouse && backend.state === "idle"
                    ? theme.accent : theme.accentDim
                opacity: backend.state === "idle" ? 1.0 : 0.4
                Text {
                    anchors.centerIn: parent
                    text: "SENDEN"
                    color: "#1a0a02"
                    font.family: theme.fontMono
                    font.pixelSize: 10
                    font.weight: Font.Bold
                    font.letterSpacing: 1.6
                }
                MouseArea {
                    id: sendMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    enabled: backend.state === "idle"
                    cursorShape: Qt.PointingHandCursor
                    onClicked: sendMessage()
                }
            }
        }
    }

    // ---------- Fehlerbanner -----------------------------------------
    Rectangle {
        id: errorBanner
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 12
        width:  errorText.implicitWidth + 40
        height: 36
        radius: theme.radiusSm
        color: "#2a0e0c"
        border.color: theme.danger
        border.width: 1
        visible: errorText.text.length > 0
        opacity: visible ? 1.0 : 0.0
        z: 50

        Behavior on opacity { NumberAnimation { duration: 200 } }

        Text {
            id: errorText
            anchors.centerIn: parent
            color: theme.danger
            font.family: theme.fontMain
            font.pixelSize: 12
            text: ""
        }
    }

    Timer {
        id: errorClearTimer
        interval: 5000
        onTriggered: errorText.text = ""
    }

    // ---------- Verbindungen -----------------------------------------
    Connections {
        target: backend

            function onHistoryReloaded() {
        loadHistory()
    }

    function onSystemMessageAdded(msg) {
        // System-Nachrichten werden direkt als eigener Chat-Eintrag hinzugefügt
        chatModel.append({
            role: "system",
            text: "⚙️ " + msg,
            time: Qt.formatTime(new Date(), "HH:mm")
        })
    }

    function onResponseChunk(chunk) {
            if (chatModel.count > 0 &&
                chatModel.get(chatModel.count - 1).role === "assistant") {
                const last = chatModel.count - 1
                const prev = chatModel.get(last).text
                chatModel.setProperty(last, "text", prev + chunk)
            }
        }

        function onResponseFinished(fullText) {
            if (chatModel.count > 0 &&
                chatModel.get(chatModel.count - 1).role === "assistant") {
                chatModel.setProperty(chatModel.count - 1, "text", fullText)
            }
        }

        function onResponseError(err) {
            errorText.text = err
            errorBanner.visible = true
            errorClearTimer.restart()
        }
    }

    // ---------- Senden -----------------------------------------------
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