// Снимает красную краску с афиши с увеличением. Режимы:
//   mask  — белое на чёрном (для vectorize.swift), резкий порог
//   paint — RGBA: цвет пикселя афиши, альфа = сколько в нём красного (краска с просветами, на белом читается 1:1)
// Запуск: swift .work/paint.swift <mode> <in> <out.png> x y w h scale
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 9, let src = CIImage(contentsOf: URL(fileURLWithPath: a[2])) else { print("usage"); exit(1) }
let mode = a[1]
let H = src.extent.height
let x = Double(a[4])!, y = Double(a[5])!, w = Double(a[6])!, h = Double(a[7])!, s = Double(a[8])!
let rect = CGRect(x: x, y: H - y - h, width: w, height: h)
let crop = src.clampedToExtent().cropped(to: rect).transformed(by: CGAffineTransform(translationX: -rect.minX, y: -rect.minY))
let big = crop.applyingFilter("CILanczosScaleTransform", parameters: ["inputScale": s, "inputAspectRatio": 1.0])
let out = CGRect(x: 0, y: 0, width: (w * s).rounded(), height: (h * s).rounded())

// «сколько красного»: (R - (G+B)/2)
func redness(_ img: CIImage, gain: CGFloat, bias: CGFloat) -> CIImage {
    img.applyingFilter("CIColorMatrix", parameters: [
        "inputRVector": CIVector(x: gain, y: -gain / 2, z: -gain / 2, w: 0),
        "inputGVector": CIVector(x: gain, y: -gain / 2, z: -gain / 2, w: 0),
        "inputBVector": CIVector(x: gain, y: -gain / 2, z: -gain / 2, w: 0),
        "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
        "inputBiasVector": CIVector(x: bias, y: bias, z: bias, w: 0)]).applyingFilter("CIColorClamp")
}

var result: CIImage
if mode == "mask" {
    // мягкий шум внутри букв гасим размытием, потом жёсткий порог
    let m = redness(big.applyingFilter("CIGaussianBlur", parameters: ["inputRadius": s * 0.8]), gain: 10, bias: -1.9)
    result = m.cropped(to: out)
} else {
    // резкость после увеличения, бледно-розовую дымку бумаги отрезаем
    let sharp = big.applyingFilter("CIUnsharpMask", parameters: ["inputRadius": s * 0.9, "inputIntensity": 0.85])
    let m = redness(big.applyingFilter("CIGaussianBlur", parameters: ["inputRadius": s * 0.25]), gain: 4.4, bias: -0.36)
    let clear = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: out)
    result = sharp.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": m]).cropped(to: out)
}
let ctx = CIContext()
guard let cg = ctx.createCGImage(result, from: out, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[3]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", Int(out.width), "x", Int(out.height))
