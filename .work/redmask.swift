// Выделяет красную краску: (R - G) * 3 в белое на чёрном. Обрезает область x,y,w,h (от верхнего левого угла).
// Запуск: swift .work/redmask.swift <in> <out.png> x y w h
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 7, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let H = src.extent.height
let x = Double(a[3])!, y = Double(a[4])!, w = Double(a[5])!, h = Double(a[6])!
let rect = CGRect(x: x, y: H - y - h, width: w, height: h)
let cropped = src.cropped(to: rect).transformed(by: CGAffineTransform(translationX: -rect.minX, y: -rect.minY))
let mask = cropped.applyingFilter("CIColorMatrix", parameters: [
    "inputRVector": CIVector(x: 3, y: -3, z: 0, w: 0),
    "inputGVector": CIVector(x: 3, y: -3, z: 0, w: 0),
    "inputBVector": CIVector(x: 3, y: -3, z: 0, w: 0),
    "inputAVector": CIVector(x: 0, y: 0, z: 0, w: 1),
    "inputBiasVector": CIVector(x: -0.25, y: -0.25, z: -0.25, w: 0)])
let ctx = CIContext()
guard let cg = ctx.createCGImage(mask, from: CGRect(x: 0, y: 0, width: w, height: h)) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, nil)
CGImageDestinationFinalize(dest)
print("ok")
