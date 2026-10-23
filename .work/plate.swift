// Вырезает металлическую табличку с белого фона: маска «не белое», закрытие дыр (блики внутри), мягкий край.
// swift .work/plate.swift <in> <out.png>
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 3, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let ext = src.extent
// min(R,G,B) → не белое = 1
let m0 = src.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0), "inputGVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0),
    "inputBVector": CIVector(x: 0, y: 0.5, z: 0.5, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1)])
    .applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: -40, y: 0, z: 0, w: 0), "inputGVector": CIVector(x: -40, y: 0, z: 0, w: 0),
    "inputBVector": CIVector(x: -40, y: 0, z: 0, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: 39.2, y: 39.2, z: 39.2, w: 0)]).applyingFilter("CIColorClamp")
// закрытие: расширить на 14px, сжать на 14px — дыры от бликов внутри заливаются
let closed = m0.clampedToExtent()
    .applyingFilter("CIMorphologyMaximum", parameters: ["inputRadius": 14])
    .applyingFilter("CIMorphologyMinimum", parameters: ["inputRadius": 15])
    .applyingFilter("CIGaussianBlur", parameters: ["inputRadius": 0.8]).cropped(to: ext)
let clear = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: ext)
let out = src.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": closed])
let ctx = CIContext()
guard let cg = ctx.createCGImage(out, from: ext, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", Int(ext.width), "x", Int(ext.height))
