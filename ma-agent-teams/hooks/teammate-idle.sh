#!/bin/bash
# TeammateIdle hook for meta-pipe agent teams
#
# Runs when a teammate is about to go idle.
# Exit 2 = send feedback and keep the teammate working
# Exit 0 = allow the teammate to go idle
#
# This hook reminds teammates to check the shared task list
# for unclaimed tasks before going idle.

set -euo pipefail

# Check if the teammate has explicitly finished all assigned work
# by looking for a completion marker in the task description
if [[ "${CLAUDE_TASK_STATUS:-}" == "all_complete" ]]; then
    exit 0
fi

# Send feedback to keep working
echo "Before going idle, please check the shared task list for any remaining tasks assigned to you or unclaimed tasks you can pick up. If all your tasks are truly complete, message the lead to confirm completion."
exit 2
