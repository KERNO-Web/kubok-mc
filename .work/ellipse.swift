// Вырезает объект с фото эллипсом с мягким краем, сохраняя все родные пиксели (блики, тени). Увеличивает x scale.
// swift .work/ellipse.swift <in> <out.png> cx cy rx ry scale
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 8, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let H = src.extent.height
let cx = Double(a[3])!, cy = Double(a[4])!, rx = Double(a[5])!, ry = Double(a[6])!, s = Double(a[7])!
let r = CGRect(x: cx - rx - 2, y: H - cy - ry - 2, width: 2 * rx + 4, height: 2 * ry + 4)
let crop = src.cropped(to: r).transformed(by: CGAffineTransform(translationX: -r.minX, y: -r.minY))
let big = crop.applyingFilter("CILanczosScaleTransform", parameters: ["inputScale": s, "inputAspectRatio": 1.0])
let W = r.width * s, Hh = r.height * s
let out = CGRect(x: 0, y: 0, width: W.rounded(), height: Hh.rounded())
// круговой градиент, растянутый в эллипс
let circ = CIFilter(name: "CIRadialGradient", parameters: [
    "inputCenter": CIVector(x: 0, y: 0), "inputRadius0": rx * s * 0.86, "inputRadius1": rx * s,
    "inputColor0": CIColor(red: 1, green: 1, blue: 1, alpha: 1), "inputColor1": CIColor(red: 0, green: 0, blue: 0, alpha: 1)])!.outputImage!
let mask = circ.transformed(by: CGAffineTransform(scaleX: 1, y: ry / rx).concatenating(CGAffineTransform(translationX: W / 2, y: Hh / 2))).cropped(to: out)
let clear = CIImage(color: CIColor(red: 0, green: 0, blue: 0, alpha: 0)).cropped(to: out)
let res = big.applyingFilter("CIBlendWithMask", parameters: ["inputBackgroundImage": clear, "inputMaskImage": mask]).cropped(to: out)
let ctx = CIContext()
guard let cg = ctx.createCGImage(res, from: out, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", Int(out.width), "x", Int(out.height))
