import QtQuick
import QtQuick.Layouts

Rectangle {
    id: root
    property string cardTitle: ""
    property string cardDesc: ""
    property string cardIcon: ""
    signal clicked()
    
    Layout.fillWidth: true
    height: 80
    color: theme.bgSurface
    radius: theme.radius
    border.color: theme.border
    border.width: 1
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        
        Rectangle {
            width: 40
            height: 40
            radius: theme.radiusSm
            color: theme.bgNav
            Text { 
                anchors.centerIn: parent
                text: root.cardIcon
                color: theme.accent
                font.pixelSize: 20 
            }
        }
        
        ColumnLayout {
            Text { 
                text: root.cardTitle
                color: theme.text
                font.family: theme.fontMain
                font.pixelSize: 14
                font.weight: Font.Medium 
            }
            Text { 
                text: root.cardDesc
                color: theme.textDim
                font.family: theme.fontMain
                font.pixelSize: 11 
            }
        }
    }
    MouseArea { 
        anchors.fill: parent
        cursorShape: Qt.PointingHandCursor 
        onClicked: root.clicked()
    }
}