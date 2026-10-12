import AppKit

// Veylo case-study images from iPhone 17 Pro simulator screenshots (1206 × 2622):
//   device-<name>.png  — the screen in a drawn phone frame, 1470 × 3000 (the same canvas and screen
//                        rectangle as the Numi device images, so the case-page CSS applies unchanged)
//   cover.png          — two framed screens on a pale blue ground, 1340 × 1174 (homepage cover size)
//
//   swift scripts/compose-veylo-images.swift <screens-dir> <output-dir> <cover-left> <cover-right> <name> [name ...]
// Reads <screens-dir>/<name>.png. Encode to WebP afterwards (cwebp -q 90).

let args = CommandLine.arguments
guard args.count >= 6 else {
    fputs("Usage: compose-veylo-images.swift <screens-dir> <output-dir> <cover-left> <cover-right> <name> [name ...]\n", stderr)
    exit(1)
}
let screens = URL(fileURLWithPath: args[1], isDirectory: true)
let output = URL(fileURLWithPath: args[2], isDirectory: true)
let coverNames = (args[3], args[4])
let names = Array(args.dropFirst(5))
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)

let deviceSize = NSSize(width: 1470, height: 3000)
let screenRect = NSRect(x: 75, y: 66, width: 1320, height: 2868)

func bitmap(_ size: NSSize) -> NSBitmapImageRep {
    NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(size.width), pixelsHigh: Int(size.height),
                     bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                     colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
}

func write(_ rep: NSBitmapImageRep, _ name: String) {
    let url = output.appendingPathComponent(name)
    try! rep.representation(using: .png, properties: [:])!.write(to: url)
    print("wrote \(url.path)")
}

/// A phone: titanium band, black border, the screenshot with rounded corners.
func drawDevice(_ screen: NSImage, in rect: NSRect) {
    let s = rect.width / deviceSize.width
    let outer = NSBezierPath(roundedRect: rect, xRadius: 236 * s, yRadius: 236 * s)
    NSGradient(colors: [NSColor(calibratedWhite: 0.36, alpha: 1), NSColor(calibratedWhite: 0.18, alpha: 1),
                        NSColor(calibratedWhite: 0.30, alpha: 1)])!.draw(in: outer, angle: -60)
    let band = rect.insetBy(dx: 9 * s, dy: 9 * s)
    NSColor(calibratedWhite: 0.04, alpha: 1).setFill()
    NSBezierPath(roundedRect: band, xRadius: 228 * s, yRadius: 228 * s).fill()
    let sr = NSRect(x: rect.minX + screenRect.minX * s, y: rect.minY + screenRect.minY * s,
                    width: screenRect.width * s, height: screenRect.height * s)
    NSGraphicsContext.saveGraphicsState()
    NSBezierPath(roundedRect: sr, xRadius: 172 * s, yRadius: 172 * s).addClip()
    screen.draw(in: sr, from: .zero, operation: .sourceOver, fraction: 1)
    NSGraphicsContext.restoreGraphicsState()
}

func load(_ name: String) -> NSImage {
    guard let img = NSImage(contentsOf: screens.appendingPathComponent(name + ".png")) else {
        fputs("cannot read \(name).png\n", stderr)
        exit(1)
    }
    return img
}

for name in names {
    let rep = bitmap(deviceSize)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
    drawDevice(load(name), in: NSRect(origin: .zero, size: deviceSize))
    NSGraphicsContext.restoreGraphicsState()
    write(rep, "device-\(name).png")
}

// Cover: two phones, the right one a little higher, soft shadows, pale blue (the app icon's blue, quiet).
let coverSize = NSSize(width: 1340, height: 1174)
let rep = bitmap(coverSize)
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSColor(calibratedRed: 0.890, green: 0.918, blue: 0.949, alpha: 1).setFill()
NSRect(origin: .zero, size: coverSize).fill()
let h: CGFloat = 1010
let w = h * deviceSize.width / deviceSize.height
for (i, name) in [coverNames.0, coverNames.1].enumerated() {
    let x: CGFloat = i == 0 ? 670 - w - 26 : 670 + 26
    let y: CGFloat = i == 0 ? 52 : 112
    NSGraphicsContext.saveGraphicsState()
    let shadow = NSShadow()
    shadow.shadowColor = NSColor(calibratedRed: 0.06, green: 0.11, blue: 0.12, alpha: 0.22)
    shadow.shadowBlurRadius = 46
    shadow.shadowOffset = NSSize(width: 0, height: -22)
    shadow.set()
    NSColor.black.setFill()
    NSBezierPath(roundedRect: NSRect(x: x, y: y, width: w, height: h), xRadius: 236 * w / deviceSize.width,
                 yRadius: 236 * w / deviceSize.width).fill()
    NSGraphicsContext.restoreGraphicsState()
    drawDevice(load(name), in: NSRect(x: x, y: y, width: w, height: h))
}
NSGraphicsContext.restoreGraphicsState()
write(rep, "cover.png")
