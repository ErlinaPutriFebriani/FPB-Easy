# Membuat ikon PWA FPB Easy (PNG) dengan System.Drawing bawaan Windows.
# Jalankan dari folder proyek:  powershell -ExecutionPolicy Bypass -File scripts\buat_ikon.ps1
Add-Type -AssemblyName System.Drawing

$folder = Join-Path $PSScriptRoot "..\public\icons"
New-Item -ItemType Directory -Force -Path $folder | Out-Null

function Buat-Ikon([int]$ukuran, [string]$nama, [bool]$penuh, [double]$skalaIsi) {
    $bmp = New-Object System.Drawing.Bitmap $ukuran, $ukuran
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::Transparent)

    $biru = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 47, 111, 219))
    $putih = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::White)
    $oranye = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb(255, 245, 158, 11))

    if ($penuh) {
        $g.FillRectangle($biru, 0, 0, $ukuran, $ukuran)
    } else {
        $r = [int]($ukuran * 0.22)
        $path = New-Object System.Drawing.Drawing2D.GraphicsPath
        $path.AddArc(0, 0, $r * 2, $r * 2, 180, 90)
        $path.AddArc($ukuran - $r * 2, 0, $r * 2, $r * 2, 270, 90)
        $path.AddArc($ukuran - $r * 2, $ukuran - $r * 2, $r * 2, $r * 2, 0, 90)
        $path.AddArc(0, $ukuran - $r * 2, $r * 2, $r * 2, 90, 90)
        $path.CloseFigure()
        $g.FillPath($biru, $path)
    }

    # Tulisan "FPB"
    $tinggiHuruf = $ukuran * 0.30 * $skalaIsi
    $font = New-Object System.Drawing.Font "Arial", ([single]$tinggiHuruf), ([System.Drawing.FontStyle]::Bold), ([System.Drawing.GraphicsUnit]::Pixel)
    $format = New-Object System.Drawing.StringFormat
    $format.Alignment = [System.Drawing.StringAlignment]::Center
    $format.LineAlignment = [System.Drawing.StringAlignment]::Center
    $kotakTeks = New-Object System.Drawing.RectangleF 0, ([single]($ukuran * -0.06)), $ukuran, $ukuran
    $g.DrawString("FPB", $font, $putih, $kotakTeks, $format)

    # Tiga "chip" kecil: dua putih + satu oranye (faktor persekutuan)
    $d = $ukuran * 0.11 * $skalaIsi
    $jarak = $d * 0.45
    $lebarTotal = 3 * $d + 2 * $jarak
    $x0 = ($ukuran - $lebarTotal) / 2
    $y = $ukuran * 0.5 + $ukuran * 0.13 * $skalaIsi
    for ($i = 0; $i -lt 3; $i++) {
        $kuas = if ($i -eq 2) { $oranye } else { $putih }
        $g.FillEllipse($kuas, [single]($x0 + $i * ($d + $jarak)), [single]$y, [single]$d, [single]$d)
    }

    $file = Join-Path $folder $nama
    $bmp.Save($file, [System.Drawing.Imaging.ImageFormat]::Png)
    $g.Dispose(); $bmp.Dispose()
    Write-Output "Dibuat: $file"
}

Buat-Ikon 192 "icon-192.png" $false 1.0
Buat-Ikon 512 "icon-512.png" $false 1.0
# Maskable: latar penuh, isi diperkecil agar aman dari potongan bentuk ikon Android.
Buat-Ikon 512 "icon-maskable-512.png" $true 0.75
# iPhone: latar penuh (iOS membulatkan sudut sendiri).
Buat-Ikon 180 "apple-touch-icon.png" $true 0.9
