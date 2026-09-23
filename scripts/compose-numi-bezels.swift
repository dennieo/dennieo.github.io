import AppKit

let arguments = CommandLine.arguments
guard arguments.count == 4 else {
    fputs("Usage: compose-numi-bezels.swift <bezel.png> <screens-dir> <output-dir>\n", stderr)
    exit(1)
}

let bezelURL = URL(fileURLWithPath: arguments[1])
let screensURL = URL(fileURLWithPath: arguments[2], isDirectory: true)
let outputURL = URL(fileURLWithPath: arguments[3], isDirectory: true)
let canvasSize = NSSize(width: 1470, height: 3000)
let screenRect = NSRect(x: 75, y: 66, width: 1320, height: 2868)
let fileManager = FileManager.default

guard let bezel = NSImage(contentsOf: bezelURL) else {
    fputs("Could not read bezel at \(bezelURL.path)\n", stderr)
    exit(1)
}

try fileManager.createDirectory(at: outputURL, withIntermediateDirectories: true)

let screens = [
    "meal-history",
    "home",
    "progress",
    "fasting",
]

for name in screens {
    let sourceURL = screensURL.appendingPathComponent("simulator-\(name).webp")
    let destinationURL = outputURL.appendingPathComponent("device-\(name).png")

    guard let screen = NSImage(contentsOf: sourceURL) else {
        fputs("Could not read screenshot at \(sourceURL.path)\n", stderr)
        exit(1)
    }

    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: Int(canvasSize.width),
        pixelsHigh: Int(canvasSize.height),
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ) else {
        fputs("Could not create output bitmap\n", stderr)
        exit(1)
    }

    bitmap.size = canvasSize
    NSGraphicsContext.saveGraphicsState()
    guard let context = NSGraphicsContext(bitmapImageRep: bitmap) else {
        fputs("Could not create drawing context\n", stderr)
        exit(1)
    }
    NSGraphicsContext.current = context
    context.cgContext.clear(NSRect(origin: .zero, size: canvasSize))
    context.imageInterpolation = .high
    NSGraphicsContext.saveGraphicsState()
    NSBezierPath(roundedRect: screenRect, xRadius: 165, yRadius: 165).addClip()
    screen.draw(in: screenRect, from: .zero, operation: .copy, fraction: 1)
    NSGraphicsContext.restoreGraphicsState()
    bezel.draw(
        in: NSRect(origin: .zero, size: canvasSize),
        from: .zero,
        operation: .sourceOver,
        fraction: 1
    )
    context.flushGraphics()
    NSGraphicsContext.restoreGraphicsState()

    guard let data = bitmap.representation(using: .png, properties: [:]) else {
        fputs("Could not encode \(destinationURL.lastPathComponent)\n", stderr)
        exit(1)
    }
    try data.write(to: destinationURL)
    print(destinationURL.path)
}
