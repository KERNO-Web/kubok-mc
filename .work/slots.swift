// Ищет пустые тёмные окна полароидов на доске: тёмное и серое (не коричневое дерево) → контуры Vision → рамки.
// swift .work/slots.swift <board> <mask.png>   печатает x y w h в долях (от верхнего левого угла)
import Foundation
import CoreImage
import Vision
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 3, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let ext = src.extent
// серость: 1 - (R - B)*6 ; тёмность: (0.55 - L)*5 ; маска = их произведение через порог
let grey = src.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: -6, y: 0, z: 6, w: 0), "inputGVector": CIVector(x: -6, y: 0, z: 6, w: 0),
    "inputBVector": CIVector(x: -6, y: 0, z: 6, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: 1, y: 1, z: 1, w: 0)]).applyingFilter("CIColorClamp")
let dark = src.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: -1.7, y: -1.7, z: -1.7, w: 0), "inputGVector": CIVector(x: -1.7, y: -1.7, z: -1.7, w: 0),
    "inputBVector": CIVector(x: -1.7, y: -1.7, z: -1.7, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: 2.6, y: 2.6, z: 2.6, w: 0)]).applyingFilter("CIColorClamp")
let m = grey.applyingFilter("CIMultiplyCompositing", parameters: ["inputBackgroundImage": dark])
    .applyingFilter("CIGaussianBlur", parameters: ["inputRadius": 6]).cropped(to: ext)
    .applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 8, y: 0, z: 0, w: 0), "inputGVector": CIVector(x: 8, y: 0, z: 0, w: 0),
    "inputBVector": CIVector(x: 8, y: 0, z: 0, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: -3.6, y: -3.6, z: -3.6, w: 0)]).applyingFilter("CIColorClamp")
let ctx = CIContext()
let cg = ctx.createCGImage(m, from: ext)!
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
let req = VNDetectContoursRequest()
req.detectsDarkOnLight = false
try VNImageRequestHandler(cgImage: cg).perform([req])
for c in req.results!.first!.topLevelContours {
    let b = c.normalizedPath.boundingBox
    if b.width * b.height < 0.01 { continue }
    print(String(format: "%.4f %.4f %.4f %.4f", b.minX, 1 - b.maxY, b.width, b.height))
}
