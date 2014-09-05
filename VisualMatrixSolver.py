import random
from Tkinter import *
import copy 
import numpy as np
import webbrowser




class VMS_top_down(object):
#     #def sizeChanged(self,event):
#           self.width = event.width - 4
#           self.height = event.height - 4
#           self.redrawALL()
     
    def timerFired(self):
        if self.timerCounter<75 and self.startCounter==1:
             self.timerCounter+=1
        if self.page=='animation page':
            self.redrawAnimation()
            delay = 2 # milliseconds
            def f():
               self.timerFired() # DK: define local fun in closure
            self.canvas.after(delay, f) 
            # pause, then call timerFired again
    def mousePressed(self,event):
        if self.openMouseMotion==True:
           if (self.isOnBoard(event.x, event.y)):
               (self.confirmRow, self.confirmCol) = \
               self.getCellFromLocation(event.x, event.y)
               
               self.openMouseMotion=False
               self.openTextField=True
               if self.playingWithGE==True : 
                  if self.page=='computing mode page':# GE compute
                     self.deltaDraw()
                  elif self.page=='view mode page': #GE view
                      self.deltaViewDraw()
               elif self.playingWithLU==True:  # LU
                   if self.confirmRow==self.confirmCol:
                      if self.page=='computing mode page': #lu compute
                         self.deltaDraw()
                      elif self.page=='view mode page':# GE view
                         self.deltaViewDraw()
                   else: # LU must be square matrix
                       self.redrawALL()
                       self.openMouseMotion=True
                       #self.mouseMotion(event)
                       self.openInstruction=True
                       self.instructionMsg=\
           'Sorry, you have to choose a square matrix for LU decomposition' 
                       self.drawInstruction()
               elif self.playingWithMatrixAd==True: # add
                   
                   if self.page=='view mode page':
                       self.deltaViewDrawAddition()
                   else:pass #self.page=='computing mode page':
                       #self.deltaDraw()   # back here
               elif self.playingWithMatrixMul==True:
                   if self.page=='view mode page':
                       if self.pickMulMatrix1==True:
                           # and self.pickMulMatrix2==False:
                         self.confirmMul1Row=self.confirmRow
                         self.confirmMul1Col=self.confirmCol
                         self.deltaViewDrawMulti()
                         self.pickMulMatrix1=False
                         #Fself.matrixBoundary=self.matrixBoundary1
                         self.pickMulMatrix2=True
                         self.openMouseMotion=True
                         
                         boardX0=self.matrixBoundary1[0]+\
                          (self.maxCol/2.0-(self.confirmCol+1)/2.0)\
                          *self.cellSize
                         boardY0=self.matrixBoundary1[1]+\
                          (self.maxRow/2.0-(self.confirmMul1Row+1)/2.0)\
                          *self.cellSize
                         boardX1=boardX0+self.confirmCol*self.cellSize
                         boardY1=boardY0+self.confirmRow*self.cellSize 
                         
                         self.drawPickingBlock(boardX0,boardY0,
                                               boardX1,boardY1)
                         
                       elif self.pickMulMatrix2==True:
                           self.deltaViewDrawMulti()
                           self.pickMulMatrix1=False 
                           self.pickMulMatrix2=False
                           #print self.confirmRow,self.confirmCol
                       else:
                           pass
                   else: #self.page=='computing mode page':
                       pass
                       #self.deltaComputeDrawAddition()   # back here
                       
           
           
               if self.page=='computing mode page':            
                   if self.playingWithGE==True:
                      self.openInstruction=True
                      self.instructionMsg=\
             'Excellent! You pick a %d x %d matrix, now fill the blank' \
              %(self.confirmRow+1,self.confirmCol+1)
                      self.drawInstruction()
                   elif self.playingWithLU==True and \
                   self.confirmRow==self.confirmCol:
                       self.openInstruction=True
                       self.instructionMsg=\
        'Excellent! You pick a %d x %d matrix, now fill the blank' \
             %(self.confirmRow+1,self.confirmCol+1)
                       self.drawInstruction()
                       
                       
                   elif self.playingWithMatrixAd==True:
                       self.openInstruction=True
                       self.instructionMsg=\
             'Excellent! You pick a %d x %d matrix, now fill the blank' \
              %(self.confirmRow+1,self.confirmCol+1)
                       self.drawInstruction()
                     
               elif self.page=='view mode page':
                   if self.playingWithGE==True:
                      self.openInstruction=True
                      self.instructionMsg=\
                        '          Excellent! You pick a %d x %d matrix' \
       %(self.confirmRow+1,self.confirmCol+1)
                      self.drawInstruction()
                   elif self.playingWithLU==True \
                   and self.confirmRow==self.confirmCol:
                       self.openInstruction=True
                       self.instructionMsg=\
                         'Excellent! You pick a %d x %d matrix'\
             %(self.confirmRow+1,self.confirmCol+1)
                       self.drawInstruction()
    
    
    
    
    
    
    
    def mouseMotion(self,event):
        if self.openMouseMotion==True:
            #print self.pickMulMatrix2
            #print self.matrixBoundary1
            #print self.isOnBoard(event.x, event.y)
            if (self.isOnBoard(event.x, event.y)): 
                    (self.shadowRow, self.shadowCol) \
                    = self.getCellFromLocation(event.x, event.y)
                    #print '2',self.pickMulMatrix2
                    if self.pickMulMatrix2==False:
                       self.drawPickSizeMatrix(self.matrixBoundary[0],\
                                               self.matrixBoundary[1],\
                                            self.matrixBoundary[2],\
                                            self.matrixBoundary[3])
                    
                    elif self.pickMulMatrix2==True: 
                         boardX0=self.matrixBoundary1[0]+\
                          (self.maxCol/2.0-(self.confirmCol+1)/2.0)\
                          *self.cellSize
                         boardY0=self.matrixBoundary1[1]+\
                          (self.maxRow/2.0-(self.confirmMul1Row+1)/2.0)\
                          *self.cellSize
                         boardX1=boardX0+self.confirmCol*self.cellSize
                         boardY1=boardY0+self.confirmRow*self.cellSize 
                         
                         self.drawPickingBlock(boardX0,boardY0,
                                               boardX1,boardY1)
                         
                        
                        
            
    def keyPressed(self,event):
        if self.page=='animation page':
           if event.keysym == "Left":
                if self.step>0:  self.step-=1
           if event.keysym == "Right":
                if self.step<self.maxStep: 
                    self.step+=1
                    self.startCounter=1 
                    self.timerCounter=0    
           self.redrawAnimation() 
           if (event.char == "b"):
               self.initPage1()
    def initWelcomePage(self):
        self.title='Visual Matrix Solver'
        self.page='welcome page'
        self.welcomeImage = PhotoImage(file="/images/welcomeImage.gif")
        self.buttonWelcome1Image=PhotoImage(file='/images/B1.gif')
        self.buttonWelcome2Image=PhotoImage(file='/images/B2.gif')
        
        self.buttonHelp=PhotoImage(file='/images/B3.gif')
        self.buttonBack=PhotoImage(file='/images/B4.gif')
        self.buttonAddMatrix=PhotoImage(file='/images/B5.gif')
        self.buttonMulMatrix=PhotoImage(file='/images/B6.gif')
        self.buttonGE=PhotoImage(file='/images/B7.gif')
        self.buttonImageShowAns=PhotoImage(file='/images/B8.gif')
        self.buttonImageNextStep=PhotoImage(file='/images/B9.gif')
        
        self.buttonImageLU=PhotoImage(file='/images/B10.gif')
        self.buttonImagePrevStep=PhotoImage(file='/images/B11.gif')
        self.buttonImageYesMark=PhotoImage(file='/images/B12.gif')
        
        #self.page1Image=PhotoImage(file='2Demo.gif') # demo
        self.page1Image=PhotoImage(file='/images/page1.gif') # demo
        self.page2Image=PhotoImage(file='/images/page2.gif') # computation
        self.page3Image=PhotoImage(file='/images/page3.gif')
        
        
        
        self.openMouseMotion=False
        self.redrawALL()
        pass
    def initPage1(self): #view mode
        self.title1='Demo Mode'
        self.page='view mode page'
        self.redrawALL()
        
        self.playingWithGE=False
        self.playingWithLU=False
        self.playingWithMatrixAd=False
        self.playingWithMatrixMul=False
        self.pickMulMatrix1=False # use to identify matrix in multiply
        self.pickMulMatrix2=False
    
        
        self.openInstruction=True
        self.instructionMsg='Please choose what you want to learn'+\
                             ' from the following buttons.'
        self.drawInstruction()

    
    
    def initPage2(self): #compute mode
        self.title2='Computing Mode'
        self.page='computing mode page'
        self.redrawALL()
        self.playingWithGE=False
        self.playingWithLU=False
        self.playingWithMatrixAd=False
        self.playingWithMatrixMul=False
        
        self.geProblemMatrix=False
        
        self.openInstruction=True
        self.instructionMsg='                         GE or LU?'
        self.drawInstruction()
    
    def initAnimationPage(self):
        self.title3='Animation'
        self.page='animation page'
        

        self.geAnimationPage=True
        self.startCounter=0
        self.timerCounter=0
        self.redrawALL()
        
        

    
    def callGE(self):
        # call this funtion when press the GE button in compute mode
        # first reveal a matrix for users to choose size 
        
        #GE pickSize Matrix location
        #GE board boundary
        self.playingWithGE=True
        self.playingWithLU=False
        self.playingWithMatrixAd=False
        self.playingWithMatrixMul=False
        x0=2*self.boardMargin+(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        y0=self.boardMargin*3+1*self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0
        #self.singularMatrixError=False
        self.matrixBoundary=(x0,y0,x1,y1) 
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True # after this I get shadowRol and shadowCol
        self.openTextField=False
        
        #instruction
        self.openInstruction=True
        self.instructionMsg=\
        'GE? You are insane...pick matrix size and press Left Mouse.'
        self.drawInstruction()
        
    def callViewGE(self):
        self.playingWithGE=True
        self.playingWithLU=False
        x0=2*self.boardMargin+(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        y0=self.boardMargin*3+self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0

        self.matrixBoundary=(x0,y0,x1,y1) 
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True # after this I get shadowRol and shadowCol
        self.openTextField=False
        
        #instruction
        self.openInstruction=True
        self.instructionMsg=\
        'GE? You are insane...now pick matrix size and press left'
        self.drawInstruction()
    
        
    
    def callViewMatrixAddition(self):
        #in view mode, when I click matrix addition button,
        # get into this function
        
        self.playingWithMatrixAd=True
        self.playingWithGE=False
        self.playingWithLU=False
        self.playingWithMatrixMul=False
        x0=2*self.boardMargin#+(self.maxCol+2)*self.cellSize
        x0_1=2*self.boardMargin+(self.maxCol+2)*self.cellSize
        x0_2=2*self.boardMargin+2*(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        x1_1=x0_1+self.cellSize*self.maxCol
        x1_2=x0_2+self.cellSize*self.maxCol
        y0=self.boardMargin*3+self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0

        self.matrixBoundary=(x0,y0,x1,y1) 
        # matrix boundary for different case.... right now ad
        self.matrixBoundary1=(x0_1,y0,x1_1,y1) 
        # boundary of matrix in the middle
        self.matrixBoundary2=(x0_2,y0,x1_2,y1) 
        # boundary of matrix in the right
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True
         # after this I get shadowRol and shadowCol
        self.openTextField=False
        self.pickMulMatrix2=False
        self.openInstruction=True
        self.instructionMsg=\
        'Please use the board above to pick the size of first matrix,\n' +\
        'and press left mouse to confirm.'
        self.drawInstruction()
        pass
        
    
    def callViewMatrixMul(self):
        # back here
        #in view mode, when I click matrix multiplication button,
        # get into this function
        self.playingWithMatrixAd=False
        self.playingWithGE=False
        self.playingWithLU=False
        self.playingWithMatrixMul=True
        
        x0=2*self.boardMargin#+(self.maxCol+2)*self.cellSize
        x0_1=self.boardMargin+(self.maxCol+2)*self.cellSize
        x0_2=self.boardMargin+2*(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        x1_1=x0_1+self.cellSize*self.maxCol
        x1_2=x0_2+self.cellSize*self.maxCol
        y0=self.boardMargin*3+self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0

        self.matrixBoundary=(x0,y0,x1,y1) 
        # matrix boundary for different case.... right now ad
        self.matrixBoundary1=(x0_1,y0,x1_1,y1) 
        # boundary of matrix in the middle
        self.matrixBoundary2=(x0_2,y0,x1_2,y1) 
        # boundary of matrix in the middle
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True
         # after this I get shadowRol and shadowCol
        self.pickMulMatrix1=True
        self.openTextField=False
        self.pickMulMatrix2=False

        self.openInstruction=True #mark
        self.instructionMsg=\
        'Please use the board above to pick the size of first matrix, ' +\
        'and press left mouse to confirm.'
        self.drawInstruction()
        
        pass
        
        pass    
            
   
    def callLU(self):
        self.playingWithLU=True
        self.playingWithGE=False
        x0=2*self.boardMargin+(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        y0=self.boardMargin*2+self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0
        #self.singularMatrixError=False
        self.matrixBoundary=(x0,y0,x1,y1) 
        # matrix boundary for different case.... right now GE
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True 
        # after this I get shadowRol and shadowCol
        self.openTextField=False
        
        #instruction
        self.openInstruction=True
        self.instructionMsg=\
        'LU? insane again...pick matrix size and press Left Mouse.'
        self.drawInstruction()
        
    def callViewLU(self):
        
        self.playingWithLU=True
        self.playingWithGE=False
        x0=2*self.boardMargin+(self.maxCol+2)*self.cellSize
        x1=x0+self.cellSize*self.maxCol
        y0=self.boardMargin*2+self.titleMargin
        y1=y0+self.cellSize*self.maxRow
        self.step=0
        #self.singularMatrixError=False
        self.matrixBoundary=(x0,y0,x1,y1) 
        # matrix boundary for different case.... right now GE
        self.redrawALL() # think about this again.
        self.drawPickSizeMatrix(x0,y0,x1,y1)
        self.openMouseMotion=True 
        # after this I get shadowRol and shadowCol
        self.openTextField=False
        
        #instruction
        self.openInstruction=True
        self.instructionMsg=\
        'LU? insane again...now pick matrix size and press left'
        self.drawInstruction()    
   
        
        
    def getMatrixFromBoxField(self):
        # after clicking OK, I get matrix from users input , 
        #then I need to draw the matrix again
        
        self.matrixGetFromBoxField=\
        np.zeros((self.confirmRow+1,self.confirmCol+1))
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                 self.matrixGetFromBoxField[row][col]=\
                 round(self.geEnt[row,col].get(),2)
        # here I draw the confirmedMatrix
        #self.stepList=[]
        #self.stepList.append(copy.deepcopy(self.matrixGetFromBoxField))
        # initiate stepList matrix pool
        self.geProblemMatrix=False
        if self.confirmRow>self.confirmCol:
            for i in xrange(self.confirmCol+1):
                if self.matrixGetFromBoxField[i][i]==0:
                    self.geProblemMatrix=True # back here
        
        else:
            for i in xrange(self.confirmRow+1):
                if self.matrixGetFromBoxField[i][i]==0:
                    self.geProblemMatrix=True # back here
        

            
        self.redrawALL()
        if self.playingWithGE==True:
            self.drawStepThroughButton()
            self.drawStepBackButton()
            self.drawAnswerButton()
        elif self.playingWithLU==True:
            self.drawStepThroughButton()
            self.drawStepBackButton()
            self.drawAnswerButton()
        
        if self.geProblemMatrix==False:
            self.drawConfirmedMatrix()
        #if np.linalg.det(self.matrixGetFromBoxField)==0:
         #  self.singular=True # back here
        
        if self.playingWithGE==True:
              self.openMouseMotion=False
              self.openInstruction=True
              if self.geProblemMatrix!=True:
                 self.instructionMsg=\
              """you can get answer if you treat me as a calculator...
               or you can track each step on the way"""
              else:
                  self.instructionMsg=\
                  "Sorry, that is a singular matrix. Please choose another one."
                  self.openMouseMotion=True
                  self.canvas.delete(self.buttonShowAnswer,\
                                     self.buttonNextStep,self.buttonBackStep)
                  
              self.drawInstruction()
              
        
        elif self.playingWithLU==True:
              self.openMouseMotion=False
              self.openInstruction=True
              if self.geProblemMatrix!=True:
                 self.instructionMsg=\
              """you can get answer if you treat me as a calculator...
               or you can track each step on the way"""
              else:
                  self.instructionMsg=\
                  "Sorry, that is singular. Please choose another one."
                  self.openMouseMotion=True
                  self.canvas.delete(self.buttonShowAnswer,\
                                     self.buttonNextStep,self.buttonBackStep)
                  self.drawInstruction()
              
              
#               boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
#                     (self.confirmCol+1)/2.0)*self.cellSize
#               boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
#                     (self.confirmRow+1)/2.0)*self.cellSize
#               boardX1=boardX0+self.confirmCol*self.cellSize
#               boardY1=boardY0+self.confirmRow*self.cellSize
#               self.drawPickSizeMatrix(boardX0, boardY0, boardX1, boardY1)

    
    
    def geStepThrough(self):
        self.gaussElimination()
        self.maxStep=len(self.stepList)
        
            
        if self.step==-1:
            self.step+=1
        if 0<=self.step<self.maxStep:
            
            #self.lastStepMatrix=self.stepMatrix[self.step-1]
            
            if self.confirmRow+1==1: # rows=1 instructions
                self.instructionMsg='There is really no GE happening'
                self.stepMatrix=self.stepList[self.step]
                self.step+=1
            
            elif self.confirmRow+1==2: # rows=2 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix,Next step,row 1 is divided by %0.2f"""\
                     %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    """     Next Step, row 2 - row 1 x  %0.2f"""\
                     %(self.matrixGetFromBoxField[1][0])
                elif self.step==2:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step+=1
            
            
            elif self.confirmRow+1==3: # rows=3 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix,Next step,row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x  %0.2f'\
                     %(self.matrixGetFromBoxField[1][0])
                elif self.step==2:
                    self.instructionMsg=\
                    '     Next Step, row 3 - row 1 x  %0.2f ' \
                    %(self.matrixGetFromBoxField[2][0]) 
                elif self.step==3:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by  %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif self.step==4:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 3 - row 2 x  %0.2f'\
                     %(self.stepMatrix[2][1])  
                elif self.step==5:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step+=1
            
            elif self.confirmRow+1==4: # rows=4 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix,Next step,row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x  %0.2f' \
                    %(self.matrixGetFromBoxField[1][0])
                elif 1<self.step<4:
                    self.instructionMsg=\
                    '     Next Step, row %d - row 1 x  %0.2f '\
                     %(self.step+1,self.matrixGetFromBoxField[self.step][0]) 
                elif self.step==4:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by  %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif 4<self.step<7:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 2 x  %0.2f'\
                     %(self.step-2,self.stepMatrix[self.step-3][1])  
                elif self.step==7:
                    self.instructionMsg=\
                    '     Next Step, row 3 is divided by  %0.2f'\
                    %(self.stepMatrix[2][2])
                elif self.step==8:
                    self.instructionMsg=\
                    '     Next Step, row 4  - row 3 x  %0.2f'\
                    %(self.stepMatrix[3][2])
                elif self.step==9:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step+=1
            
            elif self.confirmRow+1==5: # rows=5 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix,Next step,row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x  %0.2f'\
                     %(self.matrixGetFromBoxField[1][0])
                elif 1<self.step<5:
                    self.instructionMsg=\
                    '     Next Step, row %d - row 1 x  %0.2f ' \
                    %(self.step+1,self.matrixGetFromBoxField[self.step][0]) 
                elif self.step==5:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by  %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif 5<self.step<9:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 2 x  %0.2f'\
                     %(self.step-3,self.stepMatrix[self.step-4][1])  
                elif self.step==9:
                    self.instructionMsg=\
                    '     Next Step, row 3 is divided by  %0.2f'\
                    %(self.stepMatrix[2][2])
                elif 9<self.step<12:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 3 x  %0.2f' \
                    %(self.step-6,self.stepMatrix[self.step-7][2]) 
                elif self.step==12:
                    self.instructionMsg=\
                    '     Next Step, row 4 is divided by  %0.2f'\
                    %(self.stepMatrix[3][3])
                elif self.step==13:
                    self.instructionMsg=\
                    '     Next Step, row 5  - row 4 x  %0.2f'\
                    %(self.stepMatrix[4][3])
                elif self.step==14:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step+=1
           
        
        self.redrawALL()# self.matrix
        self.drawAnswerButton()
        self.drawStepThroughButton()
        self.drawStepBackButton()
        self.drawStepMatrix()
        self.openInstruction=True
        
        
        self.drawInstruction()

        
     
    def geStepBack(self):
        self.gaussElimination()
        self.maxStep=len(self.stepList)
        if self.step==self.maxStep:
            self.step-=1
        if 0<=self.step<self.maxStep:
            if self.confirmRow+1==1: # rows=1 instructions
                self.instructionMsg='There is really no GE happening'
                self.stepMatrix=self.stepList[self.step]
                self.step-=1
            
            elif self.confirmRow+1==2: # rows=2 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix, Next step, row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x %0.2f'\
                     %(self.matrixGetFromBoxField[1][0])
                elif self.step==2:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step-=1
            
            
            elif self.confirmRow+1==3: # rows=3 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix, Next step, row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x %0.2f'\
                     %(self.matrixGetFromBoxField[1][0])
                elif self.step==2:
                    self.instructionMsg=\
                    '     Next Step, row 3 - row 1 x %0.2f '\
                     %(self.matrixGetFromBoxField[2][0]) 
                elif self.step==3:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif self.step==4:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 3 - row 2 x %0.2f' \
                    %(self.stepMatrix[2][1])  
                elif self.step==5:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step-=1
            
            elif self.confirmRow+1==4: # rows=4 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix, Next step, row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x %0.2f' \
                    %(self.matrixGetFromBoxField[1][0])
                elif 1<self.step<4:
                    self.instructionMsg=\
                    '     Next Step, row %d - row 1 x %0.2f '\
                     %(self.step+1,self.matrixGetFromBoxField[self.step][0]) 
                elif self.step==4:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif 4<self.step<7:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 2 x %0.2f' \
                    %(self.step-2,self.stepMatrix[self.step-3][1])  
                elif self.step==7:
                    self.instructionMsg=\
                    '     Next Step, row 3 is divided by %0.2f'\
                    %(self.stepMatrix[2][2])
                elif self.step==8:
                    self.instructionMsg=\
                    '     Next Step, row 4  - row 3 x %0.2f'\
                    %(self.stepMatrix[3][2])
                elif self.step==9:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step-=1
            
            elif self.confirmRow+1==5: # rows=5 instructions
                if self.step==0:
                    self.instructionMsg=\
"""Now you see the original matrix, Next step, row 1 is divided by %0.2f"""\
                    %(self.matrixGetFromBoxField[0][0])
                elif self.step==1:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step, row 2 - row 1 x %0.2f' \
                    %(self.matrixGetFromBoxField[1][0])
                elif 1<self.step<5:
                    self.instructionMsg=\
                    '     Next Step, row %d - row 1 x %0.2f '\
                     %(self.step+1,self.matrixGetFromBoxField[self.step][0]) 
                elif self.step==5:
                    self.instructionMsg=\
                    '     Next Step, row 2 is divided by %0.2f'\
                    %(self.stepMatrix[1][1]) 
                elif 5<self.step<9:# or self.step==1+self.confirmRow:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 2 x %0.2f' \
                    %(self.step-3,self.stepMatrix[self.step-4][1])  
                elif self.step==9:
                    self.instructionMsg=\
                    '     Next Step, row 3 is divided by %0.2f'\
                    %(self.stepMatrix[2][2])
                elif 9<self.step<12:
                    self.instructionMsg=\
                    '     Next Step ,row %d - row 3 x %0.2f' \
                    %(self.step-6,self.stepMatrix[self.step-7][2]) 
                elif self.step==12:
                    self.instructionMsg=\
                    '     Next Step, row 4 is divided by %0.2f'\
                    %(self.stepMatrix[3][3])
                elif self.step==13:
                    self.instructionMsg=\
                    '     Next Step, row 5  - row 4 x %0.2f'\
                    %(self.stepMatrix[4][3])
                elif self.step==14:
                    self.instructionMsg='     Well Done!'      
                self.stepMatrix=self.stepList[self.step]
                self.step-=1            
            
            
        self.redrawALL()
        self.drawAnswerButton()
        self.drawStepThroughButton()
        self.drawStepBackButton()
        self.drawStepMatrix()
        self.openInstruction=True
            
        self.drawInstruction()
        
    
    def luStepThrough(self):
        self.luDecomposition()
        self.maxLStep=len(self.stepLlist)
        self.maxUStep=len(self.stepUlist)
        self.maxStep=self.maxUStep=self.maxLStep
            
        if self.step==-1:
            self.step+=1
        if 0<=self.step<self.maxStep:
                self.instructionMsg='      Press Next Step or Previous Step to iterate.'
                self.stepLMatrix=self.stepLlist[self.step]
                self.stepUMatrix=self.stepUlist[self.step]
                self.step+=1
        self.redrawALL()
        self.drawAnswerButton()
        self.drawStepThroughButton()
        self.drawStepBackButton()
        self.drawLUStepMatrix()
        self.drawConfirmedMatrix()
        self.openInstruction=True
        self.drawInstruction()

    def luStepBack(self):
        self.luDecomposition()
        self.maxLStep=len(self.stepLlist)
        self.maxUStep=len(self.stepUlist)
        self.maxStep=self.maxUStep=self.maxLStep
            
        if self.step==self.maxStep:
            self.step-=1
        if 0<=self.step<self.maxStep:
                self.instructionMsg='Look carefully, step%d'%(self.step)
                self.stepLMatrix=self.stepLlist[self.step]
                self.stepUMatrix=self.stepUlist[self.step]
                self.step-=1
        self.redrawALL()
        self.drawAnswerButton()
        self.drawStepThroughButton()
        self.drawStepBackButton()
        self.drawLUStepMatrix()
        self.drawConfirmedMatrix()
        self.openInstruction=True
        self.drawInstruction()
        
    def geShowAnswer(self):
        try:
            self.gaussElimination()
            self.answerMatrix=self.stepList[-1]
            self.drawAnswerMatrix()
        except:
            pass
        
#         self.openInstruction=True
#         self.instructionMsg='The answer of GE '
#         self.drawInstruction()
        
        
    def luShowAnswer(self):

        self.luDecomposition()
        self.answerLMatrix=self.stepLlist[-1]
        self.answerUMatrix=self.stepUlist[-1]
        self.drawLUAnswerMatrix()
        
    def addShowAnswer(self):
        #back here
        #self.canvas.delete()
        self.answerMatrix=self.viewAdmatrix+self.viewAdmatrix1
        self.drawAddAnswerMatrix()
        self.drawViewStepThroughButton() # animation viewing button
        
        self.canvas.delete(self.instru)
        self.openInstruction=True
        self.instructionMsg=\
        ' Now you could press Nest Step to watch the process.'
        self.drawInstruction() 
        self.canvas.delete(self.buttonShowAnswer)
        
#           
    def mulShowAnswer(self):
        if self.pickMulMatrix2==False: #to gurantee
            self.answerMatrix=np.dot(self.viewMulmatrix,self.viewMulmatrix1)
            #print self.viewMulmatrix
            #print self.viewMulmatrix1
            #print self.answerMatrix
            self.drawMulAnswerMatrix()
            self.drawViewStepThroughButton() # animation viewing button
        self.canvas.delete(self.instru)
        self.openInstruction=True
        self.instructionMsg=\
        ' Now you could step through the process by pressing Show Step Button.'
        self.drawInstruction()
        self.canvas.delete(self.buttonShowAnswer)
 
    
    
    
    def drawAddAnswerMatrix(self):
        #sign 
        
        self.sign2=self.canvas.create_text((self.matrixBoundary1[2]+\
                self.matrixBoundary2[0])/2,\
                (self.matrixBoundary[1]+self.matrixBoundary[3])/2,\
                text='=',font=("Helvatica", 12, "bold"))

        
        
        boardX0=self.matrixBoundary2[0]+\
        (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary2[1]+\
        (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix3_1=\
                self.canvas.create_rectangle(cellX0,cellY0,\
                    cellX1,cellY1,fill=self.cellBorderColor)
                
                if row==(self.step-1)/(self.confirmCol+1) and\
                   col==(self.step-1)%(self.confirmCol+1):
                   self.matrix3_2=self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                        fill='BurlyWood')
                else: # self.step!=0
                     self.matrix3_2=self.canvas.create_rectangle(\
                     cellX0+self.cellMargin,cellY0+self.cellMargin,\
                     cellX1-self.cellMargin,cellY1-self.cellMargin,\
                     fill=self.cellBorderColor)  

                self.matrix3_3=self.canvas.create_text(\
                 (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                 text=str(self.answerMatrix[row][col]),\
                 font=("Helvatica", 10, "bold"))
    
    def drawMulAnswerMatrix(self):
        
        self.sign2=self.canvas.create_text((self.matrixBoundary1[2]+\
                self.matrixBoundary2[0])/2,\
                (self.matrixBoundary[1]+self.matrixBoundary[3])/2,\
                text='=',font=("Helvatica", 12, "bold"))

        boardX0=self.matrixBoundary2[0]+\
         (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary2[1]+\
         (self.maxRow/2.0-(self.confirmMul1Row+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmMul1Row*self.cellSize
        for row in xrange(self.confirmMul1Row+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix3_1=self.canvas.create_rectangle(\
                 cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                
                if row==(self.step-1)/(self.confirmCol+1) \
                   and col==(self.step-1)%(self.confirmCol+1):
                    self.matrix3_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                         fill='BurlyWood')
                else: # self.step!=0
                     self.matrix3_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                            fill=self.cellBorderColor)  

                self.matrix3_3=self.canvas.create_text(\
                    (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                    text=str(self.answerMatrix[row][col]),\
                    font=("Helvatica", 10, "bold"))
        
    def gaussElimination(self):
        """
        This function is the engine of gauss elimination, 
        with the functionality of 
        showing each step of the work.
        The function is partially cited from scipy website
        """
        if self.page=='computing mode page':
           A=copy.deepcopy(self.matrixGetFromBoxField)
        elif self.page=='view mode page':
            A=copy.deepcopy(self.viewGEmatrix)
            
        rows=len(A)
        cols=len(A[0])
        self.stepList=[]
        if self.page=='view mode page':
           self.matrixGetFromBoxField=copy.deepcopy(self.viewGEmatrix)
        self.stepList.append(self.matrixGetFromBoxField)
        for col in xrange(0,cols): #variable to eliminate
            for row in xrange(col+1,rows): 
                #rows to eliminate said variable from
               if A[col][col]!=0 and A[col][col]!=1 and (row-1)==col:
                   A[row-1]=A[row-1]/A[col][col]
               else: #pivoting needed
                   #self.singularMatrixError=True
                   pass # partial pivoting or not? 
               for i in xrange(rows):                      
                   for j in xrange(cols):
                       A[i][j]=round(A[i][j],2)
               if (row-1)==col:
                   for i in xrange(rows):                      
                     for j in xrange(cols):
                       A[i][j]=round(A[i][j],2)
                       if abs(A[i][j]-0.0)<0.01:
                           A[i][j]=0.0
                   self.stepList.append(copy.deepcopy(A))
               
               tmp=A[col]*(-A[row][col]/A[col][col]) #multiply row
               A[row]=tmp+A[row]#add
            
               for i in xrange(rows):                      
                   for j in xrange(cols):
                       A[i][j]=round(A[i][j],2)
                       if abs(A[i][j]-0.0)<0.01:
                           A[i][j]=0.0
               self.stepList.append(copy.deepcopy(A)) 
        try:A[rows-1]=A[rows-1]/A[rows-1][rows-1]
        except:pass
        for i in xrange(rows):                      
                   for j in xrange(cols):
                       A[i][j]=round(A[i][j],2)
                       if abs(A[i][j]-0.0)<0.01:
                           A[i][j]=0.0
        self.stepList.append(copy.deepcopy(A))             
               #stepList.append(A)
        #return self.stepList 
    
    def mult_matrix(self, M, N):
        
        """Multiply square matrices of same dimension M and N
        This function is partially cited from scipy website"""
    
        # Converts N into a list of tuples of columns                                                                                                                                                                                                      
        tuple_N = zip(*N)
    
        # Nested list comprehension to calculate matrix multiplication                                                                                                                                                                                     
        return [[sum(el_m * el_n for el_m, el_n in zip(row_m, col_n)) \
                 for col_n in tuple_N] for row_m in M]

    def pivot_matrix(self,M):
        """Returns the pivoting matrix for M, 
        used in Doolittle's method.
        This function is partially cited from scipy website"""
        m = len(M)
    
        # Create an identity matrix, with floating point values                                                                                                                                                                                            
        id_mat = [[float(i ==j) for i in xrange(m)] for j in xrange(m)]
    
        # Rearrange the identity matrix such that the largest element of                                                                                                                                                                                   
        # each column of M is placed on the diagonal of of M                                                                                                                                                                                               
        for j in xrange(m):
            row = max(xrange(j, m), key=lambda i: M[i][j])
            if j != row:
                # Swap the rows                                                                                                                                                                                                                            
                id_mat[j], id_mat[row] = id_mat[row], id_mat[j]
    
        return id_mat

    def luDecomposition(self):
        """Performs an LU Decomposition of A (which must be square)                                                                                                                                                                                        
        into PA = LU. The function returns P, L and U.
        This function is partially cited from scipy website"""
        A=self.matrixGetFromBoxField
        n = len(A)
    
        # Create zero matrices for L and U                                                                                                                                                                                                                 
        L = [[0.0] * n for i in xrange(n)]
        U = [[0.0] * n for i in xrange(n)]
    
        # Create the pivot matrix P and the multipled matrix PA                                                                                                                                                                                            
        P = self.pivot_matrix(A)
        PA = self.mult_matrix(P, A)
        stepU=[]
        stepL=[]
        
        # Perform the LU Decomposition                                                                                                                                                                                                                     
        for j in xrange(n):
            # All diagonal entries of L are set to unity                                                                                                                                                                                                   
            L[j][j] = 1.0
    
            for i in xrange(j+1):
                s1 = sum(U[k][j] * L[i][k] for k in xrange(i))
                U[i][j] = PA[i][j] - s1
                stepU.append(copy.deepcopy(U))
                
    
            for i in xrange(j, n):
                s2 = sum(U[k][j] * L[i][k] for k in xrange(j))
                L[i][j] = (PA[i][j] - s2) / U[j][j]
                stepL.append(copy.deepcopy(L))
            
        for i in xrange(len(stepL)):
            for row in xrange(len(stepL[i])):
                for col in xrange(len(stepL[i][0])):
                    stepL[i][row][col]=round(stepL[i][row][col],2)
                    stepU[i][row][col]=round(stepU[i][row][col],2)
           
        self.stepUlist=stepU
        self.stepLlist=stepL                    
            
    
    #share for all page
    def isOnBoard(self,x,y): # ge
        if self.pickMulMatrix2==False:
            (boardX0, boardY0, boardX1, boardY1) = self.matrixBoundary
        else:
            (boardX0, boardY0, boardX1, boardY1) = self.matrixBoundary1
        return ((x >= boardX0) and (x <= boardX1) and
                (y >= boardY0) and (y <= boardY1))
        
    def getCellFromLocation(self, x, y):  #
        if self.pickMulMatrix2==False:
            (boardX0, boardY0, boardX1, boardY1) = self.matrixBoundary
        else:
            (boardX0, boardY0, boardX1, boardY1) = self.matrixBoundary1
        row = (y - boardY0) / self.cellSize
        col = (x - boardX0) / self.cellSize
        return (row, col)

        
#-------------------------drawStuff------------------------------#
    def drawWelcomePage(self):
        if self.page=='welcome page':
            self.canvas.create_image(0,0, anchor=NW, \
            image = self.welcomeImage)

#             self.canvas.create_text(self.width/2, \
#               self.height/3, text='Visual Matrix Solver', \
#               font=self.welcomeFont)
            
            
            #back here
            
                    
            #drawButton  text=" Click here to learn matrix calculation "
            
            # back here !!!
            self.b1 = Button(self.canvas,image=self.buttonWelcome1Image, \
                          command=self.initPage1,\
                          font = ("helvetica", "16", "normal"))
            self.b1.config(highlightbackground = "white")
            self.b1.pack()
            #self.b1.place(x=self.width/2,y=(self.height*1.7/3))
            #self.b1.forget()
            self.canvas.create_window(self.width/2, self.height*1.7/3,\
                                   window=self.b1)
 
 
            self.b2 = Button(self.canvas, image=self.buttonWelcome2Image, \
                         command=self.initPage2, \
                         font = ("helvetica", "16", "normal"))
            #self.b2.config(highlightbackground = "white")
            self.b2.pack()
            self.canvas.create_window(self.width/2, self.height*2/3, \
                                      window=self.b2) 
    
    
    
    def drawPage1(self): #view mode page
        if self.page=='view mode page':
#             self.canvas.create_text(self.width/2, \
#                 self.titleMargin/2+self.boardMargin, text=self.title1, \
#                 font=self.titleFont)
#           
            self.canvas.create_image(0,0, anchor=NW, \
            image = self.page1Image)

  
            #back button
            self.bP1_1 = Button(self.canvas, image=self.buttonBack, \
                             command=self.initWelcomePage, \
                             font = ("helvetica", "10", "normal"))
            #self.bP1_1.config(highlightbackground = "white")
            self.bP1_1.pack()
            self.canvas.create_window(self.width-30-self.boardMargin, \
                                      20+self.boardMargin, \
                                          window=self.bP1_1) 
            
            # help buton
            self.bP1_2 = Button(self.canvas, image=self.buttonHelp, \
                             command=self.wikiButtonPressed, \
                             font = ("helvetica", "10", "normal"))
            #self.bP1_2.config(highlightbackground = "white")
            self.bP1_2.pack()
            self.canvas.create_window(self.width-80-self.boardMargin, \
                                      20+self.boardMargin, \
                                          window=self.bP1_2) 
            
            
            
            #Addition 
            self.bMA = Button(self.canvas, image=self.buttonAddMatrix, \
                    command=self.callViewMatrixAddition, \
                             font = ("helvetica", "16", "normal"))
            #self.bMA.config(highlightbackground = "white")
            self.bMA.pack()
            self.canvas.create_window(self.width*1.5/8, \
            self.height-1.8*self.boardMargin-self.menuMargin/2, \
                                          window=self.bMA) 
            
            
            #multi
            self.bMul = Button(self.canvas, image=self.buttonMulMatrix, \
                             command=self.callViewMatrixMul, \
                             font = ("helvetica", "16", "normal"))
            #self.bMul.config(highlightbackground = "white")
            self.bMul.pack()
            self.canvas.create_window(self.width*4/8, \
                self.height-1.8*self.boardMargin-self.menuMargin/2, \
                                          window=self.bMul) 
            
            
            
            #GE 
            self.bP2_2 = Button(self.canvas, image=self.buttonGE, \
                             command=self.callViewGE, \
                             font = ("helvetica", "16", "normal"))
            #self.bP2_2.config(highlightbackground = "white")
            self.bP2_2.pack()
            self.canvas.create_window(self.width*6.5/8, \
                self.height-1.8*self.boardMargin-self.menuMargin/2, \
                                          window=self.bP2_2) 
  
  
  
            
            
    
    
    def drawPage2(self): #computing mode page
        if self.page=='computing mode page':
#             self.canvas.create_text(self.width/2, self.titleMargin/2+\
#                                     self.boardMargin,\
#                      text=self.title2, font=self.titleFont)
#             

            self.canvas.create_image(0,0, anchor=NW, \
            image = self.page2Image)

            
            #back button
            self.bP2_1 = Button(self.canvas, image=self.buttonBack, \
                             command=self.initWelcomePage, \
                             font = ("helvetica", "10", "normal"))
            self.bP2_1.config(highlightbackground = "white")
            self.bP2_1.pack()
            self.canvas.create_window(self.width-30-self.boardMargin, \
                                      20+self.boardMargin, \
                                          window=self.bP2_1) 
            
            # help buton
            self.bP1_2 = Button(self.canvas, image=self.buttonHelp, \
                             command=self.wikiButtonPressed, \
                             font = ("helvetica", "10", "normal"))
            self.bP1_2.config(highlightbackground = "white")
            self.bP1_2.pack()
            self.canvas.create_window(self.width-80-self.boardMargin, \
                                      20+self.boardMargin, \
                                          window=self.bP1_2) 

                    
    
            #GE 
            self.bP2_2 = Button(self.canvas, image=self.buttonGE, \
                             command=self.callGE, \
                             font = ("helvetica", "16", "normal"))
            self.bP2_2.config(highlightbackground = "white")
            self.bP2_2.pack()
            self.canvas.create_window(self.width*3/10, \
               self.height-self.boardMargin-self.menuMargin*2/3, \
                                          window=self.bP2_2) 
           
            
            #LU
            self.bP2_3 = Button(self.canvas, image=self.buttonImageLU, \
                             command=self.callLU, \
                             font = ("helvetica", "16", "normal"))
            self.bP2_3.config(highlightbackground = "white")
            self.bP2_3.pack()
            self.canvas.create_window(self.width*7/10, \
                self.height-self.boardMargin-self.menuMargin*2/3, \
                                          window=self.bP2_3)
    

    
    
    def drawAnimationPage(self):
        if self.page=='animation page':
            
#             self.canvas.create_text(self.width/2, \
#                 self.titleMargin/2, text=self.title3, font=self.titleFont)
#             # here I init timerfired
            self.canvas.create_image(0,0, anchor=NW, \
            image = self.page3Image)
            self.timerFired()
            

            
    def redrawAnimation(self): #back here
        # delete Matrix part is oK
        self.canvas.delete(ALL)
        self.canvas.create_image(0,0, anchor=NW, \
            image = self.page3Image)
        #self.canvas.create_text(self.width/2, \
        #    self.titleMargin/2, text=self.title3, font=self.titleFont)
        
        
        self.openInstruction=True
        self.instructionMsg=\
        """        Press Right arrow to show the elimination\n
        Did you see that the number in LightSalmon changes?\n
        Press Left arrow to show the previous step\n
        Press B to come back the previous page"""
        self.drawHelpInstruction()
        # back here
        
        self.drawMatrixAnimationStep()
        
    
    
    def pickDivideStep(self):
        k=self.confirmRow+1
        l=[]
        m=k
        prev=1
        for i in xrange(k-1):
           prev=prev+m
           m-=1
           l.append(prev)
        self.pickDivideStepPool=l
    
    
    def drawMatrixAnimationStep(self):
        #print 'step=',self.step
        self.pickDivideStep()
        if self.step<=self.pickDivideStepPool[-1]+1:   
#                 self.timerCounter=0                  
            if self.step==self.pickDivideStepPool[-1]+1:
                #self.drawLineofStartandEnd()
                self.step=0
                self.drawMatrixIntheMiddle0()
                self.timerCounter=0
            if self.step==0:
                self.drawMatrixIntheMiddle0()
                self.drawLineofStartandEnd()
                self.timerCounter=0
            
            elif self.step==1:
                self.divideRow=1 #row number to divide first elem
                self.startingElimRow=self.divideRow 
                # from row 2 to eliminate
                self.drawLineofNumbersStep1()  
                # step 1 is row/number
                self.matrixNow=self.stepList[0]
                self.drawMatrixIntheMiddle1() 
                #fading effect
                if self.timerCounter==75:
                    self.matrixNow=self.stepList[1]
                    self.drawMatrixIntheMiddle1()
            
            
            
            elif (self.step in self.pickDivideStepPool): #step=4
                self.divideRow=self.pickDivideStepPool.index(self.step)+2
                self.startingElimRow=self.divideRow # now =3
                self.drawLineofNumbersStep1()      # step 4 is row/4
                self.matrixNow=self.stepList[self.step-1]
                self.drawMatrixIntheMiddle1() #fading effect
                if self.timerCounter==75:
                    self.matrixNow=self.stepList[self.step]
                    self.drawMatrixIntheMiddle1()
           
            else:        #2<=self.step<=self.confirmRow+1:     step 2 3 5 
                #self.drawLineofNumbersStep2()   
                #step2 is row2-row1*number
                lastDivideStep=1
                for i in self.pickDivideStepPool:
                    if i < self.step:
                        lastDivideStep=i 
                #print 'lastDividestep=',lastDivideStep              
                if lastDivideStep!=1:
                     self.startingElimRow=self.step-lastDivideStep+\
                      self.pickDivideStepPool.index(lastDivideStep)+2 
                else:
                    self.startingElimRow=self.step
                # print self.startingElimRow
                self.drawLineofNumbersStep2() 
                self.matrixNow=self.stepList[self.step-1]
                self.drawMatrixIntheMiddle1()
                if self.timerCounter==75:
                    try:
                        self.matrixNow=self.stepList[self.step]
                        self.drawMatrixIntheMiddle1()
                    except:pass
 
 
    def drawLineofStartandEnd(self): # back here
        boardX0=self.matrixBoundary[0]+\
        (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+\
        (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
        if self.step==0:
           textmsg='Get Started'
        elif self.step==self.pickDivideStepPool[-1]+1:
           textmsg='done'
        self.canvas.create_text(boardX0+self.cellSize*2,boardY0+\
                    0.5*self.cellSize,\
                   text=textmsg\
                ,font=("Helvatica", 10, "bold"))
                
    
    def drawLineofNumbersStep1(self):
        boardX0=self.matrixBoundary[0]+\
        (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+\
        (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize

        try:self.canvas.create_text(boardX0+self.cellSize*2,boardY0+\
                    0.5*self.cellSize,\
                   text='row%d'%self.divideRow +'   /   '\
         +str(self.stepList[self.step-1][self.divideRow-1][self.divideRow-1])\
                ,font=("Helvatica", 12, "bold"))
        except:pass
    def drawLineofNumbersStep2(self):
        boardX0=self.matrixBoundary[0]+\
        (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+\
        (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
        #print 'startingElimRow-1',self.startingElimRow-1
        #print 'divideRow-1',self.divideRow-1
        #print len(self.stepList)
        try:self.canvas.create_text(boardX0+self.cellSize*2,boardY0+\
                    0.5*self.cellSize,\
           text='row%d - row%d x '%(self.startingElimRow,self.divideRow)\
        +''+str(self.stepList[self.step-1]\
                [self.startingElimRow-1][self.divideRow-1])\
        ,font=("Helvatica", 12, "bold"))
        except:pass
            
           
    def drawMatrixIntheMiddle0(self):
        # draw Matrix when step=0
        if self.playingWithGE==True:
            boardX0=self.matrixBoundary[0]+\
            (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+\
            (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize+50
            boardX1=boardX0+(self.confirmCol+1)*self.cellSize
            boardY1=boardY0+(self.confirmRow+1)*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_text((cellX0+cellX1)/2,\
                 (cellY0+cellY1)/2,text=str(self.stepList[0][row][col])\
            , font=("Helvatica", 10, "bold"))    # draw numbers
        self.canvas.create_line(boardX0-self.cellSize,\
                        boardY0,boardX0-self.cellSize,boardY1)
        self.canvas.create_line(boardX1+self.cellSize,\
                    boardY0,boardX1+self.cellSize,boardY1)
       
    def drawMatrixIntheMiddle1(self):
        if self.playingWithGE==True:
            boardX0=self.matrixBoundary[0]+(\
             self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(\
             self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize+50
            boardX1=boardX0+(self.confirmCol+1)*self.cellSize
            boardY1=boardY0+(self.confirmRow+1)*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                if row==self.startingElimRow-1:
                    self.canvas.create_rectangle(\
                        cellX0,cellY0,cellX1,cellY1,\
                        fill='BurlyWood',outline='')
                    if col==self.divideRow-1:
                       self.canvas.create_rectangle(\
                        cellX0,cellY0,cellX1,cellY1,\
                        fill='LightSalmon',outline='')
                else:
                    pass
#                     self.canvas.create_rectangle(\
#                         cellX0,cellY0,cellX1,cellY1,\
#                         fill=self.cellBorderColor,outline='')
                self.canvas.create_text(\
                      (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                    text=str(self.matrixNow[row][col])\
                    , font=("Helvatica", 10, "bold"))    # draw numbers
        self.canvas.create_line(boardX0-self.cellSize,\
                        boardY0,boardX0-self.cellSize,boardY1)
        self.canvas.create_line(boardX1+self.cellSize,\
                    boardY0,boardX1+self.cellSize,boardY1)
        
    
    
    
    
    
    
    
    def drawInstruction(self):
        if self.openInstruction==True:
           self.instru=self.canvas.create_text(\
          self.width*0.9/3,self.titleMargin+\
          2*self.boardMargin+self.maxRow*self.cellSize+\
          1.4*self.instruMargin,\
          text=self.instructionMsg,font=("Helvatica", 16, "bold"),\
          anchor=SW)
           self.openInstruction=False
                                
    def drawHelpInstruction(self):
        if self.openInstruction==True:
           self.instru=self.canvas.create_text(\
            self.width/2,self.height-2*self.boardMargin-self.menuMargin/2,\
            text=self.instructionMsg,font=("Helvatica", 16, "bold"))
           self.openInstruction=False                           
    
    def wikiButtonPressed(self):
        try:
#             element = self.board[self.startRow][self.startCol]
#             index = self.elementsList.index(element)
#             name = self.nameList[index]
            if self.page=='view mode page':
               webbrowser.open('http://en.wikipedia.org/wiki/Gauss_elimination')
            else:
               webbrowser.open('http://en.wikipedia.org/wiki/Lu_decomposition') 
        except: pass
    
    
    def deltaDraw(self):
        #after pressing the mouse, I get self.confirmRow,and self.confirmCol
        # I need to delete original matrix and draw a new one
        self.redrawALL()
        #self.drawConfirmedMatrix()
        #self.openTextField=True
        self.drawTextFieldandOKButton()
        
    def deltaViewDraw(self):
        self.redrawALL()
        
        self.viewGEmatrix=np.random.randint(-999,999,size=(\
                    self.confirmRow+1,self.confirmCol+1))/100.0
        self.drawViewGEInitialMatrix()
        self.drawAnswerButton()
        self.drawViewStepThroughButton() # animation viewing button
    
    
    
 
    
    def deltaViewDrawAddition(self):
        self.redrawALL()
        
        self.viewAdmatrix=np.random.randint(-9,9,size=(\
                    self.confirmRow+1,self.confirmCol+1))
        self.viewAdmatrix1=np.random.randint(-9,9,size=(\
                   self.confirmRow+1,self.confirmCol+1))
        
        self.drawViewAdInitialMatrix()
        self.drawAnswerButton()
        #self.drawViewStepThroughButton() # animation viewing button
        
        self.openInstruction=True
        self.instructionMsg=\
        '  The second matrix of the same size is created for you,\n'+\
        'now you can press Show Ans button to find out the answer.' 
        self.drawInstruction()
    
    def deltaViewDrawMulti(self):
        self.redrawALL()
        
        if self.pickMulMatrix1==True:
            self.viewMulmatrix=np.random.randint(-9,9,size=(\
                self.confirmMul1Row+1,self.confirmMul1Col+1))
    
            self.drawViewMulInitialMatrix() # back here
        elif self.pickMulMatrix2==True:
            self.drawViewMulInitialMatrix()
            self.viewMulmatrix1=np.random.randint(-9,9,size=(\
                self.confirmMul1Col+1,self.confirmCol+1))
            self.drawViewMulInitalMatrix2()
            #self.drawViewStepThroughButton() 
            self.drawAnswerButton()
            #self.drawViewStepThroughButton() # animation viewing button
        
        self.openInstruction=True
        if self.pickMulMatrix1==True:
            self.instructionMsg=\
('Matrix 1 has %d columns so the second matrix must have %d row.'+\
'\n     Please choose the number of columns for matrix 2' )%\
           ((self.confirmMul1Col+1),\
                            (self.confirmMul1Col+1)) 
        else:
            self.instructionMsg=\
            'Now you can press Show Ans button to find out the answer.'
        self.drawInstruction()
        
    
    
    def drawViewMulInitialMatrix(self):
        # x sign
        self.sign1=self.canvas.create_text((self.matrixBoundary[2]+\
                self.matrixBoundary1[0])/2,\
                (self.matrixBoundary[1]+self.matrixBoundary[3])/2,\
                text='x',font=("Helvatica", 12, "bold"))
        
        
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                    (self.confirmMul1Col+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                    (self.confirmMul1Row+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmMul1Col*self.cellSize
        boardY1=boardY0+self.confirmMul1Row*self.cellSize    
        for row in xrange(self.confirmMul1Row+1):
            for col in xrange(self.confirmMul1Col+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix1_1=self.canvas.create_rectangle(\
                      cellX0,cellY0,cellX1,cellY1,\
                      fill=self.cellBorderColor)
                if row==(self.step-1)/(self.confirmCol+1):
                     self.matrix1_2=self.canvas.create_rectangle(\
                      cellX0+self.cellMargin,cellY0+self.cellMargin,\
                      cellX1-self.cellMargin,cellY1-self.cellMargin,\
                      fill='BurlyWood') 
                else: # self.step!=0
                     self.matrix1_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                        fill=self.cellBorderColor) 
                self.matrix1_3=self.canvas.create_text(\
                        (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                       text=str(self.viewMulmatrix[row][col])\
                      , font=("Helvatica", 10, "bold"))
    
    
    def drawViewMulInitalMatrix2(self):
        
        
        boardX0=self.matrixBoundary1[0]+(self.maxCol/2.0-(\
                    self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary1[1]+(self.maxRow/2.0-(\
                   self.confirmMul1Row+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize    
        for row in xrange(self.confirmMul1Col+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix2_1=self.canvas.create_rectangle(\
                 cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                if (col==(self.step-1)%(self.confirmCol+1) \
                   and self.step!=0 and self.step!=\
                    (self.confirmMul1Row+1)*(self.confirmCol+1)+1):
                     self.matrix2_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                        fill='BurlyWood') 
                else: # self.step!=0
                     self.matrix2_2=self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                    fill=self.cellBorderColor) 
                self.matrix2_3=self.canvas.create_text(\
                 (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                 text=str(self.viewMulmatrix1[row][col])\
                 ,font=("Helvatica", 10, "bold"))
        
    def drawViewAdInitialMatrix(self):
        if self.playingWithMatrixAd==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
             self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
             self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize    
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix1_1=self.canvas.create_rectangle(\
                  cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                if row==(self.step-1)/(self.confirmCol+1) and \
                 col==(self.step-1)%(self.confirmCol+1):
                     self.matrix1_2=self.canvas.create_rectangle(\
                      cellX0+self.cellMargin,cellY0+self.cellMargin,\
                      cellX1-self.cellMargin,cellY1-self.cellMargin,\
                                             fill='BurlyWood') 
                else: # self.step!=0
                     self.matrix1_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                         fill=self.cellBorderColor) 
                self.matrix1_3=self.canvas.create_text(\
                     (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                     text=str(self.viewAdmatrix[row][col])\
                     , font=("Helvatica", 10, "bold"))
        
        self.sign1=self.canvas.create_text((self.matrixBoundary[2]+\
                self.matrixBoundary1[0])/2,\
                (self.matrixBoundary[1]+self.matrixBoundary[3])/2,\
                text='+',font=("Helvatica", 12, "bold"))
        
                
        
                
        boardX0=self.matrixBoundary1[0]+(self.maxCol/2.0-(\
                    self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary1[1]+(self.maxRow/2.0-(\
                   self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize  
        
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.matrix2_1=self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                if row==(self.step-1)/(self.confirmCol+1) and \
                   col==(self.step-1)%(self.confirmCol+1):
                    self.matrix2_2=self.canvas.create_rectangle(\
                        cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                                             fill='BurlyWood')
                else: # self.step!=0
                     self.matrix2_2=self.canvas.create_rectangle(\
                      cellX0+self.cellMargin,cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                             fill=self.cellBorderColor)  
                    
                self.matrix2_3=self.canvas.create_text(\
                    (cellX0+cellX1)/2,(cellY0+cellY1)/2,\
                    text=str(self.viewAdmatrix1[row][col])\
                    ,font=("Helvatica", 10, "bold"))
           
    
    
    
    def drawViewStepThroughButton(self):
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
            self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
            self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        if self.playingWithGE==True: # to init function 
           self.bStepBack = Button(self.canvas, \
                         image=self.buttonImageNextStep,\
                          command=self.viewStepAnimation, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithLU==True: # change
            self.bStepBack = Button(self.canvas,\
                          image=self.buttonImageNextStep,\
                          command=self.viewStepAnimation, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithMatrixAd==True:  
            self.bStepBack = Button(self.canvas, text=" Show Step ",
                          image=self.buttonImageNextStep, \
                           command=self.viewAddStep,\
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithMatrixMul==True:  
            self.bStepBack = Button(self.canvas, 
                           image=self.buttonImageNextStep,\
                           command=self.viewMulStep,\
                          font = ("helvetica", "16", "normal"))    
        #self.bStepBack.config(highlightbackground = "white")
        self.bStepBack.pack()
        
        self.buttonShowStep=self.canvas.create_window(self.width*5.5/8, \
                    self.height-0*self.boardMargin-self.menuMargin*2/4,\
                   window=self.bStepBack)

    
    
    
    
    def viewStepAnimation(self):
        self.gaussElimination()
        self.maxStep=len(self.stepList)
        self.initAnimationPage()
        
        
    def viewAddStep(self):
        #if self.step=0:
        try:
            if self.step<(self.confirmRow+1)*(self.confirmCol+1)+1:
                self.step+=1
            self.viewAddEachStep()
        except:
            self.canvas.delete(self.instru)
            self.openInstruction=True
            self.instructionMsg=\
           '                 Try another? Click any button below.'
            self.drawInstruction() 
            self.canvas.delete(self.buttonShowStep)
            self.canvas.delete(self.buttonShowAnswer)
            
            pass
            
    def viewMulStep(self):
#         if self.step<(self.confirmMul1Row+1)*(self.confirmCol+1):
#             self.step+=1
#         self.viewMulEachStep() # back here
#         
        
        try:
            if self.step<(self.confirmMul1Row+1)*(self.confirmCol+1)+1:
                self.step+=1
            self.viewMulEachStep()
        except:
            self.canvas.delete(self.instru)
            self.openInstruction=True
            self.instructionMsg=\
           '                 Try another? Click any button below.'
            self.drawInstruction() 
            self.canvas.delete(self.buttonShowStep)
            self.canvas.delete(self.buttonShowAnswer)
            
            pass
        
    
    def viewMulEachStep(self):
        self.canvas.delete(self.matrix1_1,self.matrix1_2,self.matrix1_3,\
                           self.matrix2_1,self.matrix2_2,self.matrix2_3,\
                           self.matrix3_1,self.matrix3_2,self.matrix3_3,\
                           self.instru,self.sign1,self.sign2)
        self.drawViewMulInitialMatrix()
        self.drawViewMulInitalMatrix2()
        self.drawMulAnswerMatrix()
        self.drawMulStepInstructoin() 
        #self.drawAnswerButton()
        #self.drawViewStepThroughButton() # animation viewing button
            
    def viewAddEachStep(self):    
        self.canvas.delete(self.matrix1_1,self.matrix1_2,self.matrix1_3,\
                           self.matrix2_1,self.matrix2_2,self.matrix2_3,\
                           self.matrix3_1,self.matrix3_2,self.matrix3_3,\
                           self.instru,self.sign1,self.sign2)
        self.drawViewAdInitialMatrix()
        self.drawAddAnswerMatrix()
        self.drawAddStepInstructoin() 
        #self.drawAnswerButton()
        #self.drawViewStepThroughButton() # animation viewing button
        
    def drawAddStepInstructoin(self): 
        self.openInstruction=True
        row=(self.step-1)/(self.confirmCol+1) 
        col=(self.step-1)%(self.confirmCol+1)
        
        self.instructionMsg='                          %d + %d = %d' % \
                   (self.viewAdmatrix[row][col],\
            self.viewAdmatrix1[row][col],self.answerMatrix[row][col]) 
        self.drawInstruction()
        
        
    def drawMulStepInstructoin(self):
        self.openInstruction=True
        row=(self.step-1)/(self.confirmCol+1) # start from row 0 
        col=(self.step-1)%(self.confirmCol+1)
        
        lZip=zip(self.viewMulmatrix[row,:],self.viewMulmatrix1[:,col])
        
        lastTul=lZip[-1]
        
        tul=()
        for i in xrange(len(lZip)-1):
            tul+=lZip[i]
        
        
        self.instructionMsg=self.confirmMul1Col*' (%d x %d) + ' % \
                   (tul) + '(%d x %d)' %(lastTul) + ' = '+'%d'\
                   %self.answerMatrix[row][col] 
        self.drawInstruction()
        #back here
        
    
    def drawTextFieldandOKButton(self):
        if self.openTextField==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                    (self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                    (self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize
            self.entry={} #diction
            self.geEnt={}
            #print self.confirmRow
            for row in xrange(self.confirmRow+1):
                for col in xrange(self.confirmCol+1):
                    cellX0 = boardX0 + col*self.cellSize
                    cellX1 = cellX0 + self.cellSize
                    cellY0 = boardY0 + row*self.cellSize
                    cellY1 = cellY0 + self.cellSize 
                    
                    self.geEnt[row,col]=DoubleVar()
                    self.entry[row,col] = Entry(self.canvas, \
                      textvariable=self.geEnt[row,col],\
                      width=self.blankWidth)
                    self.entry[row,col].pack()
                    self.canvas.create_window((cellX0+cellX1)/2,\
                     (cellY0+cellY1)/2,window=self.entry[row,col])
            self.bOK = Button(self.canvas, image=self.buttonImageYesMark, \
                          command=self.getMatrixFromBoxField, \
                          font = ("helvetica", "16", "normal"))
            #self.bOK.config(highlightbackground = "white")
            self.bOK.pack()
            if self.playingWithGE==True:
                self.canvas.create_window(boardX1+self.cellSize*3,\
                                boardY1,
                                window=self.bOK)
            elif self.playingWithLU==True:
                self.canvas.create_window(boardX1+self.cellSize*3,\
                                boardY1,
                                window=self.bOK)  
            elif self.playingWithMatrixAd==True:
                self.canvas.create_window(boardX1+self.cellSize*3,\
                                boardY1,
                                window=self.bOK)    
    def drawStepThroughButton(self):
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                            (self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                            (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        if self.playingWithGE==True:
           self.bStepThrough = Button(self.canvas, \
                            image=self.buttonImageNextStep, \
                          command=self.geStepThrough, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithLU==True:
            self.bStepThrough = Button(self.canvas,\
                          image=self.buttonImageNextStep, \
                          command=self.luStepThrough, \
                          font = ("helvetica", "16", "normal"))
        #self.bStepThrough.config(highlightbackground = "white")
        self.bStepThrough.pack()
        self.buttonNextStep=self.canvas.create_window(self.width*6.6/8, \
                    self.height-self.menuMargin*2/4,\
                    window=self.bStepThrough)
        
    def drawStepBackButton(self):
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                    (self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                    (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        if self.playingWithGE==True:
           self.bStepBack = Button(self.canvas, \
                          image=self.buttonImagePrevStep, \
                          command=self.geStepBack, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithLU==True:
            self.bStepBack = Button(self.canvas, \
                          image=self.buttonImagePrevStep, \
                          command=self.luStepBack, \
                          font = ("helvetica", "16", "normal"))
        #self.bStepBack.config(highlightbackground = "white")
        self.bStepBack.pack()
        self.buttonBackStep=self.canvas.create_window(self.width*4.8/8, \
                    self.height-self.menuMargin*2/4,\
                    window=self.bStepBack)
        
            
    
    def drawAnswerButton(self):
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                (self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        if self.playingWithGE==True:
            self.bShowAnswer = Button(self.canvas,image=self.buttonImageShowAns,\
                          command=self.geShowAnswer, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithLU==True:
            self.bShowAnswer = Button(self.canvas,image=self.buttonImageShowAns,\
                          command=self.luShowAnswer, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithMatrixAd==True:
            self.bShowAnswer = Button(self.canvas,image=self.buttonImageShowAns,\
                          command=self.addShowAnswer, \
                          font = ("helvetica", "16", "normal"))
        elif self.playingWithMatrixMul==True:
            self.bShowAnswer = Button(self.canvas,image=self.buttonImageShowAns,\
                          command=self.mulShowAnswer, \
                          font = ("helvetica", "16", "normal"))
        #self.bShowAnswer.config(highlightbackground = "white")
        self.bShowAnswer.pack()
        self.buttonShowAnswer=self.canvas.create_window(self.width*2.5/8, \
                    self.height-self.menuMargin*2/4,\
                   window=self.bShowAnswer)
            
                                          
    def drawViewGEInitialMatrix(self): #view mode
        if self.playingWithGE==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                (self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                (self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize
        if self.playingWithLU==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
             (self.confirmCol+1)/2.0)*self.cellSize+\
              self.cellSize*(self.maxCol+1)
            boardY0=self.matrixBoundary[1]+\
              (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize    
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(cellX0,cellY0,\
                        cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(cellX0+self.cellMargin,\
                        cellY0+self.cellMargin,\
                        cellX1-self.cellMargin,cellY1-self.cellMargin,\
                                             fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                        (cellY0+cellY1)/2,text=str(\
                        self.viewGEmatrix[row][col])\
                            , font=("Helvatica", 10, "bold"))

    def drawConfirmedMatrix(self): # computer mode
        if self.playingWithGE==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
                    self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
                    self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize
        elif self.playingWithLU==True:
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
                   self.confirmCol+1)/2.0)*self.cellSize+\
                   self.cellSize*(self.maxCol+1)
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
                   self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize  
        elif self.playingWithMatrixAd==True:
            #back here
            boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
             self.confirmCol+1)/2.0)*self.cellSize
            boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
             self.confirmRow+1)/2.0)*self.cellSize
            boardX1=boardX0+self.confirmCol*self.cellSize
            boardY1=boardY0+self.confirmRow*self.cellSize     
                  
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(cellX0,cellY0,\
                    cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(cellX0+self.cellMargin,\
                                            cellY0+self.cellMargin,\
                                             cellX1-self.cellMargin,\
                                             cellY1-self.cellMargin,\
                                             fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                    (cellY0+cellY1)/2,text=str(\
                    self.matrixGetFromBoxField[row][col])\
                    , font=("Helvatica", 10, "bold"))
    
    def drawAnswerMatrix(self): # GE
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-(\
                self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-(\
                 self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(cellX0,cellY0,\
                    cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(cellX0+self.cellMargin,\
                                            cellY0+self.cellMargin,\
                                            cellX1-self.cellMargin,\
                                            cellY1-self.cellMargin,\
                                            fill=self.cellBorderColor) 
                self.matrix=self.canvas.create_text((cellX0+cellX1)/2,\
                             (cellY0+cellY1)/2,\
                              text=str(self.answerMatrix[row][col])\
                            , font=("Helvatica", 10, "bold"))
      
            
    def drawStepMatrix(self): #GE
        boardX0=self.matrixBoundary[0]+(\
                self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(\
                self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                     fill=self.cellBorderColor) 
                self.matrix=self.canvas.create_text((cellX0+cellX1)/2,\
                    (cellY0+cellY1)/2,text=str(self.stepMatrix[row][col])\
                    , font=("Helvatica", 10, "bold"))
                #back here
    
    
    def drawLUAnswerMatrix(self):
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
             (self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
              (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                    fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                    (cellY0+cellY1)/2,text=\
                    str(self.stepUlist[-1][row][col])\
                    ,font=("Helvatica", 10, "bold"))
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                (self.confirmCol+1)/2.0)*self.cellSize-6*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                    fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                   (cellY0+cellY1)/2,text=\
                   str(self.stepLlist[-1][row][col])\
                  , font=("Helvatica", 10, "bold"))
    
    
    
    
    def drawLUStepMatrix(self): # change
        boardX0=self.matrixBoundary[0]+\
         (self.maxCol/2.0-(self.confirmCol+1)/2.0)*self.cellSize
        boardY0=self.matrixBoundary[1]+\
         (self.maxRow/2.0-(self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                    fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                    (cellY0+cellY1)/2,text=\
                    str(self.stepUMatrix[row][col])\
                    ,font=("Helvatica", 10, "bold"))
        boardX0=self.matrixBoundary[0]+(self.maxCol/2.0-\
                (self.confirmCol+1)/2.0)*self.cellSize-6*self.cellSize
        boardY0=self.matrixBoundary[1]+(self.maxRow/2.0-\
                (self.confirmRow+1)/2.0)*self.cellSize
        boardX1=boardX0+self.confirmCol*self.cellSize
        boardY1=boardY0+self.confirmRow*self.cellSize
        for row in xrange(self.confirmRow+1):
            for col in xrange(self.confirmCol+1):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize 
                self.canvas.create_rectangle(cellX0,cellY0,\
                    cellX1,cellY1,fill=self.cellBorderColor)
                self.canvas.create_rectangle(cellX0+self.cellMargin,\
                    cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                     fill=self.cellBorderColor) 
                self.canvas.create_text((cellX0+cellX1)/2,\
                    (cellY0+cellY1)/2,text=\
                    str(self.stepLMatrix[row][col])\
                    , font=("Helvatica", 10, "bold"))

                
    
    
        
    
    def drawPickSizeMatrix(self,boardX0,boardY0,boardX1,boardY1):  
          #useful for every case    
        
        for row in xrange(self.maxRow):
            for col in xrange(self.maxCol):
                cellX0 = boardX0 + col*self.cellSize
                cellX1 = cellX0 + self.cellSize
                cellY0 = boardY0 + row*self.cellSize
                cellY1 = cellY0 + self.cellSize
#                 if self.openMouseMotion==True:
#                    color = self.pickingColor
#                 else:
#                    color = self.cellBorderColor
                try:
                   if self.openMouseMotion==True and \
                     (row<=self.shadowRow and col<=self.shadowCol):
                      color=self.cellPickingColor
                   else:
                      color=self.cellBorderColor
                except:pass
                try:
                    self.canvas.create_rectangle(\
                    cellX0,cellY0,cellX1,cellY1,fill=color)
                    self.canvas.create_rectangle(\
                    cellX0+self.cellMargin,cellY0+self.cellMargin,\
                    cellX1-self.cellMargin,cellY1-self.cellMargin,\
                    fill=color)
                except:pass
    
    def drawPickingBlock(self,boardX0,boardY0,boardX1,boardY1):
        row=self.confirmMul1Col+1
        for col in xrange(self.maxCol):
            cellX0 = boardX0 + col*self.cellSize
            cellX1 = cellX0 + self.cellSize
            cellY0 = boardY0 #
            cellY1 = cellY0 + row*self.cellSize
#                 if self.openMouseMotion==True:
#                    color = self.pickingColor
#                 else:
#                    color = self.cellBorderColor
            if self.openMouseMotion==True and (col<=self.shadowCol):
                 color=self.cellPickingColor
            else:
                  color=self.cellBorderColor
            self.canvas.create_rectangle(cellX0,cellY0,cellX1,\
                                        cellY1,fill=color)
            self.canvas.create_rectangle(cellX0+self.cellMargin,\
                                         cellY0+self.cellMargin,\
                                         cellX1-self.cellMargin,\
                                         cellY1-self.cellMargin,\
                                         fill=color)

    
    def redrawALL(self):
        self.canvas.delete(ALL)
        self.drawWelcomePage()
        self.drawPage1()
        self.drawPage2()
        self.drawAnimationPage() 
        
    def __init__(self):
        rows=5 
        cols=19
        cellSize=40
        self.openTextField=False
        self.openMouseMotion=False
        self.pickMulMatrix2=False
        self.rows = rows
        self.cols = cols
        self.cellSize = cellSize
        self.welcomeFont="Arial 50 bold"
        self.titleFont = "Arial 14 bold"
        self.titleMargin=60
        self.menuMargin = 200
        self.instruMargin=100
        self.titleFill = "LightSalmon"
        self.boardMargin = 27
        self.cellMargin = 5
        self.cellBorderColor = 'white'
        self.cellPickingColor='BurlyWood'
        self.cellBackgroundColor = "white"
        self.blankWidth=3
        self.maxRow=5 
        self.maxCol=5
        self.openInstruction=False
        self.width = self.cols*self.cellSize + 4*self.boardMargin
        self.height = self.titleMargin+(self.rows*self.cellSize)\
             +self.instruMargin\
            + self.menuMargin + 4*self.boardMargin
        
        #print self.width
        #print self.height
        root = Tk()
        root.bind("<Button-1>", self.mousePressed)
        root.bind("<Motion>", self.mouseMotion)
        root.bind("<Key>", self.keyPressed)
#         root.bind("<Configure>", self.sizeChanged)
        
#         self.width = self.canvas.winfo_reqwidth()
#         self.height =self.canvas.winfo_reqheight()
        self.canvas=Canvas(root, width=self.width, height=self.height)
        self.canvas.pack()
        self.initWelcomePage()
        root.mainloop()
                
VMS_top_down()



    