# We load an image and draw a yellow box somewhere in it
from matplotlib import pyplot as plt
from PIL import Image, ImageDraw

image_filename = '/home/okaliagd/PycharmProjects/Azure_Adventure/Images/happy_puppy.jpg'
image = Image.open(image_filename)

fig = plt.figure(figsize=(image.width/100, image.height/100))
plt.axis('off')

draw = ImageDraw.Draw(image)
color = 'cyan'

x, y = (100, 100)
width, height = (300, 300)
bounding_box = ((x,y),(x+width,y+height))

draw.rectangle(bounding_box, outline=color, width=5)

plt.annotate('box drawn in puppy image', (x, y), backgroundcolor=color)

plt.imshow(image)
plt.tight_layout(pad=0)
plt.show()

output_file = '/home/okaliagd/PycharmProjects/Azure_Adventure/Outputs/box_in_happy_puppy.jpg'
fig.savefig(output_file)
print('results saved in '+ output_file)
