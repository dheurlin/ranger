on run argv

    set command to item 1 of argv

    tell application "iTerm"
        tell its current window to set newtab to (create tab with default profile)

        set s to the current session of newtab
        tell s
            write text command
        end tell

        
    end tell

end run
