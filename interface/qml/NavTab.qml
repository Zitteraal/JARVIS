import QtQuick

Rectangle {
    id: tab

    property QtObject theme
    property string  label: ""
    property bool    active: false
    property int     badge: 0
    signal clicked()

    implicitWidth:  contentRow.implicitWidth + 32
    implicitHeight: 32
    radius:         4
    color:          active ? theme.bgCardHi : "transparent"
    border.color:   active ? theme.accentDim : "transparent"
    border.width:   1

    Behavior on color { ColorAnimation { duration: 150 } }

    Row {
        id: contentRow
        anchors.centerIn: parent
        spacing: 8

        Text {
            text: tab.label
            color: tab.active ? theme.gold : theme.textDim
            font.family: theme.fontMono
            font.pixelSize: 10
            font.letterSpacing: 1.6
            font.weight: Font.DemiBold
            anchors.verticalCenter: parent.verticalCenter
        }

        Rectangle {
            visible: tab.badge > 0
            width: badgeText.implicitWidth + 10
            height: 16
            radius: 8
            color: theme.accentDim
            anchors.verticalCenter: parent.verticalCenter
            Text {
                id: badgeText
                anchors.centerIn: parent
                text: tab.badge
                color: theme.gold
                font.family: theme.fontMono
                font.pixelSize: 9
                font.weight: Font.Bold
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: tab.clicked()
    }
}