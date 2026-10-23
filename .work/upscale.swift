// Увеличение фона для ретины: Lanczos + лёгкая резкость. swift .work/upscale.swift <in> <out.jpg> <scale>
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 4, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let s = Double(a[3])!
let big = src.applyingFilter("CILanczosScaleTransform", parameters: ["inputScale": s, "inputAspectRatio": 1.0])
    .applyingFilter("CIUnsharpMask", parameters: ["inputRadius": 2.0, "inputIntensity": 0.6])
let out = CGRect(x: 0, y: 0, width: (src.extent.width * s).rounded(), height: (src.extent.height * s).rounded())
let ctx = CIContext()
guard let cg = ctx.createCGImage(big, from: out, format: .RGBA8, colorSpace: CGColorSpace(name: CGColorSpace.sRGB)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, [kCGImageDestinationLossyCompressionQuality: 0.88] as CFDictionary)
CGImageDestinationFinalize(dest)
print("ok", Int(out.width), "x", Int(out.height))
