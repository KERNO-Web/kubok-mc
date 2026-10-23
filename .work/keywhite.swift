// Вырезает надпись с белого фона в PNG с прозрачностью. Альфа = насколько пиксель темнее белого (по min(R,G,B)),
// поэтому красная заливка и светло-серая обводка остаются, чистый белый уходит.
// Запуск: swift .work/keywhite.swift <in> <out.png> x y w h
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
// необязательно: cx cy — стереть всё правее cx и выше cy (в координатах кропа), чтобы убрать соседнюю надпись
guard a.count == 7 || a.count == 9, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let H = src.extent.height
let x = Double(a[3])!, y = Double(a[4])!, w = Double(a[5])!, h = Double(a[6])!
let r = CGRect(x: x, y: H - y - h, width: w, height: h)
let crop = src.cropped(to: r).transformed(by: CGAffineTransform(translationX: -r.minX, y: -r.minY))
// min(R,G,B): берём G и B (у красного они низкие, у белого высокие), R не нужен
let minGB = crop.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0),
    "inputGVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0),
    "inputBVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0),
    "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1)])
// альфа = (0.975 - v) * 14, зажатая в 0..1
let mask = minGB.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: -14, y: 0, z: 0, w: 0),
    "inputGVector": CIVector(x: -14, y: 0, z: 0, w: 0),
    "inputBVector": CIVector(x: -14, y: 0, z: 0, w: 0),
    "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: 13.65, y: 13.65, z: 13.65, w: 0)]).applyingFilter("CIColorClamp")
let clear = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: crop.extent)
var out = crop.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": mask])
if a.count == 9 {
    let cx = Double(a[7])!, cy = Double(a[8])!
    let hole = CGRect(x: cx, y: h - cy, width: w - cx, height: cy)
    let black = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 1)).cropped(to: hole)
    let keep = black.composited(over: CIImage(color: CIColor(red: 1, green: 1, blue: 1, alpha: 1)).cropped(to: crop.extent))
    out = out.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": keep])
}
let ctx = CIContext()
guard let cg = ctx.createCGImage(out, from: crop.extent, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", Int(w), "x", Int(h))
