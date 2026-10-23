// Вырезает людей с фото (macOS Vision, без сети) и сохраняет PNG с прозрачным фоном.
// Запуск: swift .work/cutout.swift <вход.jpg> <выход.png>
import Foundation
import Vision
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
guard args.count == 3 else { print("usage: cutout in out"); exit(1) }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])

guard let ci = CIImage(contentsOf: input) else { print("cannot read"); exit(1) }
let handler = VNImageRequestHandler(ciImage: ci)
let req = VNGenerateForegroundInstanceMaskRequest()
try handler.perform([req])
guard let result = req.results?.first else { print("no subject"); exit(2) }
let buffer = try result.generateMaskedImage(ofInstances: result.allInstances, from: handler, croppedToInstancesExtent: false)
let masked = CIImage(cvPixelBuffer: buffer)
let ctx = CIContext()
guard let cg = ctx.createCGImage(masked, from: masked.extent) else { exit(3) }
guard let dest = CGImageDestinationCreateWithURL(output as CFURL, UTType.png.identifier as CFString, 1, nil) else { exit(4) }
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok", result.allInstances.count, "instances")
