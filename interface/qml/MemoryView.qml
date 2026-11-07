import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

Item {
    id: root
    property QtObject theme
    property string filter: "all"

    // Farbzuordnung pro Kategorie
    function categoryColor(cat) {
        switch (cat) {
            case "personal":    return theme.gold
            case "preference":  return theme.accent
            case "project":     return theme.info
            case "task":        return theme.warning
            case "instruction": return theme.danger
            default:            return theme.textDim
        }
    }
    function categoryLabel(cat) {
        switch (cat) {
            case "personal":    return "PERSÖNLICH"
            case "preference":  return "VORLIEBE"
            case "project":     return "PROJEKT"
            case "task":        return "AUFGABE"
            case "instruction": return "ANWEISUNG"
            default:            return cat.toUpperCase()
        }
    }

    // sichtbare Liste (gefiltert)
    property var visibleMemories: {
        const all = backend.memories
        if (filter === "all") return all
        return all.filter(m => m.category === filter)
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 32
        spacing: 16

        // Kopfzeile
        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            Column {
                Layout.fillWidth: true
                spacing: 2
                Text {
                    text: "GEDÄCHTNIS"
                    color: theme.text
                    font.family: theme.fontMono
                    font.pixelSize: 18
                    font.letterSpacing: 4
                    font.weight: Font.DemiBold
                }
                Text {
                    text: backend.memoryCount + " dauerhafte Erinnerungen · werden automatisch aus Gesprächen extrahiert"
                    color: theme.textDim
                    font.family: theme.fontMain
                    font.pixelSize: 12
                }
            }
        }

        // Filter-Chips
        Flow {
            Layout.fillWidth: true
            spacing: 8

            Repeater {
                model: [
                    { key: "all",         label: "ALLE" },
                    { key: "personal",    label: "PERSÖNLICH" },
                    { key: "preference",  label: "VORLIEBEN" },
                    { key: "project",     label: "PROJEKTE" },
                    { key: "task",        label: "AUFGABEN" },
                    { key: "instruction", label: "ANWEISUNGEN" }
                ]
                delegate: Rectangle {
                    property bool isActive: root.filter === modelData.key
                    width:  chipText.implicitWidth + 24
                    height: 28
                    radius: 4
                    color:        isActive ? theme.bgCardHi : "transparent"
                    border.color: isActive ? theme.accentDim : theme.border
                    border.width: 1

                    Text {
                        id: chipText
                        anchors.centerIn: parent
                        text: modelData.label
                        color: isActive ? theme.gold : theme.textDim
                        font.family: theme.fontMono
                        font.pixelSize: 10
                        font.letterSpacing: 1.4
                        font.weight: Font.DemiBold
                    }
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: root.filter = modelData.key
                    }
                }
            }
        }

        // Liste
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: theme.radius
            color: theme.bgCard
            border.color: theme.border
            border.width: 1
            clip: true

            // Empty state
            Column {
                anchors.centerIn: parent
                visible: root.visibleMemories.length === 0
                spacing: 8
                Text {
                    text: "◌"
                    color: theme.textFaint
                    font.pixelSize: 48
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Text {
                    text: root.filter === "all"
                        ? "Noch keine Erinnerungen gespeichert."
                        : "Keine Einträge in dieser Kategorie."
                    color: theme.textDim
                    font.family: theme.fontMain
                    font.pixelSize: 13
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Text {
                    text: "Erzähle J.A.R.V.I.S. etwas über dich – er merkt es sich."
                    color: theme.textFaint
                    font.family: theme.fontMain
                    font.pixelSize: 11
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }

            ListView {
                id: memList
                anchors.fill: parent
                anchors.margins: 12
                clip: true
                spacing: 8
                model: root.visibleMemories

                ScrollBar.vertical: ScrollBar {
                    policy: ScrollBar.AsNeeded
                    width: 6
                }

                delegate: Rectangle {
                    id: memItem
                    width: memList.width
                    height: itemContent.implicitHeight + 24
                    radius: theme.radiusSm
                    color: theme.bgCardHi
                    border.color: theme.border
                    border.width: 1

                    property bool editing: false

                    ColumnLayout {
                        id: itemContent
                        anchors.fill: parent
                        anchors.margins: 12
                        spacing: 6

                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 10

                            Rectangle {
                                width:  catLabel.implicitWidth + 14
                                height: 18
                                radius: 3
                                color:  Qt.rgba(
                                    root.categoryColor(modelData.category).r,
                                    root.categoryColor(modelData.category).g,
                                    root.categoryColor(modelData.category).b,
                                    0.15)
                                border.color: root.categoryColor(modelData.category)
                                border.width: 1
                                Text {
                                    id: catLabel
                                    anchors.centerIn: parent
                                    text: root.categoryLabel(modelData.category)
                                    color: root.categoryColor(modelData.category)
                                    font.family: theme.fontMono
                                    font.pixelSize: 9
                                    font.letterSpacing: 1.2
                                    font.weight: Font.DemiBold
                                }
                            }
                            Text {
                                text: modelData.source === "auto" ? "auto" : "manuell"
                                color: theme.textFaint
                                font.family: theme.fontMono
                                font.pixelSize: 9
                                font.letterSpacing: 1
                            }
                            Text {
                                text: modelData.created_at
                                color: theme.textFaint
                                font.family: theme.fontMono
                                font.pixelSize: 9
                            }
                            Item { Layout.fillWidth: true }

                            // Bearbeiten-Icon
                            Rectangle {
                                width: 24; height: 24; radius: 3
                                color: editMouse.containsMouse ? theme.bgCard : "transparent"
                                Text {
                                    anchors.centerIn: parent
                                    text: memItem.editing ? "✕" : "✎"
                                    color: theme.textDim
                                    font.pixelSize: 13
                                }
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

                            // Löschen-Icon
                            Rectangle {
                                width: 24; height: 24; radius: 3
                                color: delMouse.containsMouse ? "#2a0e0c" : "transparent"
                                Text {
                                    anchors.centerIn: parent
                                    text: "🗑"
                                    color: delMouse.containsMouse ? theme.danger : theme.textDim
                                    font.pixelSize: 12
                                }
                                MouseArea {
                                    id: delMouse
                                    anchors.fill: parent
                                    hoverEnabled: true
                                    cursorShape: Qt.PointingHandCursor
                                    onClicked: backend.deleteMemory(modelData.id)
                                }
                            }
                        }

                        // Anzeige-Modus
                        Text {
                            Layout.fillWidth: true
                            visible: !memItem.editing
                            text: modelData.content
                            color: theme.text
                            font.family: theme.fontMain
                            font.pixelSize: 13
                            wrapMode: Text.Wrap
                        }

                        // Edit-Modus
                        RowLayout {
                            Layout.fillWidth: true
                            visible: memItem.editing
                            spacing: 8

                            Rectangle {
                                Layout.fillWidth: true
                                height: 34
                                radius: 3
                                color: "#0c0c10"
                                border.color: theme.accentDim
                                border.width: 1

                                TextArea {
                                    id: editField
                                    anchors.fill: parent
                                    anchors.margins: 6
                                    topPadding: 0
                                    bottomPadding: 0
                                    leftPadding: 0
                                    rightPadding: 0
                                    color: theme.text
                                    font.family: theme.fontMain
                                    font.pixelSize: 12
                                    background: null
                                    wrapMode: TextArea.Wrap
                                }
                            }

                            Rectangle {
                                width: 60; height: 34; radius: 3
                                color: saveMouse.containsMouse ? theme.accent : theme.accentDim
                                Text {
                                    anchors.centerIn: parent
                                    text: "SPEICHERN"
                                    color: "#1a0a02"
                                    font.family: theme.fontMono
                                    font.pixelSize: 9
                                    font.weight: Font.Bold
                                    font.letterSpacing: 1
                                }
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