
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # initial children
        self.currentState.children = self.gm.getMovables()
        # judge initial condition
        if self.currentState.state == self.victoryCondition and self.gm.isWon(): return True;
        # start solver
        continue_flag = 1 # already find the next state falg = 0, else = 1
        while continue_flag == 1:
            if self.currentState.nextChildToVisit < len(self.currentState.children):
                # deeper available!
                ### trans to next state
                current_move = self.currentState.children[self.currentState.nextChildToVisit]
                self.currentState.nextChildToVisit += 1
                self.gm.makeMove(current_move)
                 # now the kb is already enter the next state

                 # create next state
                next_state = self.gm.getGameState()
                depth = self.currentState.depth + 1
                next_state = GameState(next_state, depth, current_move)

                ## judge whether visited
                if next_state not in self.visited:
                    '''
                    if over the length of currentState.children then break
                    currentState ready for updating
                    '''
                    #self.currentState.nextChildToVisit += 1

                    # fulfill the next_state
                    self.visited[next_state] = True; # add into the lib
                    next_state.parent = self.currentState
                    next_state.children = self.gm.getMovables()
                    # swap
                    self.currentState = next_state

                    # Win!
                    if self.gm.isWon() and self.currentState.state == self.victoryCondition:
                        return True
                    # stop find
                    continue_flag = 0

                else:
                    self.gm.reverseMove(current_move)

            # need to jump to parent states
            elif self.currentState.depth != 0:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

            else:
                return False



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here


        # judge initial condition ?Win??
        if self.currentState.state == self.victoryCondition and self.gm.isWon(): return True;
        # initial children
        self.currentState.children = self.gm.getMovables()

        '''if current state is initial state, then create a list for storage'''
        if self.currentState.depth == 0:
            self.visited["SerialExplore"] = []
            self.visited["SerialExplore"].append([self.currentState,self.gm.kb])
            self.visited["ExploreInd"] = 0
            self.visited["next_depth"] = []
        '''judge if the BFS is at the end'''
        if self.visited["ExploreInd"] >= len(self.visited["SerialExplore"]): return False;

        # start solver
        continue_flag = 1 # already find the next state falg = 0, else = 1
        while continue_flag == 1:
            '''
            load the current state
            if the current state is not the initial one, jump to its parent, 
            and check if we need to explore the next state
            '''

            ind = self.visited["ExploreInd"]
            currentState = self.visited["SerialExplore"][ind][0]
            kb = self.visited["SerialExplore"][ind][1]
            '''jump to the next unexplored state'''
            if currentState.nextChildToVisit >= len(currentState.children):
                self.visited["ExploreInd"] = ind + 1
                if self.visited["ExploreInd"] >= len(self.visited["SerialExplore"]): return False;
                ind = self.visited["ExploreInd"]
                currentState = self.visited["SerialExplore"][ind][0]

            '''update the currentState into Self'''
            import copy

            self.gm.kb = copy.deepcopy(self.visited["SerialExplore"][ind][1])
            self.currentState = currentState


            '''deeper!'''
            parent_depth = self.currentState.depth
            explore_depth = parent_depth + 1  # the depth we need to fully explored
            move = self.currentState.children[self.currentState.nextChildToVisit]  # this step move
            self.currentState.nextChildToVisit += 1  # tell parent find the next one
            # save this condition into the dict

            # make move
            self.gm.makeMove(move)
            next_state_depth = self.currentState.depth + 1
            next_state = self.gm.getGameState()
            next_state = GameState(next_state, next_state_depth, move)

            if next_state not in self.visited:
                # full fill the next_state
                self.visited[next_state] = True  # add to visited-dicitonary
                '''add the next state'''
                self.visited["SerialExplore"].append([next_state, self.gm.kb])

                next_state.parent = self.currentState
                next_state.children = self.gm.getMovables()
                # swap
                self.currentState = next_state

                # Win!
                if self.gm.isWon() and self.currentState.state == self.victoryCondition: return True;

                # stop find
                continue_flag = 0
            else:
                self.currentState = next_state


