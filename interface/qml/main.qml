import QtQuick
import QtQuick.Window
import QtQuick.Controls.Basic
import QtQuick.Layouts

Window {
    id: appWindow
    width: 1440
    height: 900
    minimumWidth: 1120
    minimumHeight: 700
    visible: true
    color: theme.bg
    title: "EVOX"
    
    Theme { id: theme }

    property string activeView: "home"
    property string pendingProgram: ""
    property int confirmCountdown: 120

    Shortcut {
        sequence: "Ctrl+K"
        onActivated: commandCenterPopup.open()
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        Rectangle {
            Layout.fillHeight: true
            Layout.preferredWidth: 220
            color: theme.bgNav
            border.color: theme.border
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 4

                Text {
                    text: "E V O X"
                    color: theme.text
                    font.family: theme.fontMain
                    font.pixelSize: 16
                    font.weight: Font.Bold
                    font.letterSpacing: 4
                    Layout.alignment: Qt.AlignHCenter
                    Layout.topMargin: 8
                }
                Text {
                    text: "INTELLIGENCE. EVOLUTION. CONTROL."
                    color: theme.accentDim
                    font.family: theme.fontMono
                    font.pixelSize: 7
                    font.letterSpacing: 1
                    Layout.alignment: Qt.AlignHCenter
                    Layout.bottomMargin: 24
                }

                Text { text: "WORKSPACE"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1; Layout.topMargin: 8; Layout.bottomMargin: 4 }
                NavButton { buttonText: "Home"; active: appWindow.activeView === "home"; onClicked: appWindow.activeView = "home" }
                NavButton { buttonText: "Assistant"; active: appWindow.activeView === "assistant"; onClicked: appWindow.activeView = "assistant" }
                NavButton { buttonText: "Projects"; active: appWindow.activeView === "projects"; onClicked: appWindow.activeView = "projects" }
                NavButton { buttonText: "Memory"; active: appWindow.activeView === "memory"; onClicked: appWindow.activeView = "memory" }
                NavButton { buttonText: "Files"; active: appWindow.activeView === "files"; onClicked: appWindow.activeView = "files" }

                Text { text: "SYSTEM"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1; Layout.topMargin: 16; Layout.bottomMargin: 4 }
                NavButton { buttonText: "System Analysis"; active: appWindow.activeView === "system"; onClicked: appWindow.activeView = "system" }
                
                Item { Layout.fillHeight: true }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 8
                    Rectangle { Layout.fillWidth: true; height: 1; color: theme.border }
                    RowLayout {
                        Text { text: "Ollama Core"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 11 }
                        Item { Layout.fillWidth: true }
                        Text { text: backend.ollamaOk ? "ONLINE" : "OFFLINE"; color: backend.ollamaOk ? theme.accent : theme.danger; font.family: theme.fontMono; font.pixelSize: 9; font.weight: Font.Bold }
                    }
                }
            }
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 48
                color: theme.bg
                border.color: theme.border
                border.width: 1

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 24
                    anchors.rightMargin: 24
                    
                    Text {
                        text: {
                            if (appWindow.activeView === "home") return "Workspace / Home"
                            if (appWindow.activeView === "assistant") return "Workspace / Assistant"
                            if (appWindow.activeView === "projects") return "Workspace / Projects"
                            if (appWindow.activeView === "memory") return "Workspace / Memory"
                            if (appWindow.activeView === "files") return "Workspace / Files"
                            if (appWindow.activeView === "system") return "System / Analysis"
                            return "Workspace"
                        }
                        color: theme.textDim
                        font.family: theme.fontMain
                        font.pixelSize: 12
                    }
                    
                    Item { Layout.fillWidth: true }
                    
                    Rectangle {
                        width: 60; height: 24; radius: theme.radiusSm; color: theme.bgSurface; border.color: theme.border
                        Text { anchors.centerIn: parent; text: "Ctrl+K"; color: theme.textDim; font.family: theme.fontMono; font.pixelSize: 10 }
                        MouseArea { anchors.fill: parent; onClicked: commandCenterPopup.open() }
                    }

                    Text {
                        text: backend.currentTime
                        color: theme.text
                        font.family: theme.fontMono
                        font.pixelSize: 12
                    }
                }
            }

            Loader {
                Layout.fillWidth: true
                Layout.fillHeight: true
                sourceComponent: {
                    if (appWindow.activeView === "home") return homeView
                    if (appWindow.activeView === "assistant") return assistantView
                    if (appWindow.activeView === "projects") return projectsView
                    if (appWindow.activeView === "memory") return memoryView
                    if (appWindow.activeView === "files") return filesView
                    if (appWindow.activeView === "system") return systemView
                    return homeView
                }
            }
        }
    }

    Popup {
        id: confirmPopup
        anchors.centerIn: parent
        width: 500
        height: 260
        modal: true
        closePolicy: Popup.NoAutoClose

        Timer {
            id: countdownTimer
            interval: 1000
            repeat: true
            running: confirmPopup.visible
            onTriggered: {
                if (appWindow.confirmCountdown > 0) {
                    appWindow.confirmCountdown--
                } else {
                    confirmPopup.close()
                    backend.respondToConfirmation(false)
                }
            }
        }

        background: Rectangle {
            color: theme.bgSurface
            radius: theme.radius
            border.color: theme.danger
            border.width: 1
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 24
            spacing: 16

            Text {
                text: "CRITICAL ACTION AUTHORIZATION"
                color: theme.danger
                font.family: theme.fontMain
                font.pixelSize: 14
                font.weight: Font.Bold
                font.letterSpacing: 2
                Layout.alignment: Qt.AlignHCenter
            }

            Text {
                text: "Do you authorize EVOX to execute: '" + appWindow.pendingProgram + "'?"
                color: theme.text
                font.family: theme.fontMain
                font.pixelSize: 15
                wrapMode: Text.Wrap
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
            }

            Text {
                text: "Time remaining: " + appWindow.confirmCountdown + "s"
                color: theme.warning
                font.family: theme.fontMono
                font.pixelSize: 13
                Layout.alignment: Qt.AlignHCenter
            }

            Item { Layout.fillHeight: true }

            RowLayout {
                Layout.fillWidth: true
                spacing: 12

                Button {
                    text: "DENY"
                    Layout.fillWidth: true
                    onClicked: { confirmPopup.close(); backend.respondToConfirmation(false); }
                    background: Rectangle { radius: theme.radiusSm; color: parent.down ? theme.bgNav : theme.bgSurface; border.color: theme.border; border.width: 1 }
                    contentItem: Text { text: parent.text; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 12; font.weight: Font.Bold; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    implicitHeight: 40
                }

                Button {
                    text: "AUTHORIZE"
                    Layout.fillWidth: true
                    onClicked: { confirmPopup.close(); backend.respondToConfirmation(true); }
                    background: Rectangle { radius: theme.radiusSm; color: parent.down ? "#cc4b4b" : theme.danger; border.color: theme.danger; border.width: 1 }
                    contentItem: Text { text: parent.text; color: "#fff"; font.family: theme.fontMain; font.pixelSize: 12; font.weight: Font.Bold; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    implicitHeight: 40
                }
            }
        }
    }

    Popup {
        id: commandCenterPopup
        anchors.centerIn: parent
        width: 600
        height: 400
        modal: true
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        
        background: Rectangle {
            color: theme.bgSurface
            radius: theme.radius
            border.color: theme.borderHi
            border.width: 1
            layer.enabled: true
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Text { text: "COMMAND CENTER"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1 }

            Rectangle {
                Layout.fillWidth: true
                height: 48
                radius: theme.radiusSm
                color: theme.bg
                border.color: cmdInput.activeFocus ? theme.accent : theme.border
                border.width: 1

                TextArea {
                    id: cmdInput
                    anchors.fill: parent; anchors.margins: 12
                    topPadding: 0; bottomPadding: 0; leftPadding: 0; rightPadding: 0
                    placeholderText: "Type a command, ask a question, or search..."
                    placeholderTextColor: theme.textFaint; color: theme.text
                    font.family: theme.fontMain; font.pixelSize: 16; background: null
                    
                    Keys.onPressed: (event) => {
                        if (event.key === Qt.Key_Return) {
                            event.accepted = true
                            const text = cmdInput.text.trim()
                            if (text !== "") {
                                commandCenterPopup.close()
                                appWindow.activeView = "assistant"
                                backend.sendMessage(text)
                                cmdInput.text = ""
                            }
                        }
                    }
                }
            }
            
            Text { text: "Quick Actions"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 11; font.weight: Font.Medium; Layout.topMargin: 8 }

            GridLayout {
                Layout.fillWidth: true; columns: 2; rowSpacing: 8; columnSpacing: 8
                Rectangle { 
                    Layout.fillWidth: true; height: 36; radius: theme.radiusSm; color: theme.bg
                    Text { anchors.centerIn: parent; text: "Scan System"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 12 }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: { commandCenterPopup.close(); appWindow.activeView = "system" } }
                }
                Rectangle { 
                    Layout.fillWidth: true; height: 36; radius: theme.radiusSm; color: theme.bg
                    Text { anchors.centerIn: parent; text: "New Project"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 12 }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: { commandCenterPopup.close(); backend.sendMessage("Create a new project") } }
                }
            }
            Item { Layout.fillHeight: true }
        }
        onOpened: cmdInput.forceActiveFocus()
    }

    Component {
        id: homeView
        Item {
            ColumnLayout {
                anchors.fill: parent; anchors.margins: 32; spacing: 24
                Text { text: "Good evening. What are we working on?"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 24; font.weight: Font.DemiBold }

                RowLayout {
                    Layout.fillWidth: true; spacing: 16
                    ActionCard { cardTitle: "New Project"; cardDesc: "Start a new codebase"; cardIcon: "＋" }
                    ActionCard { cardTitle: "System Scan"; cardDesc: "Analyze PC performance"; cardIcon: "⚙" }
                    ActionCard { cardTitle: "Resume Task"; cardDesc: "Continue previous work"; cardIcon: "▶" }
                }

                RowLayout {
                    Layout.fillWidth: true; Layout.fillHeight: true; spacing: 24
                    Rectangle {
                        Layout.fillWidth: true; Layout.fillHeight: true
                        color: theme.bgSurface; radius: theme.radius; border.color: theme.border; border.width: 1
                        ColumnLayout {
                            anchors.fill: parent; anchors.margins: 16
                            Text { text: "ACTIVE TASKS"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1 }
                            Text { text: "No tasks currently running."; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 13; Layout.topMargin: 8 }
                            Item { Layout.fillHeight: true }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true; Layout.fillHeight: true
                        color: theme.bgSurface; radius: theme.radius; border.color: theme.border; border.width: 1
                        ColumnLayout {
                            anchors.fill: parent; anchors.margins: 16
                            Text { text: "RECENT ACTIVITY"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; font.letterSpacing: 1 }
                            Text { text: "No recent activity."; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 13; Layout.topMargin: 8 }
                            Item { Layout.fillHeight: true }
                        }
                    }
                }
            }
        }
    }

    Component {
        id: assistantView
        Item {
            ListModel { id: chatModel }
            function loadHistory() {
                chatModel.clear()
                const msgs = backend.getCurrentMessages()
                for (let i = 0; i < msgs.length; i++) chatModel.append({ role: msgs[i].role, text: msgs[i].content, time: msgs[i].time })
            }
            Component.onCompleted: loadHistory()

            Item {
                id: chatHeader
                anchors.top: parent.top; anchors.left: parent.left; anchors.right: parent.right; height: 50
                
                Text {
                    anchors.left: parent.left; anchors.leftMargin: 24; anchors.verticalCenter: parent.verticalCenter
                    text: "Conversation History"
                    color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 12; font.weight: Font.Medium
                }
                
                Button {
                    anchors.right: parent.right; anchors.rightMargin: 24; anchors.verticalCenter: parent.verticalCenter
                    text: "CLEAR CHAT"
                    onClicked: {
                        chatModel.clear()
                        backend.clearHistory()
                    }
                    background: Rectangle { 
                        radius: theme.radiusSm
                        color: parent.down ? theme.bgNav : theme.bgSurface
                        border.color: theme.border
                        border.width: 1 
                    }
                    contentItem: Text { 
                        text: parent.text
                        color: theme.textDim
                        font.family: theme.fontMain
                        font.pixelSize: 10
                        font.weight: Font.Bold
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter 
                    }
                    implicitHeight: 28
                    implicitWidth: 90
                }
            }

            ListView {
                id: chatList
                anchors.top: chatHeader.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.bottom: inputAreaContainer.top
                anchors.margins: 24; clip: true; spacing: 20; model: chatModel
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }
                delegate: Item {
                    width: chatList.width
                    height: delegateCol.implicitHeight
                    Column {
                        id: delegateCol
                        width: parent.width
                        spacing: 6
                        Row {
                            spacing: 10
                            Text { text: model.role === "user" ? "You" : model.role === "assistant" ? "EVOX" : "System"; color: model.role === "user" ? theme.textDim : (model.role === "assistant" ? theme.accent : theme.warning); font.family: theme.fontMain; font.pixelSize: 13; font.weight: Font.Bold }
                            Text { text: model.time; color: theme.textFaint; font.family: theme.fontMono; font.pixelSize: 11; anchors.verticalCenter: parent.verticalCenter }
                        }
                        
                        TextEdit {
                            width: parent.width
                            text: model.text
                            color: theme.text
                            font.family: theme.fontMain
                            font.pixelSize: 14
                            wrapMode: TextEdit.Wrap
                            readOnly: true
                            selectByMouse: true
                            textFormat: TextEdit.PlainText
                            height: contentHeight
                        }
                    }
                }
                onCountChanged: Qt.callLater(() => positionViewAtEnd())
            }

            Item {
                id: inputAreaContainer
                anchors.bottom: parent.bottom; anchors.left: parent.left; anchors.right: parent.right; anchors.margins: 24; height: 52
                Rectangle {
                    anchors.fill: parent; radius: theme.radius; color: theme.bgSurface; border.color: inputArea.activeFocus ? theme.accent : theme.border; border.width: 1
                    
                    TextArea {
                        id: inputArea
                        anchors.left: parent.left; anchors.right: micButton.left; anchors.top: parent.top; anchors.bottom: parent.bottom
                        anchors.leftMargin: 16; anchors.rightMargin: 12; topPadding: 15; bottomPadding: 15; leftPadding: 0; rightPadding: 0
                        placeholderText: backend.state === "thinking" ? "EVOX is processing..." : "Type a command or question..."
                        placeholderTextColor: theme.textDim; color: theme.text; font.family: theme.fontMain; font.pixelSize: 14
                        background: null; wrapMode: TextArea.Wrap; enabled: backend.state === "idle"
                        Keys.onPressed: (event) => { if (event.key === Qt.Key_Return && !(event.modifiers & Qt.ShiftModifier)) { event.accepted = true; sendMessage(); } }
                    }

                    Rectangle {
                        id: micButton
                        anchors.right: sendButton.left
                        anchors.rightMargin: 8
                        anchors.verticalCenter: parent.verticalCenter
                        width: 36; height: 36; radius: theme.radiusSm
                        color: backend.isListening ? theme.danger : theme.bgNav
                        border.color: backend.isListening ? theme.danger : theme.border
                        border.width: 1
                        Text { anchors.centerIn: parent; text: "🎤"; font.pixelSize: 16; opacity: backend.state === "idle" ? 1.0 : 0.5 }
                        MouseArea { 
                            anchors.fill: parent
                            cursorShape: Qt.PointingHandCursor
                            enabled: backend.state === "idle"
                            onClicked: {
                                if (backend.isListening) { backend.stopListening() } else { backend.startListening() }
                            }
                        }
                    }

                    Rectangle {
                        id: sendButton
                        anchors.right: parent.right; anchors.rightMargin: 8; anchors.verticalCenter: parent.verticalCenter
                        width: 70; height: 36; radius: theme.radiusSm
                        color: backend.state === "idle" ? (sendMouse.containsMouse ? theme.accent : theme.bgNav) : "transparent"
                        Text { anchors.centerIn: parent; text: "Send"; color: sendMouse.containsMouse && backend.state === "idle" ? theme.bg : (backend.state === "idle" ? theme.text : theme.textFaint); font.family: theme.fontMain; font.pixelSize: 13; font.weight: Font.DemiBold }
                        MouseArea { id: sendMouse; anchors.fill: parent; hoverEnabled: true; enabled: backend.state === "idle"; cursorShape: Qt.PointingHandCursor; onClicked: sendMessage() }
                    }
                }
            }
            Connections {
                target: backend
                function onHistoryReloaded() { loadHistory() }
                function onResponseChunk(chunk) { if (chatModel.count > 0 && chatModel.get(chatModel.count - 1).role === "assistant") { const last = chatModel.count - 1; const prev = chatModel.get(last).text; chatModel.setProperty(last, "text", prev + chunk) } }
                function onResponseFinished(fullText) { if (chatModel.count > 0 && chatModel.get(chatModel.count - 1).role === "assistant") chatModel.setProperty(chatModel.count - 1, "text", fullText) }
                function onSystemMessageAdded(msg) { chatModel.append({ role: "system", text: msg, time: Qt.formatTime(new Date(), "HH:mm") }) }
                function onTextRecognized(text) { inputArea.text = text; inputArea.forceActiveFocus() }
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
    }

    Component {
        id: projectsView
        Item {
            ColumnLayout {
                anchors.fill: parent; anchors.margins: 32; spacing: 24
                Text { text: "Projects"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 24; font.weight: Font.DemiBold }
                Text { text: "Manage your codebases and development environments."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 14 }
                Rectangle {
                    Layout.fillWidth: true; Layout.fillHeight: true
                    color: theme.bgSurface; radius: theme.radius; border.color: theme.border
                    ColumnLayout {
                        anchors.centerIn: parent
                        Text { text: "No projects found"; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 16; Layout.alignment: Qt.AlignHCenter }
                        Text { text: "Ask EVOX to create a new project for you."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 13; Layout.alignment: Qt.AlignHCenter; Layout.topMargin: 8 }
                    }
                }
            }
        }
    }

    Component {
        id: memoryView
        MemoryView { }
    }

    Component {
        id: filesView
        FileWorkspace { }
    }

    Component {
        id: systemView
        Item {
            ColumnLayout {
                anchors.fill: parent; anchors.margins: 32; spacing: 24
                Text { text: "System Analysis"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 24; font.weight: Font.DemiBold }
                Text { text: "Live hardware diagnostics."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 14 }
                RowLayout {
                    Layout.fillWidth: true; spacing: 16
                    Rectangle {
                        Layout.fillWidth: true; height: 100; color: theme.bgSurface; radius: theme.radius; border.color: theme.border
                        ColumnLayout {
                            anchors.centerIn: parent
                            Text { text: "CPU LOAD"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; Layout.alignment: Qt.AlignHCenter }
                            Text { text: Math.round(backend.cpuPercent) + " %"; color: theme.accent; font.family: theme.fontMono; font.pixelSize: 28; Layout.alignment: Qt.AlignHCenter }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true; height: 100; color: theme.bgSurface; radius: theme.radius; border.color: theme.border
                        ColumnLayout {
                            anchors.centerIn: parent
                            Text { text: "MEMORY"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; Layout.alignment: Qt.AlignHCenter }
                            Text { text: Math.round(backend.ramPercent) + " %"; color: theme.accent; font.family: theme.fontMono; font.pixelSize: 28; Layout.alignment: Qt.AlignHCenter }
                        }
                    }
                    Rectangle {
                        Layout.fillWidth: true; height: 100; color: theme.bgSurface; radius: theme.radius; border.color: theme.border
                        ColumnLayout {
                            anchors.centerIn: parent
                            Text { text: "GPU LOAD"; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 10; font.weight: Font.Bold; Layout.alignment: Qt.AlignHCenter }
                            Text { text: Math.round(backend.gpuPercent) + " %"; color: theme.accent; font.family: theme.fontMono; font.pixelSize: 28; Layout.alignment: Qt.AlignHCenter }
                        }
                    }
                }
                Rectangle {
                    Layout.fillWidth: true; Layout.fillHeight: true
                    color: theme.bgSurface; radius: theme.radius; border.color: theme.border
                    ColumnLayout {
                        anchors.centerIn: parent
                        Text { text: "Detailed Analysis"; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 16 }
                        Text { text: "Ask EVOX in the Assistant tab to 'Analyze my system' for a full report."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 13; Layout.topMargin: 8 }
                    }
                }
            }
        }
    }

    Connections {
        target: backend
        function onConfirmRequested(programName) {
            appWindow.pendingProgram = programName
            appWindow.confirmCountdown = 120
            confirmPopup.open()
        }
        function onConfirmCancelled() {
            confirmPopup.close()
        }
    }
}