import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Item {
    id: root
    Theme { id: theme }
    
    // Startet im Benutzerordner (z.B. C:/Users/alexa)
    property string currentPath: backend.getHomeDirectory()
    property var files: backend.listDirectory(currentPath)

    function refresh() {
        files = backend.listDirectory(currentPath)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 16

        // Header
        RowLayout {
            Layout.fillWidth: true
            Text { 
                text: "File Workspace"
                color: theme.text
                font.family: theme.fontMain
                font.pixelSize: 24
                font.weight: Font.DemiBold 
            }
            Item { Layout.fillWidth: true }
        }

        // Pfad-Leiste
        Rectangle {
            Layout.fillWidth: true
            height: 40
            color: theme.bgSurface
            radius: theme.radiusSm
            border.color: theme.border
            border.width: 1

            RowLayout {
                anchors.fill: parent
                anchors.margins: 8
                
                Text {
                    text: "PATH:"
                    color: theme.textDim
                    font.family: theme.fontMono
                    font.pixelSize: 11
                    font.weight: Font.Bold
                }
                Text {
                    Layout.fillWidth: true
                    text: root.currentPath.replace(/\//g, " \\ ")
                    color: theme.text
                    font.family: theme.fontMono
                    font.pixelSize: 12
                    elide: Text.ElideLeft
                }
            }
        }

        // Datei-Liste
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: theme.bgSurface
            radius: theme.radius
            border.color: theme.border
            border.width: 1
            clip: true

            ListView {
                anchors.fill: parent
                anchors.margins: 8
                clip: true
                spacing: 2
                model: root.files

                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded }

                delegate: Rectangle {
                    width: ListView.view.width
                    height: 36
                    radius: theme.radiusSm
                    color: mouseArea.containsMouse ? theme.bgNav : "transparent"

                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 12
                        spacing: 12

                        Text {
                            text: modelData.is_dir ? "📁" : "📄"
                            font.pixelSize: 16
                        }
                        Text {
                            Layout.fillWidth: true
                            text: modelData.name
                            color: theme.text
                            font.family: theme.fontMain
                            font.pixelSize: 13
                        }
                        Text {
                            visible: !modelData.is_dir
                            text: (modelData.size / 1024).toFixed(1) + " KB"
                            color: theme.textDim
                            font.family: theme.fontMono
                            font.pixelSize: 11
                        }
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onDoubleClicked: {
                            if (modelData.is_dir) {
                                root.currentPath = modelData.path
                                root.refresh()
                            } else {
                                // Öffnen der Datei (falls EVOX das unterstützt)
                                backend.sendMessage("Open the file: " + modelData.path)
                            }
                        }
                    }
                }
            }
        }
    }
}