import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Item {
    id: root
    Theme { id: theme } // <--- Lädt das Design direkt selbst
    property string filter: "all"

    function categoryColor(cat) {
        switch (cat) {
            case "personal":    return theme.accent
            case "preference":  return theme.info
            case "project":     return theme.warning
            case "task":        return theme.danger
            default:            return theme.textDim
        }
    }
    
    function categoryLabel(cat) {
        return cat.toUpperCase()
    }

    property var visibleMemories: {
        const all = backend.memories
        if (filter === "all") return all
        return all.filter(m => m.category === filter)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 24

        RowLayout {
            Layout.fillWidth: true
            ColumnLayout {
                Text { text: "Memory Banks"; color: theme.text; font.family: theme.fontMain; font.pixelSize: 24; font.weight: Font.DemiBold }
                Text { text: backend.memoryCount + " permanent memories extracted from conversations."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 14 }
            }
            Item { Layout.fillWidth: true }
        }

        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: [
                    { key: "all",         label: "ALL" },
                    { key: "personal",    label: "PERSONAL" },
                    { key: "preference",  label: "PREFERENCES" },
                    { key: "project",     label: "PROJECTS" },
                    { key: "task",        label: "TASKS" },
                    { key: "instruction", label: "INSTRUCTIONS" }
                ]
                delegate: Rectangle {
                    property bool isActive: root.filter === modelData.key
                    width:  chipText.implicitWidth + 24
                    height: 32
                    radius: theme.radiusSm
                    color:        isActive ? theme.bgSurface : "transparent"
                    border.color: isActive ? theme.accent : theme.border
                    border.width: 1

                    Text {
                        id: chipText
                        anchors.centerIn: parent
                        text: modelData.label
                        color: isActive ? theme.accent : theme.textDim
                        font.family: theme.fontMain
                        font.pixelSize: 11
                        font.weight: Font.Medium
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.filter = modelData.key
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: theme.radius
            color: theme.bgSurface
            border.color: theme.border
            border.width: 1
            clip: true

            ColumnLayout {
                anchors.centerIn: parent
                visible: root.visibleMemories.length === 0
                Text { text: "No memories found."; color: theme.textFaint; font.family: theme.fontMain; font.pixelSize: 16; Layout.alignment: Qt.AlignHCenter }
                Text { text: "Tell EVOX something about yourself."; color: theme.textDim; font.family: theme.fontMain; font.pixelSize: 13; Layout.alignment: Qt.AlignHCenter; Layout.topMargin: 8 }
            }

            ListView {
                id: memList
                anchors.fill: parent
                anchors.margins: 16
                clip: true
                spacing: 12
                model: root.visibleMemories
                ScrollBar.vertical: ScrollBar { policy: ScrollBar.AsNeeded; width: 6 }

                delegate: Rectangle {
                    id: memItem
                    width: memList.width
                    height: itemContent.implicitHeight + 24
                    radius: theme.radiusSm
                    color: theme.bg
                    border.color: theme.border
                    border.width: 1

                    property bool editing: false

                    ColumnLayout {
                        id: itemContent
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 8

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10

                            Rectangle {
                                width:  catLabel.implicitWidth + 12
                                height: 20
                                radius: 3
                                color:  Qt.rgba(root.categoryColor(modelData.category).r, root.categoryColor(modelData.category).g, root.categoryColor(modelData.category).b, 0.15)
                                border.color: root.categoryColor(modelData.category)
                                border.width: 1
                                Text {
                                    id: catLabel
                                    anchors.centerIn: parent
                                    text: root.categoryLabel(modelData.category)
                                    color: root.categoryColor(modelData.category)
                                    font.family: theme.fontMain
                                    font.pixelSize: 9
                                    font.weight: Font.Bold
                                }
                            }
                            Text { text: modelData.source === "auto" ? "auto-extracted" : "manual"; color: theme.textFaint; font.family: theme.fontMono; font.pixelSize: 10 }
                            Text { text: modelData.created_at; color: theme.textFaint; font.family: theme.fontMono; font.pixelSize: 10 }
                            Item { Layout.fillWidth: true }

                            RowLayout {
                                spacing: 4
                                Rectangle {
                                    width: 24; height: 24; radius: theme.radiusSm
                                    color: editMouse.containsMouse ? theme.bgSurface : "transparent"
                                    Text { anchors.centerIn: parent; text: memItem.editing ? "✕" : "✎"; color: theme.textDim; font.pixelSize: 12 }
                                    MouseArea {
                                        id: editMouse
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: {
                                            if (memItem.editing) {
                                                memItem.editing = false
                                            } else {
                                                memItem.editing = true
                                                editField.text = modelData.content
                                                editField.forceActiveFocus()
                                            }
                                        }
                                    }
                                }
                                Rectangle {
                                    width: 24; height: 24; radius: theme.radiusSm
                                    color: delMouse.containsMouse ? Qt.rgba(0.9,0.3,0.3,0.2) : "transparent"
                                    Text { anchors.centerIn: parent; text: "🗑"; color: delMouse.containsMouse ? theme.danger : theme.textDim; font.pixelSize: 11 }
                                    MouseArea {
                                        id: delMouse
                                        anchors.fill: parent
                                        hoverEnabled: true
                                        cursorShape: Qt.PointingHandCursor
                                        onClicked: backend.deleteMemory(modelData.id)
                                    }
                                }
                            }
                        }

                        Text {
                            Layout.fillWidth: true
                            visible: !memItem.editing
                            text: modelData.content
                            color: theme.text
                            font.family: theme.fontMain
                            font.pixelSize: 13
                            wrapMode: Text.Wrap
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            visible: memItem.editing
                            spacing: 8

                            Rectangle {
                                Layout.fillWidth: true
                                height: 36
                                radius: theme.radiusSm
                                color: theme.bgSurface
                                border.color: theme.accent
                                border.width: 1
                                TextArea {
                                    id: editField
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    topPadding: 0; bottomPadding: 0; leftPadding: 0; rightPadding: 0
                                    color: theme.text
                                    font.family: theme.fontMain
                                    font.pixelSize: 13
                                    background: null
                                    wrapMode: TextArea.Wrap
                                }
                            }

                            Rectangle {
                                width: 80; height: 36; radius: theme.radiusSm
                                color: saveMouse.containsMouse ? theme.accent : theme.bgSurface
                                border.color: theme.accent
                                border.width: 1
                                Text { anchors.centerIn: parent; text: "Save"; color: saveMouse.containsMouse ? theme.bg : theme.accent; font.family: theme.fontMain; font.pixelSize: 12; font.weight: Font.Bold }
                                MouseArea {
                                    id: saveMouse
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: {
                                        backend.updateMemory(modelData.id, editField.text)
                                        memItem.editing = false
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}