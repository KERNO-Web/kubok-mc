// Рамка круга на тёмном фоне: пиксели светлее фона (яркость > порога). swift .work/circle_bbox.swift <img> <порог 0..255>
import AppKit
let a = CommandLine.arguments
let rep = NSBitmapImageRep(data: NSImage(contentsOfFile: a[1])!.tiffRepresentation!)!
let t = Double(a[2])!
var x0 = Int.max, y0 = Int.max, x1 = 0, y1 = 0
for y in 0..<rep.pixelsHigh { for x in 0..<rep.pixelsWide {
  let c = rep.colorAt(x: x, y: y)!.usingColorSpace(.sRGB)!
  if (c.redComponent + c.greenComponent + c.blueComponent) / 3 * 255 > t { x0 = min(x0, x); y0 = min(y0, y); x1 = max(x1, x); y1 = max(y1, y) }
}}
print(rep.pixelsWide, rep.pixelsHigh, "bbox", x0, y0, x1, y1, "size", x1 - x0 + 1, y1 - y0 + 1)
