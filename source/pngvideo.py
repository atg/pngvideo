import sys
import os
import png
import json
import re 

def standard_sorted(xs):
    def convert(text):
        return int(text) if text.isdigit() else text
    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)] 
    return sorted(xs, key=alphanum_key)

def listify(row):
    return [list(x) for x in row]
def box(rows):
    return [listify(zip(row[0::4], row[1::4], row[2::4], row[3::4])) for row in rows]

def unbox(rows):
    return [[item for sublist in row for item in sublist] for row in rows]

def main():
    try:
        frames_dir = sys.argv[1]
        output_path = sys.argv[2]
        json_output_path = sys.argv[3]
    except:
        print 'python pngvideo.py <frames> <output.png> <output.json>'
        sys.exit(1)
    
    # Read each frame
    frames = []
    
    for frame_name in standard_sorted(os.listdir(frames_dir)):
        if not frame_name.lower().endswith('.png'):
            continue
        
        frame_path = os.path.join(frames_dir, frame_name)
        frames.append({
            'originalPath': frame_path,
            'png': png.Reader(filename=frame_path),
        })
    
    # Check that we have any frames at all
    if not frames:
        print 'No frames found in source directory.'
        sys.exit(1)
    
    # Determine which frame is full
    frames[0]['isFull'] = True
    lastFull = frames[0]
    allrows = []
    lastFullPixels = box(lastFull['png'].asRGBA8()[2])
    allrows.extend(unbox(lastFullPixels))
    for f in frames[1:]:
        print f['originalPath']
        print f['png'].asRGBA8()[2]
        unboxedpixels = f['png'].asRGBA8()[2]
        pixels = box(unboxedpixels)
        
        isFull = False
        unchanged = 0
        changed = 0
        for i in xrange(len(lastFullPixels)):
            for j in xrange(len(lastFullPixels[i])):
                a = lastFullPixels[i][j]
                b = pixels[i][j]
                
                if b[3] == 255 or a[3] == 0 or a == b:
                    unchanged += 1
                    continue
                changed += 1
                print i
                print j
                print a
                print b
                isFull = True
                break
            if isFull:
                break
        
        # Delta encode
        if not isFull:
            for i in xrange(len(lastFullPixels)):
                for j in xrange(len(lastFullPixels[i])):
                    a = lastFullPixels[i][j]
                    b = pixels[i][j]
                    
                    if a == b:
                        pixels[i][j] = (0, 0, 0, 0)
                    
        else:
            lastFullPixels = pixels
        
        f['isFull'] = isFull
        allrows.extend(unbox(pixels))
    
    fullpng = png.from_array(allrows, 'RGBA;8')
    fullpng.save(output_path)
    
    json_output = {
        "width": len(allrows[0]) / 4,
        "height": len(allrows) / len(frames),
        "frame": [{ "isFull": f["isFull"], "duration": 1.0, } for f in frames],
    }
    
    with open(json_output_path, 'w') as jo:
        jo.write(json.dumps(json_output, sort_keys=True, indent=2 ))
    

if __name__ == '__main__':
    main()

