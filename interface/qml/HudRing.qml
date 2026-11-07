import QtQuick
import QtQuick.Shapes

/*
Ein Kreis aus einzelnen Dash-Segmenten. Rotiert über die
`rotation`-Property, die von außen gesetzt wird (NeuralCore).
*/
Item {
    id: ring

    property color  ringColor:   "#ff5e1a"
    property real   ringWidth:   1.5
    property int    dashCount:   36
    property real   dashSweep:   6           // Grad pro Dash
    property real   ringOpacity: 1.0

    Repeater {
        model: ring.dashCount
        delegate: Shape {
            anchors.fill: parent
            opacity: ring.ringOpacity

            ShapePath {
                strokeColor: ring.ringColor
                strokeWidth: ring.ringWidth
                fillColor:   "transparent"
                capStyle:    ShapePath.FlatCap

                PathAngleArc {
                    centerX:    ring.width / 2
                    centerY:    ring.height / 2
                    radiusX:    ring.width / 2 - ring.ringWidth
                    radiusY:    ring.height / 2 - ring.ringWidth
                    startAngle: index * (360 / ring.dashCount)
                    sweepAngle: ring.dashSweep
                }
            }
        }
    }
}