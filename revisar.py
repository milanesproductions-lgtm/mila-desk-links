#!/usr/bin/env python3
"""Revisa que productos.json esté bien (enlaces, fotos, categorías).

Uso:  python3 revisar.py
La página (index.html) lee productos.json directamente; no hace falta construir nada.
"""
import json
import os
import sys
from urllib.parse import urlparse

RAIZ = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(RAIZ, "productos.json")

AMAZON_HOSTS = ("amazon.com", "amzn.to", "amzn.com", "a.co")


def es_amazon(url):
    host = (urlparse(url).hostname or "").lower()
    return any(host == h or host.endswith("." + h) for h in AMAZON_HOSTS)


def leer_categorias():
    with open(DATOS, encoding="utf-8") as f:
        return json.load(f).get("categorias", [])


def validar(p, i, categorias=None):
    if categorias is None:
        categorias = leer_categorias()
    errores = []
    cat = str(p.get("categoria", "")).strip()
    nombres = [c["es"] for c in categorias]
    if cat and cat not in nombres:
        errores.append(f"producto {i + 1}: la categoría «{cat}» no existe; las que hay son: {', '.join(nombres)}")
    for campo in ("nombre", "enlace", "foto", "fecha"):
        if not str(p.get(campo, "")).strip():
            errores.append(f"producto {i + 1}: falta «{campo}»")
    enlace = p.get("enlace", "")
    if enlace and urlparse(enlace).scheme != "https":
        errores.append(f"producto {i + 1}: el enlace debe empezar por https://")
    foto = p.get("foto", "")
    if foto and not os.path.isfile(os.path.join(RAIZ, foto)):
        errores.append(f"producto {i + 1}: no existe la foto {foto}")
    if p.get("tipo") not in ("amazon", "marca"):
        errores.append(f"producto {i + 1}: «tipo» debe ser amazon o marca")
    if p.get("tipo") == "amazon" and enlace and not es_amazon(enlace):
        errores.append(f"producto {i + 1}: es tipo amazon pero el enlace no es de Amazon")
    if p.get("tipo") == "marca" and not str(p.get("marca", "")).strip():
        errores.append(f"producto {i + 1}: falta el nombre de la «marca»")
    return errores


def main():
    with open(DATOS, encoding="utf-8") as f:
        datos = json.load(f)
    categorias = datos.get("categorias", [])
    productos = datos.get("productos", [])
    errores = [err for i, p in enumerate(productos) for err in validar(p, i, categorias)]
    if errores:
        print("Hay que corregir esto en productos.json:")
        for err in errores:
            print("  -", err)
        sys.exit(1)
    print(f"Todo bien: {len(productos)} productos.")


if __name__ == "__main__":
    main()
