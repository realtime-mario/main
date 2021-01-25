#!/usr/bin/env python3
import sys
import PIL.Image
location = sys.argv[1]
image = PIL.Image.open('{}/tileset.png'.format(location))
def save(left, top, name):
    #name = 'night' + name
    left *= 64
    top *= 64
    cropped = image.crop((left, top, left + 64, top + 64))
    #if cropped.getpixel((0, 0))[0] == 192:return
    with open('{}/{}.json'.format(location, name), 'w') as f:
        f.write("""{
    "frames": 1,
    "solidity": 0,
    "slope": 0
}
""")
    cropped.save('{}/{}.png'.format(location, name))
save(0, 0, 'single')
save(1, 0, 'notright')
save(2, 0, 'topbottom')
save(3, 0, 'notleft')
save(4, 0, 'notbottom')
save(5, 0, 'leftright')
save(6, 0, 'nottop')
save(7, 0, 'bottomrightfull')
save(8, 0, 'bottomleftfull')
save(9, 0, 'toprightfull')
save(10, 0, 'topleftfull')
save(11, 0, 'bottomfull')
save(12, 0, 'topfull')
save(13, 0, 'rightfull')
save(14, 0, 'leftfull')
save(15, 0, 'middlefull')

save(0, 1, 'topcornerleft')
save(1, 1, 'topcornerright')
save(2, 1, 'bottomcornerleft')
save(3, 1, 'bottomcornerright')
save(4, 1, 'leftcornertop')
save(5, 1, 'rightcornertop')
save(6, 1, 'leftcornerbottom')
save(7, 1, 'rightcornerbottom')
save(8, 1, 'topleftcorner')
save(9, 1, 'toprightcorner')
save(10, 1, 'bottomleftcorner')
save(11, 1, 'bottomrightcorner')
save(12, 1, 'topcorner')
save(13, 1, 'bottomcorner')
save(14, 1, 'leftcorner')
save(15, 1, 'rightcorner')

save(0, 2, 'diagonal2corner')
save(1, 2, 'diagonal1corner')
save(2, 2, 'topleft')
save(3, 2, 'top')
save(4, 2, 'topright')
save(5, 2, 'left')
save(6, 2, 'middle')
save(7, 2, 'right')
save(8, 2, 'bottomleft')
save(9, 2, 'bottom')
save(10, 2, 'bottomright')
save(11, 2, 'bottomrightconcave')
save(12, 2, 'bottomleftconcave')
save(13, 2, 'toprightconcave')
save(14, 2, 'topleftconcave')
