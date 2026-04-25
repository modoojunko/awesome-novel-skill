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
    [ValidateSet("claude-code", "hermes")]
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
}

Write-Host "安装到: $DEST_DIR"

New-Item -ItemType Directory -Force -Path $DEST_DIR | Out-Null

Copy-Item "SKILL.md" "$DEST_DIR\"
Copy-Item -Recurse "scripts" "$DEST_DIR\"

Write-Host "安装完成!"
