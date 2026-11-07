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
    title: "J.A.R.V.I.S."

    Theme { id: theme }

    property string activeTab: "dashboard"
    property string pendingProgram: ""

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#08080b" }
            GradientStop { position: 0.55; color: "#100a08" }
            GradientStop { position: 1.0; color: "#08080b" }
        }
    }

    // ---------- Top-Bar ----------------------------------------------
    Item {
        id: topBar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: 66

        Row {
            anchors.left: parent.left
            anchors.leftMargin: 28
            anchors.verticalCenter: parent.verticalCenter
            spacing: 14

            Rectangle {
                width: 10; height: 10; radius: 5
                color: backend.ollamaOk ? theme.ok : theme.danger
                anchors.verticalCenter: parent.verticalCenter
                SequentialAnimation on opacity {
                    running: true; loops: Animation.Infinite
                    NumberAnimation { to: 0.4; duration: 900 }
                    NumberAnimation { to: 1.0; duration: 900 }
                }
            }
            Text {
                text: "J.A.R.V.I.S."
                color: theme.text
                font.family: theme.fontMain
                font.pixelSize: 20
                font.weight: Font.DemiBold
                font.letterSpacing: 4
                anchors.verticalCenter: parent.verticalCenter
            }
            Text {
                text: "· " + backend.modelName
                color: theme.textFaint
                font.family: theme.fontMono
                font.pixelSize: 11
                anchors.verticalCenter: parent.verticalCenter
                anchors.verticalCenterOffset: 1
            }
        }

        Row {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            spacing: 6
            NavTab {
                theme: theme
                label: "DASHBOARD"
                active: appWindow.activeTab === "dashboard"
                onClicked: appWindow.activeTab = "dashboard"
            }
            NavTab {
                theme: theme
                label: "GEDÄCHTNIS"
                active: appWindow.activeTab === "memory"
                badge: backend.memoryCount
                onClicked: appWindow.activeTab = "memory"
            }
        }

        Column {
            anchors.right: parent.right
            anchors.rightMargin: 28
            anchors.verticalCenter: parent.verticalCenter
            spacing: 0
            Text {
                text: backend.currentTime
                color: theme.text
                font.family: theme.fontMono
                font.pixelSize: 18
                font.letterSpacing: 2
                anchors.right: parent.right
            }
            Text {
                text: backend.currentDate
                color: theme.textDim
                font.family: theme.fontMono
                font.pixelSize: 10
                font.letterSpacing: 1.2
                anchors.right: parent.right
            }
        }

        Rectangle {
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            height: 1
            color: theme.border
        }
    }

    DashboardView {
        id: dashboardView
        anchors.top: topBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        theme: theme
        visible: appWindow.activeTab === "dashboard"
    }

    MemoryView {
        id: memoryView
        anchors.top: topBar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        theme: theme
        visible: appWindow.activeTab === "memory"
    }

    // ---------- SICHERHEITS-POPUP ------------------------------------
    Rectangle {
        id: confirmPopup
        anchors.fill: parent
        color: Qt.rgba(0, 0, 0, 0.7)
        visible: false
        z: 1000

        MouseArea { anchors.fill: parent } // Blockiert Klicks auf den Hintergrund

        Rectangle {
            anchors.centerIn: parent
            width: 500
            height: 240
            radius: theme.radius
            color: theme.bgCard
            border.color: theme.danger
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 16

                Text {
                    text: "SICHERHEITSWARNUNG"
                    color: theme.danger
                    font.family: theme.fontMono
                    font.pixelSize: 14
                    font.weight: Font.Bold
                    font.letterSpacing: 2
                    Layout.alignment: Qt.AlignHCenter
                }

                Text {
                    text: "Möchtest du wirklich das Programm '" + appWindow.pendingProgram + "' deinstallieren?"
                    color: theme.text
                    font.family: theme.fontMain
                    font.pixelSize: 15
                    wrapMode: Text.Wrap
                    horizontalAlignment: Text.AlignHCenter
                    Layout.fillWidth: true
                }

                Item { Layout.fillHeight: true }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12

                    Button {
                        text: "ABBRECHEN"
                        Layout.fillWidth: true
                        onClicked: {
                            confirmPopup.visible = false
                            backend.respondToConfirmation(false)
                        }
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
                            font.pixelSize: 11
                            font.letterSpacing: 1.5
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        implicitHeight: 40
                    }

                    Button {
                        text: "BESTÄTIGEN"
                        Layout.fillWidth: true
                        onClicked: {
                            confirmPopup.visible = false
                            backend.respondToConfirmation(true)
                        }
                        background: Rectangle {
                            radius: theme.radiusSm
                            color: parent.down ? "#ff5e1a" : "#a83a0e"
                            border.color: theme.danger
                            border.width: 1
                        }
                        contentItem: Text {
                            text: parent.text
                            color: "#fff"
                            font.family: theme.fontMono
                            font.pixelSize: 11
                            font.weight: Font.Bold
                            font.letterSpacing: 1.5
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        implicitHeight: 40
                    }
                }
            }
        }
    }

    // ---------- Verbindungen -----------------------------------------
    Connections {
        target: backend
        function onConfirmRequested(programName) {
            appWindow.pendingProgram = programName
            confirmPopup.visible = true
        }
    }
}