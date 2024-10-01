""" Test """
from io import StringIO
import pytest
from csv2b64img import main

def test_image_generation_with_valid_input(monkeypatch, capsys):
  """ Test the script with a valid csv input """
  # Mock the input: simulate CSV-like input as a string
  mock_csv_input = "Name,Age,Color\nJohn,25,1\nDoe,30,2"
  # Mock stdin with the CSV input
  monkeypatch.setattr('sys.stdin', StringIO(mock_csv_input))
  # Mock sys.argv if your script needs it
  monkeypatch.setattr('sys.argv', ['csv2b64img.py'])  # Adjust if needed
  # Run your script's main function (replace with the actual entry point of your script)
  main()
  # Capture the output
  captured = capsys.readouterr()
  # Ensure the output is in base64 format
  output = captured.out.strip()
  assert output.startswith('iVBOR')  # Base64 for a PNG starts with 'iVBOR'
  assert len(output) > 100  # Check the length to ensure it's a valid image string

def test_image_generation_with_invalid_input(monkeypatch, capsys):
  """ Test the script with a invalid csv input """
  # Mock the input: simulate an empty CSV-like input
  mock_csv_input = ""
  # Mock stdin with the CSV input
  monkeypatch.setattr('sys.stdin', StringIO(mock_csv_input))
  # Mock sys.argv if your script needs it
  monkeypatch.setattr('sys.argv', ['csv2b64img.py'])  # Adjust if needed
  # Run your script's main function (replace with the actual entry point of your script)
  main()
  # Capture the output
  captured = capsys.readouterr()
  # Ensure the error message is printed
  output = captured.out.strip()
  assert '400: Input is not a valid CSV data' in output
