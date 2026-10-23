// Запекает ч/б + контраст + зерно в файл, прозрачность сохраняется (для вырезок).
// Запуск: swift .work/bake.swift <вход> <выход.jpg|png>
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 3, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage: bake in out"); exit(1) }
let ext = src.extent

let noir = src.applyingFilter("CIPhotoEffectNoir")
let graded = noir.applyingFilter("CIColorControls", parameters: ["inputContrast": 1.14, "inputBrightness": -0.02])

// Зерно: случайный шум, приглушённый, только там, где есть изображение
let noise = CIFilter(name: "CIRandomGenerator")!.outputImage!.cropped(to: ext)
    .applyingFilter("CIColorMatrix", parameters: [
        "inputRVector": CIVector(x: 0, y: 1, z: 0, w: 0), "inputGVector": CIVector(x: 0, y: 1, z: 0, w: 0),
        "inputBVector": CIVector(x: 0, y: 1, z: 0, w: 0), "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 0.07),
        "inputBiasVector": CIVector(x: 0, y: 0, z: 0, w: 0)])
let grain = noise.applyingFilter("CISourceAtopCompositing", parameters: [kCIInputBackgroundImageKey: graded]).cropped(to: ext)

let out = URL(fileURLWithPath: a[2])
let png = out.pathExtension.lowercased() == "png"
let ctx = CIContext()
guard let cg = ctx.createCGImage(grain, from: ext) else { exit(3) }
let type = (png ? UTType.png : UTType.jpeg).identifier as CFString
guard let dest = CGImageDestinationCreateWithURL(out as CFURL, type, 1, nil) else { exit(4) }
CGImageDestinationAddImage(dest, cg, png ? nil : [kCGImageDestinationLossyCompressionQuality: 0.86] as CFDictionary)
CGImageDestinationFinalize(dest)
print("ok", a[2])
