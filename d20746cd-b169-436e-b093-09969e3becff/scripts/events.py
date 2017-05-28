def onPhase(args):
    lastPhase = args.name
    if lastPhase == None:
        Draw()
        
       

def Draw():
    mute()
    me.Library[0].moveTo(me.hand)
    notify("{} draws a card.".format(me))
    
          


