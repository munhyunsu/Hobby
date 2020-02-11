from PIL import Image, ImageDraw, ImageColor

WIDTH = 40*10
HEIGHT = 100*10
COLOR = ImageColor.getcolor('Red', 'RGBA')

img = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

for c in range(0, WIDTH+10, 10):
    draw.line(((c, 0), (c, HEIGHT)), fill=COLOR, width=1)
draw.line(((WIDTH-1, 0), (WIDTH-1, HEIGHT)), fill=COLOR, width=1)

for r in range(0, HEIGHT+10, 10):
    draw.line(((0, r), (WIDTH, r)), fill=COLOR, width=1)
draw.line(((0, HEIGHT-1), (WIDTH, HEIGHT-1)), fill=COLOR, width=1)

draw.line(((0, HEIGHT//2), (WIDTH, HEIGHT//2)), fill=COLOR, width=3)
draw.line(((WIDTH//2, 0), (WIDTH//2, HEIGHT)), fill=COLOR, width=3)

img.save('output.png')
