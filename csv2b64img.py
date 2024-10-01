#!/usr/bin/python
""" Module that convert csv table on base64 image string """
# coding: utf8
#region import
import sys
import base64
from typing import NamedTuple
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
#endregion import

SEPARADOR_ENTRE_COLUNAS = ','
SEPARADOR_ENTRE_LINHAS = '\n'
LARGURA_CARACTERE = 13
ALTURA_CARACTERE = 20
# CORES: branco, preto, vermelho, amarelo, verde
CORES = [
  'rgb(255,255,255)',
  'rgb(0,0,0)',
  'rgb(255,128,128)',
  'rgb(255,255,128)',
  'rgb(128,255,128)'
]

class ImageCannotBeGenerateError(BaseException):
  """ Exeption that oocurs when image cannot be generated """

class Propriedades(NamedTuple):
  """ class to hold some values """
  destacar: bool
  quantidades: int
  tamanhos: list[int]
  largura: int
  altura: int

def get_greatest_elements(vec1, vec2) -> list[int]:
  """ Function to get the greatest elements """
  if len(vec1) != len(vec2):
    raise ValueError("Vectors must be of the same size.")
  # Use a list comprehension with the built-in max() function
  return [max(v1, v2) for v1, v2 in zip(vec1, vec2)]

def get_csv_definitions(csv_data: str) -> Propriedades:
  """ Method to get Propriedades of csv data """
  if len(csv_data.strip()) == 0:
    raise ValueError("Invalid CSV input.")
  destacar = csv_data.startswith('#')
  linhas = csv_data.split(SEPARADOR_ENTRE_LINHAS)
  quantidades = sum(len(x.strip()) > 0 for x in linhas)
  tamanhos = [0 for x in linhas[0].split(SEPARADOR_ENTRE_COLUNAS)]
  for linha in linhas:
    colunas = linha.strip().split(SEPARADOR_ENTRE_COLUNAS)
    tamanhos_colunas = [len(x) for x in colunas]
    tamanhos = get_greatest_elements(tamanhos_colunas, tamanhos)
  propriedades = Propriedades(
    destacar=destacar,
    tamanhos=tamanhos,
    quantidades=quantidades,
    altura= quantidades * ALTURA_CARACTERE,
    largura= sum(tamanhos) * LARGURA_CARACTERE
    )
  return propriedades

def try_parse_int(arg: str):
  """ Get int value from str """
  try:
    return int(arg)
  except ValueError:
    return None

def generate_image_from_csv(csv_data: str) -> str:
  """Generate base64 image string from CSV-like input"""
  propriedades = get_csv_definitions(csv_data)
  linhas = csv_data.split(SEPARADOR_ENTRE_LINHAS)
  if not linhas or len(linhas[0].strip()) == 0:
    raise ValueError("Invalid CSV input.")
  # Generate the image
  with Drawing() as draw:
    with Image(
      width = propriedades.largura,
      height = propriedades.altura,
      background = Color(CORES[0])
      ) as img:
      draw.font_family = 'Consolas'
      draw.font = 'Consolas'
      draw.font_size = ALTURA_CARACTERE # 15x15 cada letra
      for i, linha in enumerate(linhas):
        cursor = 0 # reset cursor position
        if not linha:
          continue
        colunas = linha.split(SEPARADOR_ENTRE_COLUNAS)
        for j, coluna in enumerate(colunas):
          if propriedades.destacar and j == 0:
            if i == 0:
              continue
            cor = try_parse_int(coluna)
            if cor:
              draw.fill_color = Color(CORES[cor])
              draw.rectangle(
                left = 0,
                right = propriedades.largura,
                top = (i * ALTURA_CARACTERE) + 1,
                bottom = (i * ALTURA_CARACTERE) + ALTURA_CARACTERE + 1)
              draw.fill_color = Color(CORES[1])
          else:
            if coluna:
              for letra in coluna:
                draw.text(
                  x = cursor,
                  y = ((i + 1) * ALTURA_CARACTERE),
                  body = letra)
                cursor += LARGURA_CARACTERE
          cursor = sum(propriedades.tamanhos[:j + 1]) * LARGURA_CARACTERE
      draw(img)
      img_bytes = img.make_blob(format='png')
      if not img_bytes:
        raise ImageCannotBeGenerateError()
      img_base64 = base64.b64encode(img_bytes).decode('utf-8')
      return img_base64

def main():
  """Main function to handle command line input and output"""
  valores = sys.stdin.read() if (len(sys.argv) < 2) else sys.argv[1]
  try:
    img_base64 = generate_image_from_csv(valores)
    print(img_base64)
  except ImageCannotBeGenerateError:
    print('500: Image cannot be generated')
  except ValueError:
    print('400: Input is not a valid CSV data')

if __name__ == '__main__':
  main()
