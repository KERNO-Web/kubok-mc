// Вырезает красный объект (булавку или нитку) с доски по «красноте», с закрытием бликов. Можно повернуть кроп.
// swift .work/redcut.swift <in> <out.png> x y w h angleDeg closeRadius
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 9, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let H = src.extent.height
let x = Double(a[3])!, y = Double(a[4])!, w = Double(a[5])!, h = Double(a[6])!
let ang = Double(a[7])! * .pi / 180, rad = Double(a[8])!
// поворот вокруг центра кропа, потом кроп
let cx = x + w / 2, cy = H - y - h / 2
let rot = src.clampedToExtent().transformed(by: CGAffineTransform(translationX: -cx, y: -cy).concatenating(CGAffineTransform(rotationAngle: ang)).concatenating(CGAffineTransform(translationX: cx, y: cy)))
let r = CGRect(x: x, y: H - y - h, width: w, height: h)
let crop = rot.cropped(to: r).transformed(by: CGAffineTransform(translationX: -r.minX, y: -r.minY))
let out = CGRect(x: 0, y: 0, width: w, height: h)
// краснота R - (G+B)/2, порог мягкий
var m = crop.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 5, y: -2.5, z: -2.5, w: 0), "inputGVector": CIVector(x: 5, y: -2.5, z: -2.5, w: 0),
    "inputBVector": CIVector(x: 5, y: -2.5, z: -2.5, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: -2.1, y: -2.1, z: -2.1, w: 0)]).applyingFilter("CIColorClamp")
if rad > 0 {
    m = m.clampedToExtent().applyingFilter("CIMorphologyMaximum", parameters: ["inputRadius": rad])
        .applyingFilter("CIMorphologyMinimum", parameters: ["inputRadius": rad]).cropped(to: out)
}
m = m.clampedToExtent().applyingFilter("CIGaussianBlur", parameters: ["inputRadius": 0.6]).cropped(to: out)
let clear = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: out)
let res = crop.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": m]).cropped(to: out)
let ctx = CIContext()
guard let cg = ctx.createCGImage(res, from: out, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", Int(w), "x", Int(h))
