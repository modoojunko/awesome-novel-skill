# Novel Agent Skill 安装脚本 (PowerShell)

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
