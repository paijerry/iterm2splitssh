#!/usr/bin/env python3

import iterm2
import math

iplist = ["ip1", "ip2", "ip3", "ip4"]

async def main(connection):
    app = await iterm2.async_get_app(connection)
    window = app.current_window
    if window is None:
        print("No current iterm2 window.")
        return

    # 算出行數
    col = math.ceil(math.sqrt(len(iplist)))
    target = window.current_tab.current_session
    panes = []
    i = 0
    while i < len(iplist):

        if i > 0:
            if i/col < 1:
                # 第一行水平開
                target = await target.async_split_pane(vertical=True)
            else:
                # 其他行垂直開
                target = await panes[i-col].async_split_pane(vertical=False) 
        
        panes.append(target)
        await window.current_tab.async_set_title(iplist[i])
        await target.async_send_text("ssh jump\n")
        await target.async_send_text("ssh " + iplist[i] + "\n")
        i += 1

iterm2.run_until_complete(main)
