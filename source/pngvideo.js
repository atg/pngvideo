var PNGPlayer = function(_canvasid, _desc) {
    this.canvasid = _canvasid;
    this.frameDesc = _desc;
    this.currentImage = 0;
    this.isPlaying = false;
    
    var el = document.getElementById(this.canvasid);
    if (el.width)
        el.width = this.frameDesc.frameWidth;
    if (el.height)
        el.height = this.frameDesc.frameHeight;
};
PNGPlayer.prototype.play = function() {
    
    var c = document.getElementById(this.canvasid);
    if (!c.getContext)
        return;
    
    this.isPlaying = true;
    this.playFrame();
};
PNGPlayer.prototype.playFrame = function() {
    if (!isPlaying)
        return;
    
    var frame = this.frameDesc.frame[this.currentImage];
    this.drawFrame(frame, this.currentImage);
    
    var delay = frame.delay;
    window.setTimeout(function() {
        this.currentImage++;
        this.playFrame();
    }, delay);
};
PNGPlayer.prototype.drawFrame = function() {
    var lastFullFrameIndex = this.currentImage;
    
    // Go back until we have a full frame
    for (; lastFullFrameIndex >= 0; lastFullFrameIndex--) {
        if (this.frameDesc.frame[lastFullFrameIndex].isFull)
            break;
    }
    
    var ctx = document.getElementById(this.canvasid).getContext('2d');
    ctx.clearRect(0, 0, frameDesc.frameWidth, frameDesc.frameHeight);
    
    // Draw each frame
    for (var i = lastFullFrameIndex; i <= this.currentImage; i++) {
        ctx.drawImage(this.fullImage, 0, i * this.frameDesc.frameHeight);
    }
};

