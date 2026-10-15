import AppKit

// Veylo homepage cover from the framed device images: two phones on a pale blue ground, 1340 × 1174
// (homepage cover size). The phones are the same Apple bezel as the Numi and Tysha pages.
//
// 1. Frame the iPhone 17 Pro simulator screenshots (1206 × 2622, dist/img/veylo/sources) in the bezel:
//      swift scripts/compose-device-bezels.swift <bezel.png> dist/img/veylo/sources <device-dir> <name> [name ...]
// 2. The cover from two of those:
//      swift scripts/compose-veylo-images.swift <device-dir> <output-dir> <cover-left> <cover-right>
//    Reads <device-dir>/device-<name>.png, writes <output-dir>/cover.png.
// Encode to WebP afterwards (cwebp -q 90).

let args = CommandLine.arguments
guard args.count == 5 else {
    fputs("Usage: compose-veylo-images.swift <device-dir> <output-dir> <cover-left> <cover-right>\n", stderr)
    exit(1)
}
let devices = URL(fileURLWithPath: args[1], isDirectory: true)
let output = URL(fileURLWithPath: args[2], isDirectory: true)
let coverNames = (args[3], args[4])
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)

let deviceSize = NSSize(width: 1470, height: 3000)

func load(_ name: String) -> NSImage {
    guard let img = NSImage(contentsOf: devices.appendingPathComponent("device-\(name).png")) else {
        fputs("cannot read device-\(name).png\n", stderr)
        exit(1)
    }
    return img
}

// Cover: two phones, the right one a little higher, soft shadows, pale blue (quiet, from the map's water).
let coverSize = NSSize(width: 1340, height: 1174)
let rep = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: Int(coverSize.width), pixelsHigh: Int(coverSize.height),
                           bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true, isPlanar: false,
                           colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
NSGraphicsContext.saveGraphicsState()
NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: rep)
NSGraphicsContext.current?.imageInterpolation = .high
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
    load(name).draw(in: NSRect(x: x, y: y, width: w, height: h), from: .zero, operation: .sourceOver, fraction: 1)
    NSGraphicsContext.restoreGraphicsState()
}
NSGraphicsContext.restoreGraphicsState()
let url = output.appendingPathComponent("cover.png")
try! rep.representation(using: .png, properties: [:])!.write(to: url)
print("wrote \(url.path)")
