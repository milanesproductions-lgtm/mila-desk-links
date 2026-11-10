#!/usr/bin/env python3
"""Agrega un producto a productos.json, prepara su foto (la página lo muestra sola).

Ejemplos:
  python3 agregar.py --nombre "Licuadora portátil" --enlace "https://amzn.to/xxxx" \
      --foto ~/Desktop/licuadora.jpg --tipo amazon --categoria Tecnología

  python3 agregar.py --nombre "Lámpara LED" --enlace "https://marca.com/lampara" \
      --foto ~/Desktop/lampara.heic --tipo marca --marca "Lumi" --categoria Hogar

La foto (JPG, PNG o HEIC del iPhone) se recorta en cuadrado, se reduce a 600x600
y se guarda en fotos/. Usa tus propias fotos o un cuadro de tu video, nunca fotos
descargadas de Amazon.
"""
import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(RAIZ, "productos.json")


def nombre_archivo(texto):
    t = unicodedata.normalize("NFD", texto.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:40] or "producto"
    return t


def preparar_foto(origen, destino):
    salida = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", origen],
                            capture_output=True, text=True, check=True).stdout
    w = int(re.search(r"pixelWidth: (\d+)", salida).group(1))
    h = int(re.search(r"pixelHeight: (\d+)", salida).group(1))
    lado = min(w, h)
    # Primero recorta el cuadrado central, después reduce: sips no respeta el orden
    # si se piden las dos cosas en una sola llamada.
    subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "82",
                    "-c", str(lado), str(lado), origen, "--out", destino],
                   capture_output=True, check=True)
    subprocess.run(["sips", "-z", "600", "600", destino], capture_output=True, check=True)


def main():
    a = argparse.ArgumentParser(description="Agregar un producto a la página")
    a.add_argument("--nombre", required=True)
    a.add_argument("--nombre-en", default="", help="nombre en inglés (opcional)")
    a.add_argument("--enlace", required=True, help="tu enlace de Amazon o la página de la marca")
    a.add_argument("--foto", required=True, help="ruta de tu foto")
    a.add_argument("--tipo", choices=["amazon", "marca"], required=True)
    a.add_argument("--marca", default="", help="nombre de la marca (si tipo=marca)")
    a.add_argument("--no-patrocinado", action="store_true",
                   help="solo si la marca NO te pagó ni te regaló el producto")
    a.add_argument("--categoria", default="", help="Tecnología u Hogar (las de productos.json)")
    a.add_argument("--fecha", default=datetime.date.today().isoformat(), help="AAAA-MM-DD")
    args = a.parse_args()

    origen = os.path.expanduser(args.foto)
    if not os.path.isfile(origen):
        sys.exit(f"No encuentro la foto: {origen}")

    with open(DATOS, encoding="utf-8") as f:
        datos = json.load(f)

    base = nombre_archivo(args.nombre)
    ruta = f"fotos/{base}.jpg"
    n = 2
    while os.path.exists(os.path.join(RAIZ, ruta)):
        ruta = f"fotos/{base}-{n}.jpg"
        n += 1
    preparar_foto(origen, os.path.join(RAIZ, ruta))

    p = {"nombre": args.nombre, "enlace": args.enlace, "foto": ruta,
         "tipo": args.tipo, "categoria": args.categoria, "fecha": args.fecha}
    if args.nombre_en:
        p["nombre_en"] = args.nombre_en
    if args.tipo == "marca":
        p["marca"] = args.marca
        p["patrocinado"] = not args.no_patrocinado
    sys.path.insert(0, RAIZ)
    from revisar import validar
    errores = validar(p, len(datos["productos"]), datos.get("categorias", []))
    if errores:
        os.remove(os.path.join(RAIZ, ruta))
        print("No se agregó el producto:")
        for err in errores:
            print("  -", err)
        sys.exit(1)
    datos["productos"].append(p)

    with open(DATOS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Agregado: {args.nombre} ({ruta})")


if __name__ == "__main__":
    main()
