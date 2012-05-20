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

def box(rows):
    return [zip(row[0::3], row[1::3], row[2::3], row[3::3]) for row in rows]

def unbox(rows):
    return [zip(*row) for row in rows]

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
    for f in frames[1:]:
        lastFullPixels = box(lastFull['png'].asRGBA8())
        pixels = box(f['png'].asRGBA8())
        isFull = False
        for i in xrange(len(lastFullPixels)):
            for j in xrange(len(lastFullPixels[i])):
                a = lastFullPixels[i][j]
                b = pixels[i][j]
                
                if b[3] != 255 and a[3] != b[3]:
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
        
        f['isFull'] = isFull
        allrows.extend(pixels)
    
    # 'RGBA;8'
    fullpng = png.from_array(allrows, 'RGBA;8')
    fullpng.save(output_path)
    
    json_output = {
        "width": len(allrows[0]),
        "height": len(allrows),
        "frames": [{ "isFull": f["isFull"], "duration": 1.0, } for f in frames],
    }
    
    with open(json_output_path, 'w') as jo:
        jo.write(json.dumps(json_output, separators=(',',':')))
    

if __name__ == '__main__':
    main()

