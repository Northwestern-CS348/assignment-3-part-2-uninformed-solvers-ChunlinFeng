
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
        if self.gm.isWon() and self.currentState.state == self.victoryCondition:
            return True
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
                    self.currentState.nextChildToVisit += 1

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
                    self.currentState.nextChildToVisit += 1

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
        return True
