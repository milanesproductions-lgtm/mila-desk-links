# Mila.Desk · Página de productos (link in bio)

Página para el enlace de la biografía de Instagram, TikTok y Facebook.
Muestra los productos de los videos en cuadros, del más nuevo al más viejo.
Al tocar un cuadro se abre el producto: el enlace de Amazon o la página de la marca.

Es un proyecto aparte de la extensión de Chrome.

## Cómo funciona

- `index.html` es la página. Al abrirse lee `productos.json` y muestra los productos.
- `admin/` es el **panel**. Ahí se agregan, editan y quitan productos desde el celular o la computadora.
  Cada cambio se guarda en este repositorio (un solo commit) y GitHub Pages actualiza la página en 1 o 2 minutos.
- El panel necesita, una vez por dispositivo, una llave de GitHub (fine-grained token) con acceso **solo**
  a `mila-desk-links` y permiso **Contents: Read and write**. La llave se guarda solo en ese navegador.
- `fotos/`: portadas en cuadrado de 600×600. El panel las recorta en el propio dispositivo.
- `revisar.py`: revisa que `productos.json` esté bien. `agregar.py`: agrega un producto desde la terminal.

## Categorías

Por ahora solo hay dos, en este orden: **Tecnología** (Technology) y **Hogar** (Home).
Se definen en `categorias` dentro de `productos.json`, con su nombre en español y en inglés.

## Reglas

- El aviso de Amazon se ve siempre arriba de la página.
- Las fotos son propias o cuadros de los videos. No se descargan fotos de Amazon.
- Cada cuadro dice a qué tienda lleva (Amazon o el nombre de la marca).
- Las colaboraciones con marcas llevan la etiqueta «Patrocinado» / «Sponsored». Los enlaces llevan `rel="sponsored"`.
- La página solo muestra productos con enlace https, foto propia y, si dice Amazon, un enlace de Amazon.

## Dirección links.mila-desk.com

1. Donde está el dominio mila-desk.com, agregar un registro DNS:
   tipo **CNAME**, nombre **links**, valor **milanesproductions-lgtm.github.io**.
2. Después, en GitHub → Settings → Pages → Custom domain: `links.mila-desk.com`, y activar «Enforce HTTPS».
