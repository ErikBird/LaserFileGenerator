from math import sqrt,sin,cos, radians
from flask import flash
import ezdxf as ez


logo_dims = (16.5, 2.5)

def generate_text(text, font):
    #http://ncplot.com/stickfont/stickfont.htm
    convert={}
    f = open("fonts/"+font+'.CHR', "r")
    for x in f:
        l=x.split()
        if len(l)>0:
            convert[l[0]]=l[1:]

    linestart=0
    maxX=0
    maxY=0
    lines=[]
    for c in text:
        if c==' ':
            linestart+= 10
        else:
            char=convert['CHR_'+format(ord(c), 'X')]
            points = []
            for el in char[1:]:
                if el[-1]==';':
                    p=el[:-1].split(',')
                    points.append((float(p[0])+linestart,float(p[1])))
                    lines.append(points)

                    points = []
                else:
                    p=el.split(',')
                    points.append((float(p[0])+linestart,float(p[1])))
                if points:
                    if points[-1][0]>maxX: maxX=points[-1][0]
                    if points[-1][1] > maxY: maxY = points[-1][1]

            lines.append(points)
            linestart+=float(char[0][:-1])
    return lines,(maxX,maxY)




def phonecase_outer_line( h1, w1, clip_width, h2, h4, h5, w4, clip_number, h6):
    '''

    :param modelspace:
    :param h1: One milimeter higher just to have some more protection
    :param w1:
    :param clip_width:
    :param h2:
    :param h4: Distance casebuttom to first clip
    :param h5: Distance last clip to top
    :param w4:
    :return:
    '''

    points = []


    # Fancy Top
    points.append((0, w4 + 5, 0, 0, 0.5))
    points.append((5, w4, 0, 0, 0))
    points.append((h5 - 4, w4, 0, 0, -0.5))
    points.append((h5, w4 - 4, 0, 0, 0))
    points.append((h5, 4, 0, 0, 0.5))

    points.append((h5 + 4, 0, 0, 0, 0))
    points.append((h5 + clip_number * clip_width - (clip_width / 4), 0, 0, 0, 0.2))

    points.append(((h1 + h5 + clip_number * clip_width - (clip_width / 4)) / 2, w4 / 2, 0, 0, -0.25))

    points.append((h1, w4))
    points.append((h1 + h2, w4))
    points.append((h1 + h2 + h4+clip_width/4, w4))
    points.extend(generate_clips((h1 + h2 + h4+clip_width/4, w4), True, False, clip_number, clip_width, h2)[:-1])

    points.append((h1 * 2 + h2 - h6, w4-2, 0, 0, -0.5))
    points.append((h1 * 2 + h2 - h6  + 2, w4 , 0, 0, 0))
    points.append((h1 * 2 + h2 - 5, w4 , 0, 0, 0.5))
    points.append((h1 * 2 + h2, w4 + 5, 0, 0, 0))

    # Opposite Site
    points.append((h1 * 2 + h2, w4 + w1 - 5, 0, 0, 0.5))
    points.append((h1 * 2 + h2 - 5, w4 + w1 , 0, 0, 0))
    points.append((h1 * 2 + h2 - h6 + 2, w4 + w1 , 0, 0, -0.5))
    points.append((h1 * 2 + h2 - h6, w4 + w1+2, 0, 0, 0))
    points.extend(
    generate_clips((h1 * 2 + h2 - h6, w4 + w1), False, True, clip_number, clip_width, h2)[1:])

    points.append((h1 + h2 + h4+clip_width/4, w4 + w1))
    points.append((h1 + h2, w4 + w1))
    points.append((h1, w4 + w1, 0, 0, -0.25))

    points.append(((h1 + h5 + clip_number * clip_width - (clip_width / 4)) / 2, w4 / 2 + w1 + w4, 0, 0, 0.2))
    points.append((h5 + clip_number * clip_width - (clip_width / 4), w1 + w4 * 2, 0, 0, 0))
    points.append((h5 + 4, w1 + w4 * 2, 0, 0, 0.5))
    points.append((h5, w1 + w4 * 2 - 4, 0, 0, 0))
    points.append((h5, w1 + w4 + 4, 0, 0, -0.5))
    points.append((h5 - 4, w1 + w4, 0, 0, 0))
    points.append((5, w1 + w4, 0, 0, 0.5))
    points.append((0, w1 + w4 - 5))
    points.append((0, w4 + 5, 0, 0, 0.5))

    return points

def generate_clips(last_p,right,up,n,clip_width, width):
    '''

    :param last_p: Last Point to append on
    :param right: X-Direction - TRUE for right and FALSE for left
    :param up: Y-Direction - TRUE for up and FALSE for down
    :param n: Number of clips
    :return:
    '''
    clips=[]
    y = 2 if up else -2
    width = width if up else -width
    x = clip_width if right else -clip_width

    for clip in range(n):
        clips.append((last_p[0],last_p[1]+y))
        clips.append((last_p[0]-(x/4), last_p[1] + y))
        clips.append((last_p[0] - (x/4), last_p[1] + width))
        clips.append((last_p[0] + (x / 4)*3, last_p[1] + width))
        clips.append((last_p[0] + (x / 4)*3, last_p[1] + y))
        clips.append((last_p[0] + (x / 2), last_p[1]+ y))
        clips.append((last_p[0] + (x / 2), last_p[1]))
        if clip!=n-1:clips.append((last_p[0] + x , last_p[1]))
        last_p=((last_p[0] + x , last_p[1]))
    return clips

def generate_wallet_one(text=''):
    #wallet = ez.new('R2010')
    wallet = ez.readfile("dxf_generator/dxf_templates/wallet_1.dxf")
    #importer = ez.Importer(source_drawing, wallet)right
    #if importer.is_compatible():
    #importer.import_modelspace_entities(query='*')
    textsize = generate_text(text, 'ROMAND')
    modelspace = wallet.modelspace()
    #Add Text
    lines, textsize = generate_text(text, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, 40, logo_dims[1] , 13.6)
    lines = linesPlace(lines,size,(60, 84),'middle','middle')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    logo_position = ((126, 60), ('right', 'bottom'))
    cut = len(lines)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=0)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})

    return wallet

def generate_wallet_two(text=''):
    #@TODO: Namen beim Herunterladen verbessern
    wallet = ez.readfile("dxf_generator/dxf_templates/wallet_2.dxf")
    modelspace = wallet.modelspace()
    #Add Text
    lines, textsize = generate_text(text, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, 40, logo_dims[1], 0)
    lines = linesPlace(lines,size,(20, 92),'left','top')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    logo_position = ((90, 60), ('left', 'bottom'))
    cut = len(lines)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=0)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})
    return wallet

def placeScaleRotate(points,place,scalex,scaley,angle):
    new_points=[]
    for p in points:
        x=p[0]*cos(radians(angle))-p[1]*sin(radians(angle))
        y=p[0]*sin(radians(angle))+p[1]*cos(radians(angle))
        new_points.append((place[0]+x*scalex,place[1]+y*scaley))
        #new_points.append((x,y))
    return new_points
def generate_pencilcase(text=''):
    pencilcase = ez.readfile("dxf_generator/dxf_templates/pencilcase.dxf")
    modelspace = pencilcase.modelspace()
    #Add Text
    lines, textsize = generate_text(text, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, 30, logo_dims[1], 180)
    lines = linesPlace(lines,size,(95,10),'middle','middle')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})


    logo_position = ((216.5, 172), ('middle', 'middle'))
    cut = len(lines)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=180)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})

    return pencilcase


def generate_glassescover(text=''):
    glassescover = ez.readfile("dxf_generator/dxf_templates/glassescover.dxf")
    modelspace = glassescover.modelspace()
    #Add Text
    lines, textsize = generate_text(text, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, 30, logo_dims[1], 180)
    lines = linesPlace(lines,size,(100,20),'middle','middle')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    logo_position = ((30, 47), ('left', 'top'))
    cut = len(lines)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=180)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})
    return glassescover


def generate_folding_line(modelspace,start, stop,reverse=False):

    # 5mm linie 3mm abstand 1mm abstand vertical
    dx = abs(start[0]-stop[0])
    dy = abs(start[1]-stop[1])
    line_n = int(sqrt(dx*dx+dy*dy)/8)
    if line_n>0:
        if reverse:
            for n in range(line_n):
                modelspace.add_line((start[0] - n * int(dx / line_n), start[1] - n * int(dy / line_n))
                                    , (start[0] - n * int(dx / line_n) - int(dx / line_n) * (5 / 8)
                                       , start[1] - n * int(dy / line_n) - int(dy / line_n) * (5 / 8)),
                                    dxfattribs={'color': 1})
        else:
            for n in range(line_n):
                modelspace.add_line((start[0] + n * int(dx / line_n), start[1] + n * int(dy / line_n))
                                    , (start[0] + n * int(dx / line_n) + int(dx / line_n) * (5 / 8)
                                       , start[1] + n * int(dy / line_n) + int(dy / line_n) * (5 / 8)),
                                    dxfattribs={'color': 1})
    else:
        print('to short for a line ')

def generate_watchstrap(top,buckle,length,text='',nail=2,version=1):
    watchstrap = ez.new('R2010')
    modelspace = watchstrap.modelspace()
    points=[]
    dist =14
    thick=3
    d = 3  # leatherthickness at the skin for the band-organizer
    #Two Sided Part
    points.append((0, 2, 0, 0, 0.5))
    points.append((2, 0, 0, 0, 0))
    points.append((dist-thick,0))
    points.append((dist,thick))
    points.append((dist+thick, thick))
    points.append((dist+thick,0))
    points.append((length+dist-thick,(top-buckle)/2))
    points.append((length + dist-thick, ((top - buckle) / 2)+thick))
    points.append((length + dist, ((top - buckle) / 2) + thick))
    points.append((length + dist+thick, ((top - buckle) / 2) ))
    if version ==1:
        points.append((length + dist *2-2, ((top - buckle) / 2),0,0,0.5))
        points.append((length + dist * 2, ((top - buckle) / 2)+2))
        points.append((length + dist * 2, top-((top - buckle) / 2) - 2,0,0,0.5))
        points.append((length + dist * 2-2, top-((top - buckle) / 2) ))
    elif version==2:
        points.append((length + dist * 2 - 2, ((top - buckle) / 2), 0, 0, 0.5))
        points.append((length + dist * 2, -2+((top - buckle)/2)))
        points.append((length + dist *2-2+19+d, -2+((top - buckle) / 2),0,0,0.5))
        points.append((length + dist * 2+19+d, -2+((top - buckle) / 2)+2))
        points.append((length + dist * 2+19+d, 2+top-((top - buckle) / 2) - 2,0,0,0.5))
        points.append((length + dist * 2-2+19+d, 2+top-((top - buckle) / 2) ))
        points.append((length + dist * 2, +2 + top-((top - buckle) / 2), 0, 0, 0.5))
        points.append((length + dist * 2 - 2, top - ((top - buckle) / 2)))
    else: print('Wrong Version')
    points.append((length + dist + thick, top-((top - buckle) / 2)))
    points.append((length + dist, top-((top - buckle) / 2) - thick))
    points.append((length + dist - thick, top-((top - buckle) / 2) - thick))
    points.append((length + dist - thick, top-(top - buckle) / 2))
    points.append((dist+thick,top))
    points.append((dist+thick,top-thick))
    points.append((dist,top-thick))
    points.append((dist-thick,top))
    points.append((2,top,0,0,0.5))
    points.append((0,top-2))
    points.append((0,2))
    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    #Version Specific stuff
    if version ==2:
        points = []
        points.append((length + dist *2-2+5, ((top - buckle) / 2)+1))
        points.append((length + dist * 2 - 2 + 5, top - ((top - buckle) / 2)-1, 0, 0, -0.5))
        points.append((length + dist * 2 - 2 + 10, top - ((top - buckle) / 2)-1))
        points.append((length + dist * 2 - 2 + 10, ((top - buckle) / 2) +1, 0, 0, -0.5))
        points.append((length + dist * 2 - 2 + 5, ((top - buckle) / 2)+1))
        modelspace.add_lwpolyline(points, dxfattribs={'color': 1})

        points = []
        points.append((length + dist *2-2+16, ((top - buckle) / 2)+1))
        points.append((length + dist * 2 - 2 + 16, top - ((top - buckle) / 2)-1, 0, 0, -0.5))
        points.append((length + dist * 2 - 2 + 21, top - ((top - buckle) / 2)-1))
        points.append((length + dist * 2 - 2 + 21, ((top - buckle) / 2) +1, 0, 0, -0.5))
        points.append((length + dist * 2 - 2 + 16, ((top - buckle) / 2)+1))
        modelspace.add_lwpolyline(points, dxfattribs={'color': 1})


    elif version ==1:
        points = []
        points.append((length + dist *2+4, -2+((top - buckle) / 2),0,0,-0.5))
        points.append((length + dist * 2+2, -2+((top - buckle) / 2)+2))
        points.append((length + dist * 2+2, 2+top-((top - buckle) / 2) - 2,0,0,-0.5))
        points.append((length + dist * 2+4, 2+top-((top - buckle) / 2) ))
        points.append((length + dist * 2 +2*d+15, 2 + top - ((top - buckle) / 2), 0, 0, -0.5))
        points.append((length + dist * 2 + 2+2*d+15, 2 + top - ((top - buckle) / 2) - 2))
        points.append((length + dist * 2 + 2+2*d+15, -2 + ((top - buckle) / 2) + 2, 0, 0, -0.5))
        points.append((length + dist * 2 +2*d+15, -2 + ((top - buckle) / 2)))
        points.append((length + dist * 2 + 4, -2 + ((top - buckle) / 2)))
        modelspace.add_lwpolyline(points, dxfattribs={'color': 1})

        points = []
        points.append((length + dist *2+2+d, ((top - buckle) / 2) + 1))
        points.append((length + dist *2+2+d, top - ((top - buckle) / 2) - 1, 0, 0, -0.5))
        points.append((length + dist *2+2+d+5, top - ((top - buckle) / 2) - 1))
        points.append((length + dist *2+2+d+5, ((top - buckle) / 2) + 1, 0, 0, -0.5))
        points.append((length + dist *2+2+d, ((top - buckle) / 2) + 1))
        modelspace.add_lwpolyline(points, dxfattribs={'color': 1})

        points = []
        points.append((length + dist *2+2+d+10, ((top - buckle) / 2) + 1))
        points.append((length + dist *2+2+d+10, top - ((top - buckle) / 2) - 1, 0, 0, -0.5))
        points.append((length + dist *2+2+d+15, top - ((top - buckle) / 2) - 1))
        points.append((length + dist *2+2+d+15, ((top - buckle) / 2) + 1, 0, 0, -0.5))
        points.append((length + dist *2+2+d+10, ((top - buckle) / 2) + 1))
        modelspace.add_lwpolyline(points, dxfattribs={'color': 1})



    # Hole Left
    points=[]
    points.append((thick+thick/3, thick,0,0,-0.5))
    points.append((thick,thick+thick/3,0))
    points.append((thick, top - thick + -thick/3, 0, 0, -0.5))
    points.append((thick,top-thick+-thick/3,0,0,-0.5))
    points.append((thick * 2-(thick/3*2), top - thick, 0, 0, -0.5))
    points.append((thick*2, top - thick-(thick/3*2),0,0,0.2))
    points.append((dist-thick, top /2,0,0,0.2))
    points.append((thick * 2,thick+(thick/3*2),0,0,-0.5))
    points.append((thick + thick / 3, thick))
    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    modelspace.add_line((dist-thick,top/2),(thick*2+top,top/2),dxfattribs={'color': 1})
    #Hole Right
    points=[]
    points.append((length + dist*2 - thick,((top - buckle) / 2)+thick+thick/3))
    points.append((length + dist*2 - thick,((top - buckle) / 2)+buckle-thick-thick/3,0,0,0.5))
    points.append((length + dist * 2 - thick- thick / 3, ((top - buckle) / 2) + buckle - thick,0,0,0.5 ))
    points.append((length + dist*2 - thick*2, ((top - buckle) / 2)+buckle - thick- (thick / 3)*2,0,0,-0.2))
    points.append((length + dist + thick, ((top - buckle) / 2)+buckle /2+nail/2,))
    points.append((length + dist -1, ((top - buckle) / 2)+buckle / 2 + nail/2,))
    points.append((length + dist -1, ((top - buckle) / 2)+buckle /2-nail/2))
    points.append((length + dist + thick, ((top - buckle) / 2)+buckle / 2 - nail/2, 0, 0, -0.2))
    points.append((length + dist*2 - thick * 2,((top - buckle) / 2)+thick+ (thick / 3)*2,0,0,0.5))
    #points.append((length + dist * 2 - thick * 2, ((top - buckle) / 2) + thick))
    points.append((length + dist * 2 - thick- thick / 3, ((top - buckle) / 2) + thick ,0,0,0.5))
    points.append((length + dist * 2 - thick, ((top - buckle) / 2) + thick + thick / 3))
    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    modelspace.add_line((length + dist -1,top/2),(length + dist+thick -top,top/2),dxfattribs={'color': 1})
    #One Sided Part
    sep=1
    points = []
    points.append((0, 2 + top + sep, 0, 0, 0.5))
    points.append((2, top + sep, 0, 0, 0))
    points.append((dist - thick, top + sep))
    points.append((dist, thick + top + sep))
    points.append((dist + thick, thick + top + sep))
    points.append((dist + thick, top + sep))
    points.append((length / 2 + dist, ((top - buckle) / 2) + top + sep))
    points.append((length, ((top - buckle) / 2) + top + sep, 0, 0, 0.03+(buckle-10)*0.008))
    points.append((length + dist + 28, top / 2 - 2 + top + sep, 0, 0, 0.5))
    points.append((length + dist + 28, top / 2 + 2 + top + sep, 0, 0, 0.03+(buckle-10)*0.008))
    points.append((length, top - ((top - buckle) / 2) + top + sep))
    points.append((length / 2 + dist, top - ((top - buckle) / 2) + top + sep))
    points.append((dist + thick, top + top + sep))
    points.append((dist + thick, top - thick + top + sep))
    points.append((dist, top - thick + top + sep))
    points.append((dist - thick, top + top + sep))
    points.append((2, top + top + sep, 0, 0, 0.5))
    points.append((0, top - 2 + top + sep))
    points.append((0, 2 + top + sep))
    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    #Hole Left
    points=[]
    points.append((thick+thick/3, thick+top+sep,0,0,-0.5))
    points.append((thick,thick+top+sep+thick/3,0))
    points.append((thick, top - thick+top+sep + -thick/3, 0, 0, -0.5))
    points.append((thick,top-thick+-thick/3+top+sep,0,0,-0.5))
    points.append((thick * 2-(thick/3*2), top - thick+top+sep, 0, 0, -0.5))
    points.append((thick*2, top - thick-(thick/3*2)+top+sep,0,0,0.2))
    points.append((dist-thick, top /2+top+sep,0,0,0.2))
    points.append((thick * 2,thick+(thick/3*2)+top+sep,0,0,-0.5))
    points.append((thick + thick / 3, thick+top+sep))
    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    modelspace.add_line((dist-thick,top/2+top+sep),(thick*2+top,top/2+top+sep),dxfattribs={'color': 1})
    #Holes
    for n in range(6):
        modelspace.add_circle((length + dist -(n*(5+nail)), top/2 + top + sep), nail / 2, dxfattribs={'color': 1})

    #Add Text
    lines, textsize = generate_text(text, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, length -(dist * 2.5 ), 6, 0)
    lines = linesPlace(lines,size,(length/2 + dist-3,top/2),'middle','middle')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    '''
    logo = ez.readfile("dxf_generator/dxf_templates/logo.dxf")
    logo_position = ((96, 60), ('middle', 'middle'))
    msp2 = logo.modelspace()
    lines1 = msp2.query('LWPOLYLINE')
    lines = [e.control_points for e in msp2.query('SPLINE')]
    cut = len(lines)
    lines.extend(lines1)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=0)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})'''
    return watchstrap

def phonecase_generate_holes( h1, w1, clip_width, h2, h4, h5, w4, clip_number, h6,modelspace):
    for n in range(clip_number):
        modelspace.add_lwpolyline([(h6 + n * 20, 2), (h6 + n * 20+10, 2), (h6 + n * 20+10, 6.5), (h6 + n * 20, 6.5), (h6 + n * 20, 2)],
                              dxfattribs={'color': 1})
        modelspace.add_lwpolyline([(h6 + n * 20, w1 + w4 * 2 - 6.5), (h6 + n * 20+10, w1 + w4 * 2 - 6.5), (h6 + n * 20+10, w1 + w4 * 2 - 2), (h6 + n * 20, w1 + w4 * 2 -2), (h6 + n * 20, w1 + w4 * 2 - 6.5)],
                              dxfattribs={'color': 1})

    # Generate Pottom Holes
    points = [(h1, w4 + 2 / 5 * w1), (h1, w4 + 3 / 5 * w1), (h1 + h2, w4 + 3 / 5 * w1), (h1 + h2, w4 + 2 / 5 * w1),
              (h1, w4 + 2 / 5 * w1)]
    distance = (2 / 5 * w1) - int((2 / 5 * w1) / 8) * 8
    generate_folding_line(modelspace, (h1, w4 + 2 / 5 * w1 - 2), (h1, w4 + 2), True)
    generate_folding_line(modelspace, (h1 - 1, w4 + 2 / 5 * w1 - 5), (h1 - 1, w4 + 5), True)
    generate_folding_line(modelspace, (h1 + h2, w4 + 2 / 5 * w1 - 2), (h1 + h2, w4 + 2), True)
    generate_folding_line(modelspace, (h1 + h2 + 1, w4 + 2 / 5 * w1 - 5), (h1 + h2 + 1, w4 + 5), True)
    generate_folding_line(modelspace, (h1, w4 + 3 / 5 * w1 + 2), (h1, w4 + w1 - 2))
    generate_folding_line(modelspace, (h1 - 1, w4 + 3 / 5 * w1 + 5), (h1 - 1, w4 + w1 - 5))
    generate_folding_line(modelspace, (h1 + h2, w4 + 3 / 5 * w1 + 2), (h1 + h2, w4 + w1 - 2))
    generate_folding_line(modelspace, (h1 + h2 + 1, w4 + 3 / 5 * w1 + 5), (h1 + h2 + 1, w4 + w1 - 5))

    modelspace.add_lwpolyline(points, dxfattribs={'color': 1})
    n_circle = int((w1 * 2 / 5 - h2) / h2)
    for n in range(n_circle):
        modelspace.add_circle((h1 + h2 / 2, w4 + 2 / 5 * w1 - h2 - h2 * n), h2 / 4, dxfattribs={'color': 1})
        modelspace.add_circle((h1 + h2 / 2, w4 + 3 / 5 * w1 + h2 + h2 * n), h2 / 4, dxfattribs={'color': 1})


def phonecase_folding_lines( h1, w1, clip_width, h2, h4, h5, w4, clip_number, h6,modelspace):
    generate_folding_line(modelspace, (h5 + 4,w4+1),(h1- (clip_width / 4)-1,w4+1))
    generate_folding_line(modelspace, (h5 + 7, w4), (h1 - (clip_width / 4) - 4, w4))
    generate_folding_line(modelspace, (h5 + 4, w4-1), (h1 - (clip_width / 4) - 4, w4-1))

    generate_folding_line(modelspace, (h5 + 4, w4+w1-1), (h1 - (clip_width / 4) - 1, w4+w1-1))
    generate_folding_line(modelspace, (h5 + 7, w4 +w1), (h1 - (clip_width / 4) - 4, w4 +w1))
    generate_folding_line(modelspace, (h5 + 4, w4 +w1+ 1), (h1 - (clip_width / 4) - 4, w4 +w1+ 1))

    generate_folding_line(modelspace, (h1 + h2 + h4, w4 + w1 - 1), (h1*2 + h2-h5, w4 + w1 - 1))
    generate_folding_line(modelspace, (h1 + h2 + h4-3, w4 + w1 - 2), (h1 * 2 + h2 - h5+3, w4 + w1 - 2))

    generate_folding_line(modelspace, (h1 + h2 + h4, w4 + 1), (h1*2 + h2-h5, w4 + 1))
    generate_folding_line(modelspace, (h1 + h2 + h4-3, w4 + 2), (h1 * 2 + h2 - h5+3, w4 + 2))
def getSize(lines):
    curr_x=0
    curr_y=0
    for line in lines:
    # Berechnet current x,y selbst
        for point in line:
            if point[0]>curr_x:
                curr_x=point[0]
            if point[1]>curr_y:
                curr_y=point[1]
    return (curr_x,curr_y)

def linesScaleRotate(lines,curr_dims,max_x,max_y,angle):
    # Berechnet scale
    scale = 1
    new_lines = []
    if curr_dims[0] > max_x:
        scale = max_x / curr_dims[0]
    if curr_dims[1] * scale > max_y:  # maximales Y sollten 6mm sein
        scale = max_y / curr_dims[1]

    overlap_x=0
    overlap_y=0
    x_size=0
    y_size=0
    for line in lines:#Arbeitet auf mehreren Elementen
        new_line=[]
        for point in line:
            # Scale und Rotate
            x = scale*(point[0] * cos(radians(angle)) - point[1] * sin(radians(angle)))
            y = scale*(point[0] * sin(radians(angle)) + point[1] * cos(radians(angle)))
            if x<overlap_x: overlap_x=x
            if y<overlap_y:overlap_y=y
            if x>x_size: x_size=x
            if y>y_size:y_size=y
            new_line.append((x,y))
        new_lines.append(new_line)

    #Adjust to fit in (0,0)
    for line in new_lines:
        for n,point in enumerate(line):
            line[n]=(point[0]-overlap_x,point[1]-overlap_y)
    return (x_size-overlap_x,y_size-overlap_y),new_lines


def linesPlace(lines,curr_dims,point,x_orientation,y_orientation):
    adj_x=0
    adj_y=0
    if y_orientation == 'bottom':adj_y=point[1]
    elif y_orientation == 'middle':adj_y=point[1]-curr_dims[1]/2
    elif y_orientation == 'top':adj_y=point[1]-curr_dims[1]
    else:print('Wrong y-orientation argument')
    if x_orientation == 'left':adj_x=point[0]
    elif x_orientation == 'middle':adj_x=point[0]-curr_dims[0]/2
    elif x_orientation == 'right':adj_x=point[0]-curr_dims[0]
    else:print('Wrong x-orientation argument')
    for line in lines:
        for n, point in enumerate(line):
            line[n] = (point[0] +adj_x, point[1] + adj_y)
    return lines


def generate_phonecase(height,width,depth, name):
    h1=height + 1
    h4 = 24
    h2=depth
    h5 = 10
    w1 = width+7 #Adjustment for width
    w4 = depth + 3
    clip_width = 20
    clip_number = int((h1 - h4 - h5) / clip_width)
    h5 += (h1- h4 - h5) % clip_width  # Distance to top gets increased
    h6 = h5 +clip_width/4

    phonecase = ez.new('R2010')
    modelspace = phonecase.modelspace()

    lwp=modelspace.add_lwpolyline(phonecase_outer_line( h1=h1, w1=w1, h2=h2, clip_width=clip_width,
                         h4=h4, h5=h5, w4=w4, clip_number=clip_number, h6=h6), dxfattribs={'color': 1})
    lwp.closed = True

    phonecase_generate_holes(h1=h1, w1=w1, h2=h2, clip_width=clip_width,
                             h4=h4, h5=h5, w4=w4, clip_number=clip_number, h6=h6, modelspace=modelspace)

    phonecase_folding_lines(h1=h1, w1=w1, h2=h2, clip_width=clip_width,
                            h4=h4, h5=h5, w4=w4, clip_number=clip_number, h6=h6, modelspace=modelspace)

    lines, textsize = generate_text(name, 'ROMAND')
    size,lines=linesScaleRotate(lines, textsize, max_x=(w1/5)*4, max_y=logo_dims[1], angle=270)
    lines = linesPlace(lines, size, (h1+h2+11, w4 + w1 / 2), x_orientation='right', y_orientation='middle')
    for l in lines:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})



    logo_position = ((h1-logo_dims[1]-11, w4 + w1 - logo_dims[0]-11), ('left', 'bottom'))
    cut = len(lines)
    lines = linesScaleRotate(lines, curr_dims=logo_dims, max_x=logo_dims[0], max_y=logo_dims[1], angle=90)[1]
    lines = linesPlace(lines, size, logo_position[0], x_orientation=logo_position[1][0],
                       y_orientation=logo_position[1][1])
    for l in lines[cut:]:
        modelspace.add_lwpolyline(l, dxfattribs={'color': 5})

    for line in lines[:cut]:
        spline = [(p[0], p[1], 0) for p in line]
        modelspace.add_open_spline(spline, dxfattribs={'color': 5})

    return phonecase






def get_infos(msp):
    for e in msp:
        '''
        try:
            for l in e.layers:
                print(l.dxf.name)
        except:
            print('No Layers')'''
        print(e.dxftype(), e.dxf.layer, e.dxf.color)
        if e.dxftype()=='LWPOLYLINE':
            [print(point) for point in e]
        elif e.dxftype() == 'SPLINE':
            [print(p) for p in e.control_points]
        else: print('Unknown dxf Entity:',e.dxftype())





#msp.add_line((0, 0), (10, 0))  # add a LINE entity
#dwg.saveas('line.dxf')
