def clear_terminal(console):
    if console is not None and hasattr(console, "file"):
        console.file.write("\033[2J\033[3J\033[H")
        console.file.flush()
    else:
        console.clear(home=True)
