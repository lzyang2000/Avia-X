from guizero import *
def lumi_change(slider_value):
    textbox_lumi.value = "1e+"+slider_value
    r_thresh = 243
    g_thresh = 231
    b_thresh = 211
    if int(slider_value) > 7:
    	app.bg = (243, 231, 211)
    else:
    	app.bg = 
def pressure_change(slider_value):
    textbox_pressure.value = slider_value
app = App()

# Define lumi input
lumi = Slider(app, command=lumi_change, horizontal = False, align = "left", start = 2, end = 10)
text_lumi = Text(app, text="Luminance", align="left")
textbox_lumi = TextBox(app, align = "left")

# Define pressure input
pressure = Slider(app, command=pressure_change, horizontal = False, align = "left", start = 10, end = 90)
text_pressure = Text(app, text="Pressure", align="left")
textbox_pressure = TextBox(app, align = "left")

# Define image input
face1 = Picture(app, image="./pr.gif", align = "left", width = 80, height = 80)
text_pic = Text(app, text="Input Pic", align="left")
# Define calculation button
button = PushButton(app, text="Output", align="left")

app.display()