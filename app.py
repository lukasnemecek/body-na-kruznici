import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

# --- Sidebar / informace o aplikaci ---
author = "Lukáš Němeček"
contact = "285355@vutbr.cz"
technologies = ["Python 3.x", "Streamlit", "Numpy", "Matplotlib"]

st.sidebar.title("Informace")
st.sidebar.write(f"Autor: {author}")  
st.sidebar.write(f"Kontakt: {contact}")  
st.sidebar.write("Použité technologie:")
for tech in technologies:
    st.sidebar.write(f"- {tech}")

# ---- Nadpis aplikace ----
st.title("Body na kružnici – s osami a jednotkami")

# ---- Vstupní parametry ----
x0 = st.number_input("Souřadnice středu X", value=0.0)
y0 = st.number_input("Souřadnice středu Y", value=0.0)
r = st.number_input("Poloměr kružnice [m]", value=5.0, min_value=0.1)
n = st.number_input("Počet bodů", value=6, min_value=1, step=1)
color = st.color_picker("Barva bodů", "#ff0000")

# ---- Výpočet souřadnic bodů ----
angles = np.linspace(0, 2*np.pi, n, endpoint=False)
x = x0 + r * np.cos(angles)
y = y0 + r * np.sin(angles)

# ---- Vykreslení ----
fig, ax = plt.subplots()
ax.set_aspect("equal")

circle = plt.Circle((x0, y0), r, fill=False, linestyle="--", color="blue")
ax.add_artist(circle)

ax.scatter(x, y, color=color)

for i, (xi, yi) in enumerate(zip(x, y), start=1):
    ax.text(xi, yi, str(i), fontsize=10, ha="right")

ax.set_xlabel("x [m]")
ax.set_ylabel("y [m]")
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)

# ---- PDF export ----
buf = io.BytesIO()
fig.savefig(buf, format='png', dpi=150)
buf.seek(0)

pdf_buffer = io.BytesIO()
c = canvas.Canvas(pdf_buffer, pagesize=A4)
width, height = A4

# --- Text úlohy ---
c.setFont("Helvetica-Bold", 12)
c.drawString(50, height - 50, "Úloha: Body na kružnici")
c.setFont("Helvetica", 10)
c.drawString(50, height - 70, f"Stred: ({x0}, {y0})")
c.drawString(50, height - 85, f"Polomer: {r} m")
c.drawString(50, height - 100, f"Pocet bodu: {n}")
c.drawString(50, height - 115, f"Barva bodu: {color}")

# --- Text ze sidebaru ---
y_start = 140
c.drawString(50, height - y_start, f"Autor: Lukas Nemecek")
c.drawString(50, height - (y_start+15), f"Kontakt: {contact}")
c.drawString(50, height - (y_start+30), "Pouzite technologie:")
y_pos = height - (y_start+45)
for tech in technologies:
    c.drawString(60, y_pos, f"- {tech}")
    y_pos -= 15

# --- Vložení grafu pod text ---
graf_y = y_pos - 20  # mezera pod textem
graf_height = 400     # výška obrázku
c.drawImage(ImageReader(buf), 50, graf_y - graf_height, width=400, height=graf_height, preserveAspectRatio=True)

c.showPage()
c.save()
pdf_buffer.seek(0)

# Tlačítko pro stažení v sidebaru
st.sidebar.download_button(
    label="Stáhnout PDF",
    data=pdf_buffer,
    file_name="body_na_kruznici.pdf",
    mime="application/pdf"
)
