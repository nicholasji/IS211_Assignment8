#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment 8"""

import argparse, random, sys, time

class player:
    def __init__(self, name, total=0):
        self.name = name
        self.total = total

    def ntotal(self, newsocre):
        self.total = self.total + newsocre

    def rollorhold(self, gametotal=0):
        roll = raw_input("Roll or Hold? r = roll, h = hold")
        return roll

class cplayer(player):
    def rollorhold(self, gametotal):
        limit = 100 - self.total
        limit = 25 if limit > 25 else limit

        if ( gametotal < limit ):
            roll = 'r'
            rolling = 'rolling'
        else:
            roll = 'h'
            rolling = 'holding'

        return roll

class playerfacotry:
    def getplayer(self, ptype, name):
        if ptype == 'h':
            return player(name)
        if ptype == 'c':
            return cplayer(name)

class die:
    def __init__(self, roll=0):
        self.roll =  roll

    def newroll(self, seed): 
        random.seed(seed)
        self.roll = random.randrange(1, 7)
        return self.roll

class gamecenter:
    def __int__(self, players, total=0):
        self.player1 = players[1]
        self.player2 = players[2]
        self.ttotal = total

    def tscore(self, newsocre):
        self.ttotal = self.ttotal + newsocre
        return self.ttotal

    def tscoreck(self, player, wpoints):
        score = player.total + self.ttotal
        if score >= wpoints:
            player.total = score
            print "%s You win." % (player.name)
            print 'Final score', player.total
            self.govr()

    def tswitch(self, crplayer):
        self.ttotal = 0
        print 'Switch players.'
        return 2 if crplayer == 1 else 1

    def stmsg(self, player, new_roll):
        print "%s rolled %s. This turn's score %s and the total score is %s" % \
        (player.name, new_roll, self.ttotal, player.total )

    def wmsg(self, player):
        print "%s, your current score is %s." % \
        (player.name,player.total)

    def govr(self):
        print "Game Over. Restart to play again."    
        sys.exit()

class Proxy:
    def __init__(self, timestamp = 0):
        self.timestamp = timestamp
        self.dice = None
        self.dice = die()

    def timecheck(self, timestamp):
        if (self.timestamp == 0 or self.timestamp > time.time() ):
            seed = time.time()
            return self.dice.newroll(seed)
        else:
            print("Game Over")
            print "Time's up"
            sys.exit() 


def main():
    parser = argparse.ArgumentParser()
    player1 = parser.add_argument("--player1", help='enter player type: "c" - computer, "h" -human eg: --player1 c', type=str)
    player2 = parser.add_argument("--player2", help='enter player type: "c" - computer, "h" -human eg: --player1 c', type=str)
    timed = parser.add_argument("--timed", help='timed game enter y', type=str)
    args = parser.parse_args()

    factory = playerfacotry()
    game = gamecenter()

    players = { 1: factory.getplayer(args.player1,'player1'),
                2: factory.getplayer(args.player2,'player2')}

    if args.timed=='y':
        timestamp = time.time() + 60
    else:
        timestamp = 0

    p = Proxy(timestamp)

    crplayer = 1
    game.ttotal = 0
    game.wmsg(players[crplayer])

    while (players[crplayer].total < 100) :
        new_roll = p.timecheck(timestamp)

        roll = players[crplayer].rollorhold(game.ttotal)

        if roll == 'r':

            print "DIE ROLL: ", new_roll
            if new_roll == 1:
                game.ttotal = 0
                game.stmsg(players[crplayer],new_roll)
                crplayer = game.tswitch(crplayer)
                game.wmsg(players[crplayer])
                p.timecheck(timestamp)
            else:
                game.ttotal = game.tscore(new_roll)
                game.stmsg(players[crplayer],new_roll)
                game.tscoreck(players[crplayer], 100)
                p.timecheck(timestamp)

        elif roll == 'h':
            p.timecheck(timestamp)
            print players[crplayer].name, " adds ", game.ttotal, " points to the previous total of ", players[crplayer].total
            players[crplayer].ntotal(game.ttotal)
            crplayer = game.tswitch(crplayer)
            game.wmsg(players[crplayer])

        else:
            print "enter r - to roll or h - to hold"

        p.timecheck(timestamp)

if __name__ == '__main__':
    main()
