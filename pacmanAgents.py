# pacmanAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
import sys

from pacman import Directions
from game import Agent
from heuristics import *
import random
import math

class RandomAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        actions = state.getLegalPacmanActions()
        # returns random action from all the valide actions
        return actions[random.randint(0,len(actions)-1)]

class RandomSequenceAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,10):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        possible = state.getAllPossibleActions();
        for i in range(0,len(self.actionList)):
            self.actionList[i] = possible[random.randint(0,len(possible)-1)];
        tempState = state;
        for i in range(0,len(self.actionList)):
            if tempState.isWin() + tempState.isLose() == 0:
                tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
            else:
                break;
        # returns random action from all the valide actions
        return self.actionList[0];

class GreedyAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # get all legal actions for pacman
        legal = state.getLegalPacmanActions()
        # get all the successor state for these actions
        successors = [(state.generatePacmanSuccessor(action), action) for action in legal]
        # evaluate the successor states using scoreEvaluation heuristic
        scored = [(scoreEvaluation(state), action) for state, action in successors]
        # get best choice
        bestScore = max(scored)[0]
        # get all actions that lead to the highest score
        bestActions = [pair[1] for pair in scored if pair[0] == bestScore]
        # return random action from the list of the best actions
        return random.choice(bestActions)

class HillClimberAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.actionList = [];
        for i in range(0,5):
            self.actionList.append(Directions.STOP);
        return;

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Hill Climber Algorithm instead of returning Directions.STOP
        possible = state.getAllPossibleActions();
        for i in range(0, len(self.actionList)):
            self.actionList[i] = possible[random.randint(0, len(possible) - 1)];

        currentScore = 0.0
        prevStateFirstAction = self.actionList[0]
        while True:
            tempState = state
            for i in range(0, len(self.actionList)):
                if tempState.isWin() + tempState.isLose() == 0:
                    self.actionList[i] = [self.actionList[i],possible[random.randint(0, len(possible) - 1)]][random.randint(0, 1)]
                    tempState = tempState.generatePacmanSuccessor(self.actionList[i]);
                    if tempState is None:
                        print "pacman successor generation limit reached"
                        return prevStateFirstAction
                else:
                    if tempState.isWin():
                        return self.actionList[0];
                    if tempState.isLose():
                        return prevStateFirstAction

            nextScore = scoreEvaluation(tempState)
            if nextScore <= currentScore :
                return prevStateFirstAction
            prevStateFirstAction = self.actionList[0]

        return Directions.STOP

class GeneticAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        self.population = [None]*8;
        self.possible = state.getAllPossibleActions();
        return;

    def initializePopulation(self,state):
        actionList = [None] * 5;
        count = 0
        while count < 8:
            tempState = state
            for i in range(0, len(actionList)):
                actionList[i] = self.possible[random.randint(0, len(self.possible) - 1)];
                tempState = tempState.generatePacmanSuccessor(actionList[i]);
                if tempState.isWin or tempState.isLose:
                    break
            self.population[count] = (actionList,scoreEvaluation(tempState))
            count = count + 1
        return

    def evaluateCandidates(self):
        self.population.sort(key=lambda x: x[1])
        return

    def selectParents(self):
        setOfRanks = [8,7,6,5,4,3,2,1]
        randomNumberGenerated = random.randint(1,36)
        firstParent = 0
        totalSum=0
        for i in range(0,len(setOfRanks)):
            totalSum = totalSum + setOfRanks[i]
            if randomNumberGenerated <= totalSum:
                firstParent = i
                #setOfRanks.pop(i)
                break

        randomNumberGenerated = random.randint(1, sum(setOfRanks)-setOfRanks[firstParent])

        secondParent = 0
        totalSum = 0
        for i in range(0, len(setOfRanks)):
            if i!=firstParent:
                totalSum = totalSum + setOfRanks[i]
                if randomNumberGenerated <= totalSum:
                    secondParent = i
                    setOfRanks.pop(i)
                    break

        return (firstParent,secondParent)

    def recombineParents(self,firstParent, secondParent):
        randomNumberGenerated = random.randint(1,100)
        if randomNumberGenerated <= 70 : # do crossover
            child1 = [None]*5
            child2 = [None]*5

            for i in range(0,len(child1)):
                randomNumberGenerated = random.randint(1, 100)

                if randomNumberGenerated <= 50:
                    child1[i] = self.population[firstParent][0][i]
                else:
                    child1[i] = self.population[secondParent][0][i]

            for i in range(0,len(child2)):
                randomNumberGenerated = random.randint(1, 100)

                if randomNumberGenerated <= 50:
                    child2[i] = self.population[firstParent][0][i]
                else:
                    child2[i] = self.population[secondParent][0][i]
        else:
            return (None,None)

        return (child1,child2)

    def mutate(self,child):
        randomNumberGenerated = random.randint(1, 100)

        if randomNumberGenerated <= 10:
            i = random.randint(0, len(child) - 1)
            child[i] = self.possible[random.randint(0, len(self.possible) - 1)]

        return child

    def addChildToPopulation(self,child,state):
        tempState = state

        for i in range(0, len(child)):
            tempState = tempState.generatePacmanSuccessor(child[i]);
            if tempState is None:
                return 'None'
            if tempState.isWin():
                return 'Win'
            if tempState.isLose():
                return 'Lose'
        self.population.append((child,scoreEvaluation(tempState)))

        return

    def survivorSelection(self):
        self.population = self.population[:8]
        return

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write Genetic Algorithm instead of returning Directions.STOP
        self.initializePopulation(state)
        self.evaluateCandidates()

        while 1:
            firstParent, secondParent = self.selectParents()
            child1, child2 = self.recombineParents(firstParent, secondParent)

            if child1 is not None and child2 is not None: # Recombination happened
                child1 = self.mutate(child1)
                child2 = self.mutate(child2)

                returnValue = self.addChildToPopulation(child1, state)
                if returnValue is 'None':
                    break
                if returnValue is 'Win':
                    break
                if returnValue is 'Lose':
                    break

                returnValue = self.addChildToPopulation(child2, state)
                if returnValue is 'None':
                    break
                if returnValue is 'Win':
                    break
                if returnValue is 'Lose':
                    break
                self.evaluateCandidates()
                self.survivorSelection()


        return self.population[0][0][0]

class MCTSAgent(Agent):
    # Initialization Function: Called one time when the game starts
    def registerInitialState(self, state):
        return;

    def expand(self,v):
        a = v.legalActionsToVisit.pop(random.randint(0,len(v.legalActionsToVisit)-1))
        successor = v.state.generatePacmanSuccessor(a)
        if successor is None:
            self.computationalBudgetLeft = False
            return None
        child = TreeNode(successor,v,a)
        v.childrenStates.append(child)
        if not v.legalActionsToVisit:
            v.isFullyExpanded = True
        return child

    def select(self,v,root,c):
        maxUCB = - sys.maxint-1

        for childState in v.childrenStates:
            ucb = normalizedScoreEvaluation(v.state,root.state)+(c * math.sqrt(2 * math.log1p(v.timesVisited) / childState.timesVisited))
            if  ucb > maxUCB :
                maxUCB = ucb
                maxState = childState
        return maxState

    def treePolicy(self,v):
        root = v
        while v.state is not None and not v.state.isWin() and not v.state.isLose():
            if not v.isFullyExpanded:
                return self.expand(v)
            else:
                v = self.select(v,root,1)
        return v

    def defaultPolicy(self,s):
        rollout = 0
        while s is not None and not s.isWin() and not s.isLose() and rollout < 5:
            action = random.choice(s.getLegalPacmanActions())
            successor = s.generatePacmanSuccessor(action)
            if successor is not None:
                s = successor
            else:
                self.computationalBudgetLeft = False
            rollout = rollout + 1
        return scoreEvaluation(s)

    def backup(self,v,reward):
        while v is not None:
            v.timesVisited = v.timesVisited + 1
            v.reward = v.reward + reward
            v = v.parent

    def actionToBestChild(self,v0):
        maxVisited = 0

        for child in v0.childrenStates:
            if child.timesVisited > maxVisited:
                maxVisited = child.timesVisited
                action = child.action
        return action

    # GetAction Function: Called with every frame
    def getAction(self, state):
        # TODO: write MCTS Algorithm instead of returning Directions.STOP
        v0 = TreeNode(state,None,None)
        self.computationalBudgetLeft = True

        while self.computationalBudgetLeft:
            vl = self.treePolicy(v0)
            if vl is not None:
                reward = self.defaultPolicy(vl.state)
                self.backup(vl,reward)
        return self.actionToBestChild(v0)

class TreeNode:
    def __init__(self,state,parent,action):
        self.state = state
        self.legalActionsToVisit = state.getLegalPacmanActions()
        self.childrenStates = []
        self.parent = parent
        self.timesVisited = 0
        self.reward = 0.0
        self.isFullyExpanded = False
        self.action = action