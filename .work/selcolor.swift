// Выборочный цвет («Город грехов»): оставляет только доминирующий насыщенный цвет кадра, остальное прозрачно.
// swift selcolor.swift <in> <out.png> [минимальная насыщенность, по умолчанию 0.5] [окно оттенка в градусах, по умолчанию 16]
import Foundation
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let args = CommandLine.arguments
let minSat = args.count > 3 ? Double(args[3])! : 0.5
let win = args.count > 4 ? Double(args[4])! : 16
guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: args[1]) as CFURL, nil),
      let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("не читается \(args[1])") }
let w = img.width, h = img.height
var px = [UInt8](repeating: 0, count: w * h * 4)
let cs = CGColorSpaceCreateDeviceRGB()
let ctx = CGContext(data: &px, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs,
                    bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
ctx.draw(img, in: CGRect(x: 0, y: 0, width: w, height: h))

func hsv(_ r: Double, _ g: Double, _ b: Double) -> (Double, Double, Double) {
  let mx = max(r, g, b), mn = min(r, g, b), d = mx - mn
  var hh = 0.0
  if d > 0 {
    if mx == r { hh = (g - b) / d } else if mx == g { hh = (b - r) / d + 2 } else { hh = (r - g) / d + 4 }
    hh *= 60; if hh < 0 { hh += 360 }
  }
  return (hh, mx > 0 ? d / mx : 0, mx)
}
func smooth(_ a: Double, _ b: Double, _ x: Double) -> Double { let t = min(1, max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t) }

// 1. гистограмма оттенков насыщенных пикселей (вес = насыщенность × яркость)
var hist = [Double](repeating: 0, count: 36)
for i in stride(from: 0, to: px.count, by: 4) {
  let a = Double(px[i + 3]) / 255; if a < 0.5 { continue }
  let (hh, s, v) = hsv(Double(px[i]) / 255 / a, Double(px[i + 1]) / 255 / a, Double(px[i + 2]) / 255 / a)
  if s > minSat && v > 0.25 { hist[min(35, Int(hh / 10))] += s * v }
}
// сгладить по соседям (оттенок по кругу) и взять пик
var best = 0, bestV = -1.0
for k in 0..<36 { let v = hist[(k + 35) % 36] * 0.5 + hist[k] + hist[(k + 1) % 36] * 0.5; if v > bestV { bestV = v; best = k } }
let h0 = Double(best) * 10 + 5
let total = Double(w * h)
fputs("hue \(Int(h0)) weight \(String(format: "%.4f", bestV / total))\n", stderr)

// 2. маска: насыщенный пиксель близкого к пику оттенка
var out = [UInt8](repeating: 0, count: w * h * 4)
for i in stride(from: 0, to: px.count, by: 4) {
  let a = Double(px[i + 3]) / 255; if a < 0.01 { continue }
  let r = Double(px[i]) / 255 / a, g = Double(px[i + 1]) / 255 / a, b = Double(px[i + 2]) / 255 / a
  let (hh, s, v) = hsv(r, g, b)
  var dh = abs(hh - h0); if dh > 180 { dh = 360 - dh }
  let m = smooth(minSat - 0.12, minSat + 0.08, s) * smooth(0.12, 0.28, v) * (1 - smooth(win, win + 12, dh)) * a
  out[i] = UInt8(r * m * 255); out[i + 1] = UInt8(g * m * 255); out[i + 2] = UInt8(b * m * 255); out[i + 3] = UInt8(m * 255)
}
let octx = CGContext(data: &out, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: cs,
                     bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: args[2]) as CFURL, UTType.png.identifier as CFString, 1, nil)!
CGImageDestinationAddImage(dst, octx.makeImage()!, nil)
CGImageDestinationFinalize(dst)
