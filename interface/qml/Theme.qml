import QtQuick

QtObject {
    // Hintergrund
    readonly property color bg:          "#08080b"
    readonly property color bgDeep:      "#0c0b10"
    readonly property color bgCard:      "#111017"
    readonly property color bgCardHi:    "#17161f"

    // Akzente
    readonly property color accent:      "#ff5e1a"
    readonly property color accentDim:   "#a83a0e"
    readonly property color gold:        "#ffb347"
    readonly property color info:        "#5ab0ff"
    readonly property color goldBright:  "#ffd58a"

    // Text
    readonly property color text:        "#eae6df"
    readonly property color textDim:     "#8a8078"
    readonly property color textFaint:   "#5a5048"

    // Zustände
    readonly property color ok:          "#4fd48a"
    readonly property color warning:     "#ffb347"
    readonly property color danger:      "#ff4b3e"

    // Rahmen
    readonly property color border:      "#2a1e18"
    readonly property color borderHi:    "#3d2a20"

    // Typo
    readonly property string fontMain:   "Segoe UI"
    readonly property string fontMono:   "Consolas"

    // Geometrie
    readonly property int radius:        8
    readonly property int radiusSm:      4
}