import QtQuick
import QtQuick.Shapes

/*
Der animierte KI-Kern.
Reagiert über `state` auf die Backend-Zustände.
Interne Phase läuft kontinuierlich; `pulseSpeed` wird pro State
unterschiedlich gesetzt und weich animiert.
*/
Item {
    id: root

    property color  accentColor: "#ff5e1a"
    property color  goldColor:   "#ffb347"
    property string state:       "idle"

    // Kontinuierliche Phase
    property real phase:      0
    property real pulseSpeed: 1.0

    Behavior on pulseSpeed {
        NumberAnimation { duration: 700; easing.type: Easing.OutCubic }
    }

    // States – steuern die Animationsintensität
    states: [
        State { name: "idle";      PropertyChanges { target: root; pulseSpeed: 1.0 } },
        State { name: "thinking";  PropertyChanges { target: root; pulseSpeed: 2.6 } },
        State { name: "speaking";  PropertyChanges { target: root; pulseSpeed: 2.0 } },
        State { name: "listening"; PropertyChanges { target: root; pulseSpeed: 1.8 } },
        State { name: "error";     PropertyChanges { target: root; pulseSpeed: 0.4 } }
    ]

    // Taktgeber ~60 fps
    Timer {
        interval: 16
        running:  true
        repeat:   true
        onTriggered: root.phase = (root.phase + root.pulseSpeed * 0.016) % (Math.PI * 2)
    }

    // Abgeleitete Rotationen (in Grad) für die Ringe
    readonly property real rot1: (root.phase * 15) % 360
    readonly property real rot2: (-root.phase * 26) % 360
    readonly property real rot3: (root.phase * 40) % 360
    readonly property real rot4: (-root.phase * 58) % 360

    // Puls des Kerns
    readonly property real corePulse: 1.0 + Math.sin(root.phase * 2.0) * 0.045

    // ---------- Äußerer Glow -------------------------------------------
    Shape {
        id: glowShape
        anchors.centerIn: parent
        width:  root.width * 0.95
        height: width

        ShapePath {
            strokeWidth: 0
            fillGradient: RadialGradient {
                centerX: glowShape.width / 2
                centerY: glowShape.height / 2
                centerRadius: glowShape.width / 2
                focalX: glowShape.width / 2
                focalY: glowShape.height / 2
                GradientStop { position: 0.0; color: Qt.rgba(1.0, 0.37, 0.10, 0.30) }
                GradientStop { position: 0.45; color: Qt.rgba(1.0, 0.37, 0.10, 0.09) }
                GradientStop { position: 1.0; color: Qt.rgba(1.0, 0.37, 0.10, 0.0) }
            }
            PathAngleArc {
                centerX: glowShape.width / 2
                centerY: glowShape.height / 2
                radiusX: glowShape.width / 2
                radiusY: glowShape.height / 2
                startAngle: 0
                sweepAngle: 360
            }
        }
    }

    // ---------- Ring 4 (außen, fein) -----------------------------------
    HudRing {
        anchors.centerIn: parent
        width:  root.width * 0.86
        height: width
        rotation: root.rot4
        dashCount:   72
        dashSweep:   2
        ringWidth:   1
        ringColor:   root.accentColor
        ringOpacity: 0.35
    }

    // ---------- Ring 3 --------------------------------------------------
    HudRing {
        anchors.centerIn: parent
        width:  root.width * 0.72
        height: width
        rotation: root.rot3
        dashCount:   48
        dashSweep:   4
        ringWidth:   1.2
        ringColor:   root.accentColor
        ringOpacity: 0.65
    }

    // ---------- Sweep-Bogen (einzelner langer Bogen) -------------------
    Shape {
        id: sweepShape
        anchors.centerIn: parent
        width:  root.width * 0.60
        height: width
        rotation: root.rot1

        ShapePath {
            strokeColor: root.goldColor
            strokeWidth: 1.6
            fillColor:   "transparent"
            capStyle:    ShapePath.RoundCap
            PathAngleArc {
                centerX:    sweepShape.width / 2
                centerY:    sweepShape.height / 2
                radiusX:    sweepShape.width / 2 - 1
                radiusY:    sweepShape.height / 2 - 1
                startAngle: 0
                sweepAngle: 38
            }
        }
    }

    // ---------- Ring 2 --------------------------------------------------
    HudRing {
        anchors.centerIn: parent
        width:  root.width * 0.48
        height: width
        rotation: root.rot2
        dashCount:   32
        dashSweep:   6
        ringWidth:   1.5
        ringColor:   root.goldColor
        ringOpacity: 0.85
    }

    // ---------- Ring 1 (innen) -----------------------------------------
    HudRing {
        anchors.centerIn: parent
        width:  root.width * 0.34
        height: width
        rotation: root.rot1
        dashCount:   20
        dashSweep:   10
        ringWidth:   2
        ringColor:   root.accentColor
        ringOpacity: 1.0
    }

    // ---------- Zentraler Kern -----------------------------------------
    Shape {
        id: coreShape
        anchors.centerIn: parent
        width:  root.width * 0.20 * root.corePulse
        height: width

        ShapePath {
            strokeWidth: 0
            fillGradient: RadialGradient {
                centerX: coreShape.width / 2
                centerY: coreShape.height / 2
                centerRadius: coreShape.width / 2
                focalX: coreShape.width / 2
                focalY: coreShape.height / 2
                GradientStop { position: 0.00; color: "#fff6de" }
                GradientStop { position: 0.30; color: root.goldColor }
                GradientStop { position: 0.75; color: root.accentColor }
                GradientStop { position: 1.00; color: "#5a1600" }
            }
            PathAngleArc {
                centerX: coreShape.width / 2
                centerY: coreShape.height / 2
                radiusX: coreShape.width / 2
                radiusY: coreShape.height / 2
                startAngle: 0
                sweepAngle: 360
            }
        }
    }
}