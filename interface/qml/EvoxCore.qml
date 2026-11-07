import QtQuick
import QtQuick.Shapes

Item {
    id: root
    property color accentColor: "#D1F864"
    property string state: "idle"

    property real phase: 0
    property real pulseSpeed: 1.0

    Behavior on pulseSpeed {
        NumberAnimation { duration: 700; easing.type: Easing.OutCubic }
    }

    states: [
        State { name: "idle";      PropertyChanges { target: root; pulseSpeed: 1.0 } },
        State { name: "thinking";  PropertyChanges { target: root; pulseSpeed: 3.5 } },
        State { name: "listening"; PropertyChanges { target: root; pulseSpeed: 2.0 } },
        State { name: "error";     PropertyChanges { target: root; pulseSpeed: 0.4 } }
    ]

    Timer {
        interval: 16
        running: true
        repeat: true
        onTriggered: root.phase = (root.phase + root.pulseSpeed * 0.016) % (Math.PI * 2)
    }

    // Ein sehr subtiler, flacher Kreis (kein 3D, kein Glow)
    Rectangle {
        anchors.centerIn: parent
        width: root.width * 0.8; height: width; radius: width / 2
        color: "transparent"
        border.color: root.accentColor
        border.width: 1
        opacity: 0.15
        
        // Ein einzelner innerer Punkt, der sanft pulsiert
        Rectangle {
            anchors.centerIn: parent
            width: 6 + Math.sin(root.phase) * 2
            height: width; radius: width / 2
            color: root.accentColor
        }
    }
}