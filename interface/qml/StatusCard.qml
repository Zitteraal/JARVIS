import QtQuick
import QtQuick.Layouts

Rectangle {
    id: card

    property QtObject theme
    property string label:       ""
    property string value:       ""
    property color  valueColor:  "#eae6df"
    property color  accentBar:   "#ff5e1a"

    implicitHeight: 62
    radius: theme.radius
    color: theme.bgCard
    border.color: theme.border
    border.width: 1

    Rectangle {
        anchors.left:           parent.left
        anchors.top:            parent.top
        anchors.bottom:         parent.bottom
        anchors.topMargin:      10
        anchors.bottomMargin:   10
        width:                  2
        radius:                 1
        color:                  card.accentBar
    }

    ColumnLayout {
        anchors.fill:            parent
        anchors.leftMargin:      18
        anchors.rightMargin:     14
        anchors.topMargin:       10
        anchors.bottomMargin:    10
        spacing:                 2

        Text {
            text: card.label.toUpperCase()
            color: theme.textDim
            font.family: theme.fontMono
            font.pixelSize: 10
            font.letterSpacing: 1.4
        }

        Text {
            text: card.value
            color: card.valueColor
            font.family: theme.fontMain
            font.pixelSize: 15
            font.weight: Font.Medium
            elide: Text.ElideRight
            Layout.fillWidth: true
        }
    }
}