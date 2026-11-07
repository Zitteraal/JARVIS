import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property string buttonText: ""
    property bool active: false
    signal clicked()
    
    Layout.fillWidth: true
    height: 32
    color: active ? theme.bgSurface : "transparent"
    radius: theme.radiusSm
    
    Text {
        anchors.left: parent.left
        anchors.leftMargin: 12
        anchors.verticalCenter: parent.verticalCenter
        text: root.buttonText
        color: root.active ? theme.accent : theme.textDim
        font.family: theme.fontMain
        font.pixelSize: 13
        font.weight: root.active ? Font.Medium : Font.Normal
    }
    MouseArea { 
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor
        onClicked: root.clicked() 
    }
}