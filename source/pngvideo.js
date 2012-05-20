var PNGPlayer = function(_canvasid, _desc, _fullimg) {
    this.canvasid = _canvasid;
    this.frameDesc = _desc;
    this.currentImage = 0;
    this.isPlaying = false;
    this.fullImage = _fullimg;
    
    var el = document.getElementById(this.canvasid);
    if (el.width)
        el.width = this.frameDesc.width;
    if (el.height)
        el.height = this.frameDesc.height;
};
PNGPlayer.prototype.play = function() {
    
    var c = document.getElementById(this.canvasid);
    if (!c.getContext)
        return;
    
    this.isPlaying = true;
    this.playFrame();
};
PNGPlayer.prototype.playFrame = function() {
    if (!this.isPlaying)
        return;
    
    var frame = this.frameDesc.frame[this.currentImage];
    this.drawFrame(frame, this.currentImage);
    
    var duration = frame.duration;
    var self = this;
    window.setTimeout(function() {
        self.currentImage++;
        self.currentImage = self.currentImage % self.frameDesc.frame.length;
        self.playFrame();
    }, Math.round(duration * 1000));
};
PNGPlayer.prototype.drawFrame = function() {
    var lastFullFrameIndex = this.currentImage;
    
    // Go back until we have a full frame
    for (; lastFullFrameIndex >= 0; lastFullFrameIndex--) {
        if (this.frameDesc.frame[lastFullFrameIndex].isFull)
            break;
    }
    
    var ctx = document.getElementById(this.canvasid).getContext('2d');
    ctx.clearRect(0, 0, this.frameDesc.width, this.frameDesc.height);
    
    
    // Draw each frame
    for (var i = lastFullFrameIndex; i <= this.currentImage; i++) {
        if (i !== lastFullFrameIndex && i !== this.currentImage)
            continue;
        
        ctx.drawImage(this.fullImage, 0, - i * this.frameDesc.height);
    }
};

