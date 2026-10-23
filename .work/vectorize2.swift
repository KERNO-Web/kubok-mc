// Чистый вектор угловатого логотипа: увеличение x4, сглаживание, порог, контуры Vision и аппроксимация
// многоугольником (прямые грани без «лесенки»). swift .work/vectorize2.swift <logo.png> <out.svg> <epsilon>
import Foundation
import Vision
import CoreImage

let a = CommandLine.arguments
guard a.count == 4, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let eps = Float(a[3])!
let s = 4.0
let big = src.applyingFilter("CILanczosScaleTransform", parameters: ["inputScale": s, "inputAspectRatio": 1.0])
    .applyingFilter("CIGaussianBlur", parameters: ["inputRadius": 3.0]).cropped(to: CGRect(x: 0, y: 0, width: src.extent.width * s, height: src.extent.height * s))
// порог: светлое → белое
let bin = big.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 6, y: 0, z: 0, w: 0), "inputGVector": CIVector(x: 6, y: 0, z: 0, w: 0),
    "inputBVector": CIVector(x: 6, y: 0, z: 0, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: -2.6, y: -2.6, z: -2.6, w: 0)]).applyingFilter("CIColorClamp")
let w = bin.extent.width, h = bin.extent.height
let ctx = CIContext()
let cg = ctx.createCGImage(bin, from: bin.extent)!

let req = VNDetectContoursRequest()
req.contrastAdjustment = 1.0
req.detectsDarkOnLight = false
req.maximumImageDimension = 4096
try VNImageRequestHandler(cgImage: cg).perform([req])
guard let obs = req.results?.first else { print("no contours"); exit(2) }

var d = ""
func add(_ c0: VNContour) {
    guard let c = try? c0.polygonApproximation(epsilon: eps) else { return }
    let pts = c.normalizedPoints
    guard pts.count > 2 else { return }
    for (i, p) in pts.enumerated() {
        d += (i == 0 ? "M" : "L") + String(format: "%.1f %.1f", Double(p.x) * Double(w) / s, (1 - Double(p.y)) * Double(h) / s)
    }
    d += "Z"
    for child in c0.childContours { add(child) }
}
for c in obs.topLevelContours {
    let b = c.normalizedPath.boundingBox
    if b.width > 0.97 && b.height > 0.97 { for child in c.childContours { add(child) }; continue }
    if b.width * b.height < 0.0004 { continue }
    add(c)
}
let svg = "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 \(Int(w / s)) \(Int(h / s))\"><path fill=\"#fff\" fill-rule=\"evenodd\" d=\"\(d)\"/></svg>"
try svg.write(toFile: a[2], atomically: true, encoding: .utf8)
print("ok", d.count, "chars")
