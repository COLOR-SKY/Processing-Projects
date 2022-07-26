add_library("controlP5")

global cp5, src_img, threshold, degree, resol

def setup():
    size(500, 500)
    imageMode(CENTER)
    global cp5, src_img, threshold, degree, resol
    cp5 = ControlP5(this)
    src_img = loadImage("moon.jpg")
    src_img.resize(width, height)
    threshold = cp5.addSlider("threshold").setColorLabel(255).setPosition(20,20).setRange(0,255).setSize(100,10).setValue(128)
    resol = cp5.addSlider("resolution").setColorLabel(255).setPosition(20,40).setRange(1,10).setSize(100,10).setValue(3)
    degree = cp5.addKnob("degree").setRange(0,360).setValue(0).setPosition(20,60).setRadius(30).setDragDirection(Knob.VERTICAL)
    
def draw():
    # Draw rotated image in a new canvas
    pg = createGraphics(width * int(sqrt(2)), height * int(sqrt(2)))
    pg.beginDraw()
    pg.translate(width/2, height/2)
    pg.imageMode(CENTER);
    pg.rotate(radians(degree.getValue()))
    pg.image(src_img, 0, 0)
    pg.endDraw()
    
    # Read pixels line by line
    new_pg = createGraphics(width * int(sqrt(2)), height * int(sqrt(2)))
    new_pg.beginDraw()
    new_pg.noStroke()
    for y in range(0, pg.height, int(resol.getValue())):
        pixline = [pg.get(x, y) for x in range(0, pg.width, int(resol.getValue()))] 
        pixline = apply_sorter(pixline, normal_sorter)
        
        # Draw sorted pixel in a new canvas
        for x, pix in enumerate(pixline):
            new_pg.fill(pix)
            new_pg.rect(x * int(resol.getValue()), y, int(resol.getValue()), int(resol.getValue()))
    new_pg.endDraw()
    
    # Reverse rotation to display static image
    pushMatrix()
    translate(width/2, height/2)
    rotate(-radians(degree.getValue()))
    image(new_pg, 0, 0)
    popMatrix()
    
def normal_sorter(pixline):
    white_met = 0 # Keep track on # of black pixels met
    head = 0
    for i in range(len(pixline)):
        c = pixline[i]
        if alpha(c) == 0:
            white_met = 0
            continue
        if brightness(c) < threshold.getValue():
            c = color(0)
        else:
            c = color(255)
        if brightness(c) == 255:
            white_met += 1
            if white_met == 2:
                # sort pixels in between
                pixline[head:i] = sorted(pixline[head:i], key=lambda x: brightness(x))
                white_met = 0
            else:
                head = i
    return pixline
    
def apply_sorter(pixline, sorter):
    return sorter(pixline)

def keyPressed():
    if key == "s":
        saveFrame("####.png")
