[CmdletBinding()]
param(
    [string]$ProjectDir,
    [string]$RepoUrl = "https://github.com/coldwateryi/trellis-skills",
    [string]$Branch = "main",
    [string]$AgentTargets = $env:TRELLIS_SKILLS_AGENT_TARGETS
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Resolve-ExistingDirectory {
    param([Parameter(Mandatory = $true)][string]$Path)

    $item = Get-Item -LiteralPath $Path -ErrorAction SilentlyContinue
    if ($null -eq $item -or -not $item.PSIsContainer) {
        return $null
    }

    return $item.FullName
}

function Test-TrellisProject {
    param([Parameter(Mandatory = $true)][string]$Path)

    return Test-Path -LiteralPath (Join-Path $Path ".trellis") -PathType Container
}

function Get-CodexGlobalSkillsRoot {
    if (-not [string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
        return Join-Path $env:CODEX_HOME "skills"
    }

    if ([string]::IsNullOrWhiteSpace($HOME)) {
        throw "无法确定全局 Codex skill 目录：请设置 CODEX_HOME 或 HOME。"
    }

    return Join-Path (Join-Path $HOME ".codex") "skills"
}

function Get-ClaudeGlobalSkillsRoot {
    if ([string]::IsNullOrWhiteSpace($HOME)) {
        throw "无法确定全局 Claude Code skill 目录：请设置 HOME。"
    }

    return Join-Path (Join-Path $HOME ".claude") "skills"
}

function Resolve-AgentTargets {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return "both"
    }

    switch ($Value.Trim().ToLowerInvariant()) {
        "both" { return "both" }
        "all" { return "both" }
        "codex" { return "codex" }
        "agents" { return "codex" }
        "claude" { return "claude" }
        "claude-code" { return "claude" }
        "claude_code" { return "claude" }
        default {
            throw "未知 Agent 安装目标: $Value。请使用 -AgentTargets both|codex|claude，或设置 TRELLIS_SKILLS_AGENT_TARGETS=both|codex|claude。"
        }
    }
}

function Test-TrellisSkillsSource {
    param([Parameter(Mandatory = $true)][string]$Path)

    $requiredDirs = @(
        "scripts",
        "trellis-zero-to-mvp",
        "trellis-zero-to-mvp-zh",
        "trellis-mvp-to-delivery",
        "trellis-mvp-to-delivery-zh"
    )

    foreach ($dir in $requiredDirs) {
        if (-not (Test-Path -LiteralPath (Join-Path $Path $dir) -PathType Container)) {
            return $false
        }
    }

    return $true
}

function Get-LocalTrellisSkillsSource {
    $currentDir = (Get-Location).Path
    if ((Split-Path -Leaf $currentDir) -eq "scripts") {
        $parentDir = Resolve-ExistingDirectory -Path (Join-Path $currentDir "..")
        if ($null -ne $parentDir -and (Test-TrellisSkillsSource -Path $parentDir)) {
            return $parentDir
        }
    }

    $scriptPath = $PSCommandPath
    if ([string]::IsNullOrWhiteSpace($scriptPath)) {
        $scriptPath = $MyInvocation.MyCommand.Path
    }

    if (-not [string]::IsNullOrWhiteSpace($scriptPath)) {
        $scriptDir = Resolve-ExistingDirectory -Path (Split-Path -Parent $scriptPath)
        if ($null -ne $scriptDir -and (Split-Path -Leaf $scriptDir) -eq "scripts") {
            $parentDir = Resolve-ExistingDirectory -Path (Join-Path $scriptDir "..")
            if ($null -ne $parentDir -and (Test-TrellisSkillsSource -Path $parentDir)) {
                return $parentDir
            }
        }
    }

    return $null
}

function Invoke-Git {
    param(
        [Parameter(Mandatory = $true)][string]$RepoRoot,
        [Parameter(Mandatory = $true)][string[]]$Arguments
    )

    & git -C $RepoRoot @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git $($Arguments -join ' ') 执行失败。"
    }
}

function Update-LocalTrellisSkillsSource {
    param([Parameter(Mandatory = $true)][string]$SourceDir)

    if (-not (Test-Path -LiteralPath (Join-Path $SourceDir ".git") -PathType Container)) {
        Write-Host "当前 trellis-skills 目录不是 git checkout，跳过本地源码更新。"
        return
    }

    if ($null -eq (Get-Command git -ErrorAction SilentlyContinue)) {
        throw "需要 git 更新当前 trellis-skills 目录。"
    }

    Write-Host "检测到本地 trellis-skills 源码目录: $SourceDir"
    Write-Host "从 $RepoUrl 更新 $Branch 分支到当前 trellis-skills 目录..."

    Invoke-Git -RepoRoot $SourceDir -Arguments @("fetch", $RepoUrl, $Branch)

    $currentBranch = (& git -C $SourceDir rev-parse --abbrev-ref HEAD).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "无法读取当前 git 分支。"
    }

    if ($currentBranch -ne $Branch) {
        Invoke-Git -RepoRoot $SourceDir -Arguments @("checkout", $Branch)
    }

    Invoke-Git -RepoRoot $SourceDir -Arguments @("merge", "--ff-only", "FETCH_HEAD")
    Write-Host "本地 trellis-skills 源码已更新。"
}

function Read-GlobalInstallChoice {
    param([Parameter(Mandatory = $true)][string]$CheckedDir)

    while ($true) {
        $answer = Read-Host "目录 $CheckedDir 不是 Trellis 项目。是否改为安装到全局 skill 目录? [y/N]"

        switch -Regex ($answer) {
            '^(Y|y|Yes|yes|YES|是)$' { return $true }
            '^\s*$' { return $false }
            '^(N|n|No|no|NO|否)$' { return $false }
            default { Write-Host "请输入 y/yes/是 或 n/no/否。" }
        }
    }
}

function Read-TrellisProjectDirectory {
    while ($true) {
        $inputDir = Read-Host "请输入已完成 Trellis 初始化的项目目录"

        if ([string]::IsNullOrWhiteSpace($inputDir)) {
            Write-Host "目录不能为空。"
            continue
        }

        $resolvedDir = Resolve-ExistingDirectory -Path $inputDir
        if ($null -eq $resolvedDir) {
            Write-Host "目录不存在: $inputDir"
            continue
        }

        if (Test-TrellisProject -Path $resolvedDir) {
            return [PSCustomObject]@{
                Scope = "project"
                TargetDir = $resolvedDir
            }
        }

        Write-Host "该目录未发现 .trellis/: $resolvedDir"
        if (Read-GlobalInstallChoice -CheckedDir $resolvedDir) {
            return [PSCustomObject]@{
                Scope = "global"
                TargetDir = $null
            }
        }

        Write-Host "请先运行 trellis init，或输入其他已初始化 Trellis 的项目目录。"
    }
}

function Read-SkillLanguage {
    param([Parameter(Mandatory = $true)][string]$TargetLabel)

    while ($true) {
        $answer = Read-Host "是否安装中文版 skill 到 $TargetLabel ? [Y/n]"

        switch -Regex ($answer) {
            '^\s*$' { return "zh" }
            '^(Y|y|Yes|yes|YES|是)$' { return "zh" }
            '^(N|n|No|no|NO|否)$' { return "en" }
            default { Write-Host "请输入 y/yes/是 或 n/no/否。" }
        }
    }
}

function Install-TrellisSkills {
    param(
        [Parameter(Mandatory = $true)][ValidateSet("project", "global")][string]$InstallScope,
        [string]$TargetDir,
        [Parameter(Mandatory = $true)][ValidateSet("zh", "en")][string]$Language,
        [string]$SourceDir,
        [Parameter(Mandatory = $true)][ValidateSet("both", "codex", "claude")][string]$AgentTargets
    )

    if ($Language -eq "zh") {
        $skills = @(
            "trellis-zero-to-mvp-zh",
            "trellis-mvp-to-delivery-zh",
            "trellis-implement-tdd-zh",
            "trellis-debug-systematic-zh",
            "trellis-review-twostage-zh"
        )
    }
    else {
        $skills = @(
            "trellis-zero-to-mvp",
            "trellis-mvp-to-delivery",
            "trellis-implement-tdd",
            "trellis-debug-systematic",
            "trellis-review-twostage"
        )
    }

    $installRoots = @()
    if ($InstallScope -eq "project") {
        if ([string]::IsNullOrWhiteSpace($TargetDir)) {
            throw "项目级安装需要 TargetDir。"
        }

        if ($AgentTargets -eq "both" -or $AgentTargets -eq "codex") {
            $installRoots += (Join-Path $TargetDir ".agents\skills")
        }
        if ($AgentTargets -eq "both" -or $AgentTargets -eq "claude") {
            $installRoots += (Join-Path $TargetDir ".claude\skills")
        }
    }
    else {
        if ($AgentTargets -eq "both" -or $AgentTargets -eq "codex") {
            $installRoots += (Get-CodexGlobalSkillsRoot)
        }
        if ($AgentTargets -eq "both" -or $AgentTargets -eq "claude") {
            $installRoots += (Get-ClaudeGlobalSkillsRoot)
        }
    }

    $tempRoot = $null

    try {
        if (-not [string]::IsNullOrWhiteSpace($SourceDir)) {
            $resolvedSourceDir = Resolve-ExistingDirectory -Path $SourceDir
            if ($null -eq $resolvedSourceDir) {
                throw "本地 trellis-skills 源目录不存在: $SourceDir"
            }
            Write-Host "使用已更新的本地 trellis-skills 源码安装 skill。"
        }
        else {
            $tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("trellis-skills-" + [System.Guid]::NewGuid().ToString("N"))
            New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null

            $archiveUrl = "$RepoUrl/archive/refs/heads/$Branch.zip"
            $archivePath = Join-Path $tempRoot "trellis-skills.zip"

            Write-Host "从 $RepoUrl 下载 $Branch 分支..."
            Invoke-WebRequest -Uri $archiveUrl -OutFile $archivePath

            Expand-Archive -Path $archivePath -DestinationPath $tempRoot -Force
            $sourceDir = Get-ChildItem -Path $tempRoot -Directory |
                Where-Object { $_.Name -like "trellis-skills-*" } |
                Select-Object -First 1

            if ($null -eq $sourceDir) {
                throw "解压后未找到 trellis-skills 源目录。"
            }

            $resolvedSourceDir = $sourceDir.FullName
        }

        foreach ($installRoot in $installRoots) {
            New-Item -ItemType Directory -Path $installRoot -Force | Out-Null
            Write-Host "准备安装 skills 到: $installRoot"

            foreach ($skill in $skills) {
                $sourceSkill = Join-Path $resolvedSourceDir $skill
                $targetSkill = Join-Path $installRoot $skill

                if (-not (Test-Path -LiteralPath $sourceSkill -PathType Container)) {
                    throw "GitHub 源目录缺少 skill: $skill"
                }

                if (Test-Path -LiteralPath $targetSkill) {
                    Remove-Item -LiteralPath $targetSkill -Recurse -Force
                }

                Copy-Item -LiteralPath $sourceSkill -Destination $installRoot -Recurse
                Write-Host "已安装: $targetSkill"
            }

            Write-Host "完成。安装目录: $installRoot"
        }

        Write-Host "完成。安装目标: $AgentTargets"
    }
    finally {
        if (-not [string]::IsNullOrWhiteSpace($tempRoot) -and (Test-Path -LiteralPath $tempRoot)) {
            Remove-Item -LiteralPath $tempRoot -Recurse -Force
        }
    }
}

$resolvedAgentTargets = Resolve-AgentTargets -Value $AgentTargets
Write-Host "安装目标: $resolvedAgentTargets"

$localSourceDir = Get-LocalTrellisSkillsSource
if ($null -ne $localSourceDir) {
    Update-LocalTrellisSkillsSource -SourceDir $localSourceDir
}

$projectDirProvided = -not [string]::IsNullOrWhiteSpace($ProjectDir)
if (-not $projectDirProvided) {
    $candidateDir = (Get-Location).Path
}
else {
    $candidateDir = Resolve-ExistingDirectory -Path $ProjectDir
    if ($null -eq $candidateDir) {
        throw "项目目录不存在: $ProjectDir"
    }
}

if (Test-TrellisProject -Path $candidateDir) {
    $installScope = "project"
    $targetDir = $candidateDir
}
else {
    if ($projectDirProvided) {
        Write-Host "指定项目目录未发现 .trellis/，不是已初始化的 Trellis 项目: $candidateDir"
        if (Read-GlobalInstallChoice -CheckedDir $candidateDir) {
            $installTarget = [PSCustomObject]@{
                Scope = "global"
                TargetDir = $null
            }
        }
        else {
            $installTarget = Read-TrellisProjectDirectory
        }
    }
    else {
        Write-Host "当前目录未发现 .trellis/，不是已初始化的 Trellis 项目。"
        $installTarget = Read-TrellisProjectDirectory
    }

    $installScope = $installTarget.Scope
    $targetDir = $installTarget.TargetDir
}

if ($installScope -eq "global") {
    $targetLabel = "全局 skill 目录"
}
else {
    $targetLabel = $targetDir
}

$language = Read-SkillLanguage -TargetLabel $targetLabel
Install-TrellisSkills -InstallScope $installScope -TargetDir $targetDir -Language $language -SourceDir $localSourceDir -AgentTargets $resolvedAgentTargets
