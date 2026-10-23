// Бесшовная плитка: вырезает патч и складывает 2x2 с зеркалами. swift .work/mirror.swift <in> <out.jpg> x y w h
import Foundation
import CoreImage
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count == 7, let src = CIImage(contentsOf: URL(fileURLWithPath: a[1])) else { print("usage"); exit(1) }
let H = src.extent.height
let x = Double(a[3])!, y = Double(a[4])!, w = Double(a[5])!, h = Double(a[6])!
let r = CGRect(x: x, y: H - y - h, width: w, height: h)
let p = src.cropped(to: r).transformed(by: CGAffineTransform(translationX: -r.minX, y: -r.minY))
let fx = p.transformed(by: CGAffineTransform(scaleX: -1, y: 1).translatedBy(x: -2 * w, y: 0))
let fy = p.transformed(by: CGAffineTransform(scaleX: 1, y: -1).translatedBy(x: 0, y: -2 * h))
let fxy = p.transformed(by: CGAffineTransform(scaleX: -1, y: -1).translatedBy(x: -2 * w, y: -2 * h))
let tile = fxy.composited(over: fy.composited(over: fx.composited(over: p)))
let out = CGRect(x: 0, y: 0, width: 2 * w, height: 2 * h)
let ctx = CIContext()
guard let cg = ctx.createCGImage(tile, from: out) else { exit(3) }
let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: a[2]) as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dest, cg, [kCGImageDestinationLossyCompressionQuality: 0.84] as CFDictionary)
CGImageDestinationFinalize(dest)
print("ok", Int(2 * w), "x", Int(2 * h))
