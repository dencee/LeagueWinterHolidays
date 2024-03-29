from Snowball import Snowball

class SnowMan:
    
    def __init__(self, scale=1, body_color='#F0F0F0', x=None, y=None):
        self.scale = height / 800.0    # scale 1 for width=1200, height=800
        
        if x is None:
            self.x = width/2
        else:
            self.x = x
        
        if y is None:
            self.y = height
        else:
            self.y = y

        self.body_color = body_color
        self.inverted = color(255 - red(body_color), 255 - green(body_color), 255 - blue(body_color))

        self.radiusBot = int(175 * scale)
        self.radiusMid = int(140 * scale)
        self.radiusTop = int(100 * scale)
        self.offsetBot = self.y - self.radiusBot - 20
        self.offsetMid = self.offsetBot - (self.radiusBot)
        self.offsetTop = self.offsetMid - (2 * self.radiusTop)
  
        self.snowballSize = 0
        self.snowballX = 0
        self.snowballY = 0
        self.snowballThrowX = 0
        self.snowballThrowY = 0
        
        self.snowballs = list()
  
    def draw_body(self):
        pushStyle()
        
        noStroke()
        fill(self.body_color)
        ellipse(self.x, self.offsetBot, 2.15 * self.radiusBot, 2 * self.radiusBot)
        ellipse(self.x, self.offsetMid, 2.15 * self.radiusMid, 2 * self.radiusMid)
        ellipse(self.x, self.offsetTop, 2 * self.radiusTop, 2 * self.radiusTop)
        
        popStyle()
  
    def draw_nose(self):
        pushStyle()
    
        noseHeight = 0.2 * self.radiusTop
        noseLength = 1.2 * self.radiusTop
    
        noStroke()
        fill('#FFA500')
        triangle(self.x, self.offsetTop, self.x, self.offsetTop + noseHeight, self.x + noseLength, self.offsetTop)
     
        popStyle()
  
    def draw_eyes_mouth(self):
        pushStyle()
    
        radiusEyes = 0.25 * self.radiusTop
    
        # Inverted color
        noStroke()
        fill(self.inverted)
        ellipse(self.x - (self.radiusTop/4), self.offsetTop - (self.radiusTop/4), radiusEyes, radiusEyes)
        ellipse(self.x + (self.radiusTop/4), self.offsetTop - (self.radiusTop/4), radiusEyes, radiusEyes)
    
        radiusSmile = 1.25 * self.radiusTop
        smileWidth = 0.15 * self.radiusTop
    
        noFill()
        stroke(self.inverted)
        strokeWeight(smileWidth)
        arc(self.x, self.offsetTop, radiusSmile, radiusSmile, PI/4, 3*PI/4, OPEN)
        
        popStyle()
  
    def draw_hat(self):
        pushStyle()
    
        brimWidth = 2.5 * self.radiusTop
        brimHeight = 0.3 * self.radiusTop
        topWidth = 0.5 * brimWidth
        topHeight = self.radiusTop
    
        noStroke()
        fill(1)
        rect(self.x - brimWidth/2, self.offsetTop - self.radiusTop, brimWidth, brimHeight)
        rect(self.x - topWidth/2, self.offsetTop - self.radiusTop - topHeight, topWidth, topHeight)
    
        popStyle()

    def draw_buttons(self):
        pushStyle()
    
        buttonSize = 0.25 * self.radiusMid;
    
        stroke(self.inverted)
        strokeWeight(buttonSize)
    
        point(self.x, self.offsetMid)
        point(self.x, self.offsetMid - (0.5 * self.radiusMid))
        point(self.x, self.offsetMid + (0.5 * self.radiusMid))

        popStyle()

    def draw_arms(self):
        pushStyle()
    
        armY = self.offsetMid - (0.3 * self.radiusMid)
        leftArmX =  self.x - (0.9 * self.radiusMid)
        rightArmX = self.x + (0.9 * self.radiusMid)
        armLength = 1.2 * self.radiusMid
        armWidth =  0.1 * self.radiusMid
    
        stroke('#4C322B')
        strokeWeight(armWidth)
        strokeCap(ROUND)

        if abs(mouseX - leftArmX) == 0 or abs(mouseX - rightArmX) == 0:
            return

        # Left arm angle and lengths
        thetaL = atan( abs(mouseY - armY) / abs(mouseX - leftArmX) )
        leftHandX = armLength * cos(thetaL)
        leftHandY = armLength * sin(thetaL)

        # If mouseX is farther to the right, add to x position
        if mouseX < leftArmX:
            leftHandX = -leftHandX
        
        # If mouseY is farther below, add to the y position
        if mouseY < armY:
            leftHandY = -leftHandY

        # Same for right arm
        thetaR = atan( abs(mouseY - armY) / abs(mouseX - rightArmX) )
        rightHandX = armLength * cos(thetaR)
        rightHandY = armLength * sin(thetaR)
    
        if mouseX < rightArmX:
            rightHandX = -rightHandX
        
        if mouseY < armY:
            rightHandY = -rightHandY

        # Draw arms
        line(leftArmX, armY , leftArmX + leftHandX, armY + leftHandY) 
        line(rightArmX, armY , rightArmX + rightHandX, armY + rightHandY)
    
        if mousePressed and mouseButton == RIGHT:
            # Create a snowball in the snowman's hand!
            self.snowballSize += 1
      
            strokeWeight(3)
            stroke(0)
            fill(self.body_color)
            self.snowballThrowX = mouseX
            self.snowballThrowY = mouseY
            self.snowballX = leftArmX + leftHandX;
            self.snowballY = armY + leftHandY;
            circle(self.snowballX, self.snowballY, self.snowballSize);

        for ball in self.snowballs:
            ball.draw()
            
        if len(self.snowballs) > 0:
            self.snowballs[:] = [ball for ball in self.snowballs if ball.is_active]
    
        popStyle()
        
    def throw_snowball(self):
        if mouseButton == RIGHT:
            if self.snowballSize > 0:
                speed = constrain( 50 - (self.snowballSize * 0.2), 1, 50)
                new_snowball = Snowball(self.snowballSize, self.snowballX, self.snowballY, self.snowballThrowX, self.snowballThrowY, self.body_color, speed)
                self.snowballs.append(new_snowball);
                self.snowballSize = 0
