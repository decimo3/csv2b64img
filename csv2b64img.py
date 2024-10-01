#!/usr/bin/python
""" Module that convert csv table on base64 image string """
# coding: utf8
#region import
import sys
import base64
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

def try_parse_int(arg: str):
  """ Get int value from str """
  try:
    return int(arg)
  except ValueError:
    return None

def generate_image_from_csv(csv_data: str) -> str:
  """Generate base64 image string from CSV-like input"""
  linhas = csv_data.split(SEPARADOR_ENTRE_LINHAS)
  if not linhas or len(linhas[0].strip()) == 0:
    raise ValueError("Invalid CSV input.")
  tamanho_colunas_relatorio = [0] * len(linhas[0].split(SEPARADOR_ENTRE_COLUNAS))
  destacar_linhas = linhas[0].startswith('#')
  quantidade_linhas_relatorio = 0
  for i, linha in enumerate(linhas):
    if not linha:
      continue
    quantidade_linhas_relatorio += 1
    colunas = linha.split(SEPARADOR_ENTRE_COLUNAS)
    for j, coluna in enumerate(colunas):
      if destacar_linhas and j == 0:
        continue
      if len(coluna) >= tamanho_colunas_relatorio[j]:
        tamanho_colunas_relatorio[j] = len(coluna) + 1
  # tamanho_colunas_relatorio = [x + 2 for x in tamanho_colunas_relatorio]
  caracteres_total = sum(tamanho_colunas_relatorio)
  largura_total_imagem = caracteres_total * LARGURA_CARACTERE
  altura_total_imagem = quantidade_linhas_relatorio * ALTURA_CARACTERE
  # Generate the image
  with Drawing() as draw:
    with Image(
      width = largura_total_imagem,
      height = altura_total_imagem,
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
          if destacar_linhas and j == 0:
            if i == 0:
              continue
            cor = try_parse_int(coluna)
            if cor:
              top_margin = (i * ALTURA_CARACTERE) + 1
              botton_margin = (i * ALTURA_CARACTERE) + ALTURA_CARACTERE + 1
              draw.fill_color = Color(CORES[cor])
              draw.rectangle(
                left = 0,
                right = largura_total_imagem,
                top = top_margin,
                bottom = botton_margin)
              draw.fill_color = Color(CORES[1])
          else:
            if coluna:
              for letra in coluna:
                draw.text(
                  x = cursor,
                  y = ((i + 1) * ALTURA_CARACTERE),
                  body = letra)
                cursor += LARGURA_CARACTERE
          cursor = sum(tamanho_colunas_relatorio[:j + 1]) * LARGURA_CARACTERE
      draw(img)
      img_bytes = img.make_blob(format='png')
      if not img_bytes:
        raise Exception()
      img_base64 = base64.b64encode(img_bytes).decode('utf-8')
      return img_base64

def main():
  """Main function to handle command line input and output"""
  valores = sys.stdin.read() if (len(sys.argv) < 2) else sys.argv[1]
  try:
    img_base64 = generate_image_from_csv(valores)
    print(img_base64)
  except:
    print('500: Image cannot be generated')

if __name__ == '__main__':
  main()
