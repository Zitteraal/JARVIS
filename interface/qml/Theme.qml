import QtQuick

QtObject {
    // Farbpalette (Exakt nach Vorgabe)
    readonly property color bg:          "#0B1011" // Deep Graphite
    readonly property color bgNav:       "#141C1A" // Command Panel
    readonly property color bgSurface:   "#1C2722" // Elevated Surface

    readonly property color accent:      "#B7F36B" // Signal Lime
    readonly property color accentDim:   "#788875" // Tactical Olive

    readonly property color text:        "#E5EBE5" // Soft White
    readonly property color textDim:     "#8B9790" // Muted Gray
    readonly property color textFaint:   "#4a544f"

    readonly property color warning:     "#F2B84B" // Warning Amber
    readonly property color danger:      "#E85B5B" // Critical Red

    readonly property color border:      "#1f2b26"
    readonly property color borderHi:    "#2d3d36"

    // Typografie (Inter & JetBrains Mono Fallbacks)
    readonly property string fontMain:   "Segoe UI" // Fallback für Inter
    readonly property string fontMono:   "Consolas" // Fallback für JetBrains Mono

    // Geometrie (Minimalistisch, keine Pill-Shapes)
    readonly property int radius:        4
    readonly property int radiusSm:      2
}