SBtk.py is the main program

it should only deal with 3 things:

1 - Digesting system arguments (passed from the console)
2 - Instantiating the manager
3 - Passing the proper interface class to the manager

Period.

(notice however that main() function does ask for the main loop. This is just to keep it running, and should make even more sense if the interface is multi-threaded)

For everything else, I (Leira) am trying to follow an MVP guideline (however clumsily), so, there are only 3 directories that contain code (src, manager, user_interfaces)