// Дерево HUNT без растяжения на весь блок: исходник + его зеркало снизу (шов по вертикали не виден),
// опционально Lanczos + лёгкая резкость. swift .work/wood_v79.swift <in> <out.jpg> <scale>
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 4, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let s = Double(a[3])!
let w = src.extent.width, h = src.extent.height
// CoreImage: y вверх. Оригинал наверху (y h..2h), зеркало снизу (0..h)
let top = src.transformed(by: CGAffineTransform(translationX: 0, y: h))
let bottom = src.transformed(by: CGAffineTransform(scaleX: 1, y: -1).translatedBy(x: 0, y: -h))
var img = top.composited(over: bottom)
if s != 1 {
  img = img.applyingFilter("CILanczosScaleTransform", parameters: ["inputScale": s, "inputAspectRatio": 1.0])
    .applyingFilter("CIUnsharpMask", parameters: ["inputRadius": 1.6, "inputIntensity": 0.5])
}
let out = CGRect(x: 0, y: 0, width: (w * s).rounded(), height: (2 * h * s).rounded())
guard let cg = CIContext().createCGImage(img, from: out, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, [kCGImageDestinationLossyCompressionQuality: 0.9] as CFDictionary)
CGImageDestinationFinalize(dest)
print("ok", Int(out.width), "x", Int(out.height))
