from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here

        # get the number of Pegs
        askPegNumber = parse_input("fact: (is ?x peg)")
        numberOfPegs = len(self.kb.kb_ask(askPegNumber))

        # ask disk on a peg
        StateStatus = []
        for pegNumber in range(numberOfPegs):
            # construct the question
            questionOnPeg = "fact: (on ?x peg)"
            targetPeg_str = "peg" + str(pegNumber+1)
            questionOnPeg = questionOnPeg.replace("peg",targetPeg_str)

            askPegNumber = parse_input(questionOnPeg)
            DisksOnPeg = self.kb.kb_ask(askPegNumber)

            # get the disk correct serial number
            PegStatus = []
            if DisksOnPeg != False:
                for ind,item in enumerate(DisksOnPeg):
                    # example : item.constant = "disk5"
                    op = item.bindings[0].constant.element[4:]
                    PegStatus.append(int(op))

                PegStatus.sort()

            # tuple to converter
            StateStatus.append(tuple(PegStatus)) # !False,append as normal; or append []

        return tuple(StateStatus)
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        # judge if legal
        if GameMaster.isMovableLegal(self,movable_statement):
            ### ge-information
            movable_disk = movable_statement.terms[0]
            from_where = movable_statement.terms[1]
            to_where = movable_statement.terms[2]
            Game_status = self.getGameState()

            #### get the one under movable
            curr_peg = int(from_where.term.element[3:])
            curr_peg_state = Game_status[curr_peg-1] # initial peg num is 1

            if len(curr_peg_state) < 2: next_top = "base" + str(curr_peg);
            else: next_top = "disk" + str(curr_peg_state[1]);

            ### get the top on target_peg
            target_peg = int(to_where.term.element[3:])
            target_peg_state = Game_status[target_peg-1] # initial peg num is 1
            if len(target_peg_state) < 1: target_top = "base" + str(target_peg);
            else: target_top = "disk" + str(target_peg_state[0]);


            ## fact above
             # construct the question
            disk_str = str(movable_disk)
            questionAbove = "fact: (above disk ?x)".replace("disk",disk_str)

             # ask
            askPegNumber = parse_input(questionAbove)
            statement_matched = self.kb.kb_ask(askPegNumber)

             # retract Above fact
            for ind,item in statement_matched.list_of_bindings:
                fact = item[0]
                if fact in self.kb.facts:
                    self.kb.kb_retract(fact)

             # retract 2 original tops
            del_fact1 = parse_input("fact: (top " + str(movable_disk) + " " + str(from_where) + ")")
            del_fact2 = parse_input("fact: (top " + str(target_top) + " " + str(to_where) + ")")
            self.kb.kb_retract(del_fact1)
            self.kb.kb_retract(del_fact2)

             # add new Above
            general_fact = "fact: (above disk_x disk_y)"
            general_fact = general_fact.replace("disk_x", disk_str)
            general_fact = general_fact.replace("disk_y", target_top)
            new_fact = parse_input(general_fact)
            self.kb.kb_assert(new_fact)

            ## fact top
            general_fact = "fact: (top disk peg)"
            general_fact = general_fact.replace("disk",next_top)
            general_fact = general_fact.replace("peg", str(from_where))
            new_fact = parse_input(general_fact)
            self.kb.kb_assert(new_fact)

            general_fact = "fact: (top disk peg)"
            general_fact = general_fact.replace("disk",str(movable_disk))
            general_fact = general_fact.replace("peg", str(to_where))
            new_fact = parse_input(general_fact)
            self.kb.kb_assert(new_fact)

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
