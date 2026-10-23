// Векторизация светлого логотипа на тёмном фоне через Vision (контуры) в SVG с evenodd.
// Запуск: swift .work/vectorize.swift <logo.png> <out.svg>
import Foundation
import Vision
import CoreImage

let a = CommandLine.arguments
guard a.count == 3, let img = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let w = img.extent.width, h = img.extent.height

let req = VNDetectContoursRequest()
req.contrastAdjustment = 2.0
req.detectsDarkOnLight = false
req.maximumImageDimension = 2048
try VNImageRequestHandler(ciImage: img).perform([req])
guard let obs = req.results?.first else { print("no contours"); exit(2) }

var d = ""
func add(_ c: VNContour) {
    let pts = c.normalizedPoints
    guard pts.count > 2 else { return }
    for (i, p) in pts.enumerated() {
        let x = Double(p.x) * Double(w), y = (1 - Double(p.y)) * Double(h)
        d += (i == 0 ? "M" : "L") + String(format: "%.1f %.1f", x, y)
    }
    d += "Z"
    for child in c.childContours { add(child) }
}
for c in obs.topLevelContours {
    // отбрасываем рамку изображения и мелкий шум
    let b = c.normalizedPath.boundingBox
    if b.width > 0.97 && b.height > 0.97 { for child in c.childContours { add(child) }; continue }
    if b.width * b.height < 0.0004 { continue }
    add(c)
}
let svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 \(Int(w)) \(Int(h))\"><path fill=\"#fff\" fill-rule=\"evenodd\" d=\"\(d)\"/></svg>"
try svg.write(toFile: a[2], atomically: true, encoding: .utf8)
print("ok", obs.topLevelContours.count, "contours,", d.count, "chars")
