"""This subpackage contains game states.

Game states are subclasses of the State class. They handle input, logic and
drawing, starting at their registration and ending at their (self-initiated)
unregistration, which causes the main program to either register the next
queued state or quit."""