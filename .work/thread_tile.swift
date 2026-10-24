// Бесшовная нитка: исходник + его зеркало по горизонтали, края всегда совпадают. swift .work/thread_tile.swift <in> <out.png>
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers
let a = CommandLine.arguments
guard a.count == 3, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let w = src.extent.width, h = src.extent.height
let flip = src.transformed(by: CGAffineTransform(scaleX: -1, y: 1).translatedBy(x: -2 * w, y: 0))
let img = flip.composited(over: src)
guard let cg = CIContext().createCGImage(img, from: CGRect(x: 0, y: 0, width: 2 * w, height: h)) else { exit(3) }
let d = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(d, cg, nil)
CGImageDestinationFinalize(d)
print("ok", Int(2 * w), "x", Int(h))
