# awesome-novel-skill - AI-assisted novel writing workflow system
# Copyright (C) 2026  modoojunko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("claude-code", "hermes", "openclaw")]
    [string]$Platform
)

$HOME_DIR = $env:USERPROFILE

switch ($Platform) {
    "claude-code" {
        $DEST_DIR = "$HOME_DIR\.claude\skills\awesome-novel"
    }
    "hermes" {
        $DEST_DIR = "$HOME_DIR\.hermes\skills\awesome-novel"
    }
    "openclaw" {
        $DEST_DIR = "$HOME_DIR\.openclaw\skills\awesome-novel"
    }
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "安装到: $DEST_DIR"

# 全量覆盖
Remove-Item -Recurse -Force $DEST_DIR -ErrorAction SilentlyContinue
Copy-Item -Recurse "$SCRIPT_DIR" "$DEST_DIR"

# 清理不需要的文件
Remove-Item -Recurse -Force "$DEST_DIR\.git" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$DEST_DIR\.claude" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$DEST_DIR\docs" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$DEST_DIR\example" -ErrorAction SilentlyContinue

Write-Host "安装完成!"
