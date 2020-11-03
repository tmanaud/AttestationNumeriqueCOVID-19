from PyPDF2 import PdfFileWriter, PdfFileReader
import qrcode
import datetime
from PIL import ImageFont
from PIL import ImageDraw
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pathlib import Path

from datetime import datetime,timedelta
import argparse


# Motifs
# travail-courses-sante-famille-sport-judiciaire-missions

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-name", required=True, type=str)
    parser.add_argument("--last-name", required=True, type=str)
    parser.add_argument("--birth-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--birth-city", required=True, type=str)
    parser.add_argument("--address", required=True, type=str, help="Address Postcode City")
    parser.add_argument("--current-city", required=True, type=str)
    parser.add_argument("--start-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--end-date", required=True, type=str, help="DD/MM/YYYY")
    parser.add_argument("--leave-hour", required=True, type=str, help="HH:MM")
    parser.add_argument("--motifs", required=True, type=str, help="- delimited: travail-courses-sante-famille-sport-judiciaire-missions")
    parser.add_argument("--save-as", required=False, type=str)
    return parser.parse_args()


args = parse_args()
print("Args:", args)


# ---------------------------
#  First Page (All fields to fill)
# ---------------------------
def generate():
  img = Image.open("input-page1.png")
  img_array = np.array(img)

  # Erase fields
  img_array[300:330, 250:] = 255
  img_array[355:390, 250:] = 255
  img_array[400:430, 185:] = 255
  img_array[450:490, 270:] = 255
  img_array[895:925, 155:180] = 255
  img_array[635:660, 155:180] = 255

  # Erase crosses
  img_array[630:660, 155:185] = 255
  img_array[735:765, 155:185] = 255
  img_array[820:850, 155:185] = 255
  img_array[895:925, 155:185] = 255
  img_array[1010:1040, 155:185] = 255
  img_array[1110:1140, 155:185] = 255
  img_array[1185:1215, 155:185] = 255

  # Erase Current city
  img_array[1260:1300, 220:527] = 255

  # Erase Current date
  img_array[1316:1339, 190:319] = 255

  # Erase Current time
  img_array[1315:1339, 409:500] = 255

  # Erase Current time under QR
  img_array[1442:1453, 948:1078] = 255

  # Erase QR
  img_array[1217:1430, 800:1100] = 255

  img = Image.fromarray(img_array)


  # Create crosses:
  def get_cross():
      image = Image.new('RGB', (30, 30), color=(255, 255, 255))
      image_draw = ImageDraw.Draw(image)
      image_font = ImageFont.truetype("Arial.ttf", 35)
      image_draw.text((3, -4), f'X', (0, 0, 0), font=image_font)
      return np.array(image)


  # travail-courses-sante-famille-sport-judiciaire-missions
  img_array = np.array(img)
  cross = get_cross()
  if "travail" in args.motif:
      img_array[630:660, 155:185] = cross
  if "courses" in args.motif:
      img_array[735:765, 155:185] = cross
  if "sante" in args.motif:
      img_array[820:850, 155:185] = cross
  if "famille" in args.motif:
      img_array[895:925, 155:185] = cross
  if "sport" in args.motif:
      img_array[1010:1040, 155:185] = cross
  if "judiciaire" in args.motif:
      img_array[1110:1140, 155:185] = cross
  if "missions" in args.motif:
      img_array[1185:1215, 155:185] = cross

  # QR CODE
  qr_text = f"Cree le: {args.leave_date} a {args.leave_hour};" \
            f" Nom: {args.last_name};" \
            f" Prenom: {args.first_name};" \
            f" Naissance: {args.birth_date} a {args.birth_city};" \
            f" Adresse: {args.address};" \
            f" Sortie: {args.leave_date} a {args.leave_hour};" \
            f" Motifs: {args.motif}"

  # qr_text="hyduzqhdzoiqd zqoihdpodqz"
  qr = qrcode.make(qr_text, border=0)
  qr = qr.resize((200, 200))
  qr = np.array(qr).astype(np.uint8) * 255
  qr = qr.repeat(3).reshape(qr.shape[0], qr.shape[1], -1)
  # img_array = np.array(img)
  img_array[1228:1428, 890:1090] = np.array(qr)
  img = Image.fromarray(img_array)

  # Fill args
  draw = ImageDraw.Draw(img)
  font = ImageFont.truetype("Arial.ttf", 22)
  font_small = ImageFont.truetype("Arial.ttf", 14)
  draw.text((260, 307), f'{args.first_name} {args.last_name}', (0, 0, 0), font=font)
  draw.text((255, 357), f'{args.birth_date}', (0, 0, 0), font=font)
  draw.text((190, 407), f"{args.birth_city}", (0, 0, 0), font=font)
  draw.text((280, 458), f"{args.address}", (0, 0, 0), font=font)

  draw.text((228, 1268), f"{args.current_city}", (0, 0, 0), font=font)
  draw.text((190, 1319), f"{args.leave_date}", (0, 0, 0), font=font)
  draw.text((411, 1318), f"{args.leave_hour}", (0, 0, 0), font=font)

  draw.text((948, 1443), f"{args.leave_date} à {args.leave_hour}", (0, 0, 0), font=font_small)

  plt.imsave("output-1.pdf", np.array(img), format="pdf")

  # ---------------------------
  #  Second Page (Big QR code)
  # ---------------------------
  img = np.array(Image.open('input-page2.png'))
  img[:] = 255
  qr = Image.fromarray(qr)
  qr = qr.resize((qr.size[0] * 3, qr.size[1] * 3))
  qr = np.array(qr)
  img[113:113 + qr.shape[0], 113:113 + qr.shape[1]] = qr
  plt.imsave("output-2.pdf", img, format="pdf")

  # --------------------
  # Merge PDFs
  # --------------------
  pdf1 = PdfFileReader('output-1.pdf')
  pdf2 = PdfFileReader('output-2.pdf')
  writer = PdfFileWriter()
  writer.addPage(pdf1.getPage(0))
  writer.addPage(pdf2.getPage(0))
  writer.write(open(f"{args.output}", "wb"))


start_date_object = datetime.strptime(args.start_date+' '+args.leave_hour, "%d/%m/%Y %H:%M")
end_date_object = datetime.strptime(args.end_date, "%d/%m/%Y")
hours = 1
hours_added = timedelta(hours = hours)
while(start_date_object != end_date_object): 
  args.leave_date=start_date_object.strftime("%d/%m/%Y")
  args.leave_hour=start_date_object.strftime("%H:%M")
  folder_str = "output/"+start_date_object.strftime("%Y-%m-%d")+'/'
  Path(folder_str).mkdir(parents=True, exist_ok=True)
  args.save_as = folder_str+start_date_object.strftime("%Y-%m-%d_%H:%M")
  if "travail" in args.motifs:
      args.output=args.save_as+"_travail.pdf"
      args.motif = "travail"
      generate()
  if "courses" in args.motifs:
      args.output=args.save_as+"_courses.pdf"
      args.motif = "courses"
      generate()
  if "sante" in args.motifs:
      args.output=args.save_as+"_sante.pdf"
      args.motif = "sante"
      generate()
  if "famille" in args.motifs:
      args.output=args.save_as+"_famille.pdf"
      args.motif = "famille"
      generate()
  if "sport" in args.motifs:
      args.output=args.save_as+"_sport.pdf"
      args.motif = "sport"
      generate()
  if "judiciaire" in args.motifs:
      args.output=args.save_as+"_judiciaire.pdf"
      args.motif = "judiciaire"
      generate()
  if "missions" in args.motifs:
      args.output=args.save_as+"_missions.pdf"
      args.motif = "missions"
      generate()
  # if "" in args.motifs:
  #     img_array[735:765, 155:185] = cross
  # if "sante" in args.motifs:
  #     img_array[820:850, 155:185] = cross
  # if "" in args.motifs:
  #     img_array[895:925, 155:185] = cross
  # if "sport" in args.motifs:
  #     img_array[1010:1040, 155:185] = cross
  # if "judiciaire" in args.motifs:
  #     img_array[1110:1140, 155:185] = cross
  # if "missions" in args.motifs:
  #     img_array[1185:1215, 155:185] = cross  print(start_date_object)
  start_date_object += hours_added