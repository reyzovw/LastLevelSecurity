from features.utils.console import draw_string


def render_gui():
    draw_string("Main menu, select action: \n", message_type="information")
    draw_string("1: Encrypt a block of data")
    draw_string("2: Unmount encrypted data block")
    draw_string("3: Shutdown")
