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

valores = sys.stdin.read() if (len(sys.argv) < 2) else sys.argv[1]
linhas = valores.split(SEPARADOR_ENTRE_LINHAS)
TAMANHO_COLUNAS_RELATORIO = [0] * len(linhas[0].split(SEPARADOR_ENTRE_COLUNAS))
DESTACAR_LINHAS = linhas[0].startswith('#')
QUANTIDADE_LINHAS_RELATORIO = 0

for i, linha in enumerate(linhas):
  if not linha:
    continue
  QUANTIDADE_LINHAS_RELATORIO += 1
  colunas = linha.split(SEPARADOR_ENTRE_COLUNAS)
  for j, coluna in enumerate(colunas):
    if DESTACAR_LINHAS and j == 0:
      continue
    if len(coluna) >= TAMANHO_COLUNAS_RELATORIO[j]:
      TAMANHO_COLUNAS_RELATORIO[j] = len(coluna) + 1

# TAMANHO_COLUNAS_RELATORIO = [x + 2 for x in TAMANHO_COLUNAS_RELATORIO]
CARACTERES_TOTAL = sum(TAMANHO_COLUNAS_RELATORIO)
LARGURA_TOTAL_IMAGEM = CARACTERES_TOTAL * LARGURA_CARACTERE
ALTURA_TOTAL_IMAGEM = QUANTIDADE_LINHAS_RELATORIO * ALTURA_CARACTERE

try:
  with Drawing() as draw:
    with Image(
      width = LARGURA_TOTAL_IMAGEM,
      height = ALTURA_TOTAL_IMAGEM,
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
          if DESTACAR_LINHAS and j == 0:
            if i == 0:
              continue
            cor = try_parse_int(coluna)
            if cor:
              top_margin = (i * ALTURA_CARACTERE) + 1
              botton_margin = (i * ALTURA_CARACTERE) + ALTURA_CARACTERE + 1
              draw.fill_color = Color(CORES[cor])
              draw.rectangle(
                left = 0,
                right = LARGURA_TOTAL_IMAGEM,
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
          cursor = sum(TAMANHO_COLUNAS_RELATORIO[:j + 1]) * LARGURA_CARACTERE
      draw(img)
      img_bytes = img.make_blob(format='png')
      if not img_bytes:
        raise Exception()
      img_base64 = base64.b64encode(img_bytes).decode('utf-8')
      print(img_base64)
except Exception as erro:
  print('500: Image cannot be generated')
  print(erro.args[0])
