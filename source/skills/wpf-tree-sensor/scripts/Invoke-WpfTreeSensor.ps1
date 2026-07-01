param(
    [string]$ProcessName,
    [int]$ProcessId = 0,
    [string]$WindowTitleContains,
    [string]$AutomationIdContains,
    [string]$NameContains,
    [int]$MaxDepth = 6,
    [switch]$IncludeBoundingRectangles,
    [switch]$IncludePatterns,
    [ValidateSet("json")]
    [string]$Format = "json",
    [string]$OutputPath,
    [int]$TimeoutSeconds = 5,
    [switch]$ProjectAuto,
    [switch]$ListWindows,
    [switch]$Summarize
)

$ErrorActionPreference = "Stop"

# Helper: Find file or folder upwards from a path
function Find-Upwards {
    param(
        [string]$FileName,
        [string]$StartPath
    )
    $dir = $StartPath
    while ($null -ne $dir) {
        $candidate = Join-Path $dir $FileName
        if (Test-Path $candidate) {
            return $candidate
        }
        $parent = Split-Path -Parent $dir
        if ($parent -eq $dir -or [string]::IsNullOrWhiteSpace($parent)) {
            break
        }
        $dir = $parent
    }
    return $null
}

# Helper: Find the root folder of the project/solution
function Find-ProjectRoot {
    param([string]$StartPath)
    $dir = $StartPath
    while ($null -ne $dir) {
        if ((Get-ChildItem -Path $dir -Filter "*.sln" -ErrorAction SilentlyContinue) -or 
            (Get-ChildItem -Path $dir -Filter "*.csproj" -ErrorAction SilentlyContinue) -or 
            (Test-Path (Join-Path $dir ".git") -PathType Container)) {
            return $dir
        }
        $parent = Split-Path -Parent $dir
        if ($parent -eq $dir -or [string]::IsNullOrWhiteSpace($parent)) {
            break
        }
        $dir = $parent
    }
    return $StartPath
}

# Config & Inference lists
$AllowedProcessNames = [System.Collections.Generic.List[string]]::new()
$AllowedWindowTitles = [System.Collections.Generic.List[string]]::new()
$PreferredWindowTitles = ""
$IgnoredWindowTitles = [System.Collections.Generic.List[string]]::new()
$ConfigDefaultMaxDepth = $null

# Strategy metadata
$StrategyUsed = "Explicit"
$MatchedBy = [System.Collections.Generic.List[string]]::new()

# Load parameters if provided
if (-not [string]::IsNullOrWhiteSpace($ProcessName)) {
    $AllowedProcessNames.Add($ProcessName)
    $MatchedBy.Add("processName")
}
if (-not [string]::IsNullOrWhiteSpace($WindowTitleContains)) {
    $AllowedWindowTitles.Add($WindowTitleContains)
    $MatchedBy.Add("windowTitle")
}

# Load project auto-detect if flag is set
if ($ProjectAuto) {
    $StrategyUsed = "ProjectAuto"
    $cwd = Get-Location
    
    # 1. Look for .wpf-tree-sensor.json
    $configJsonPath = Find-Upwards -FileName ".wpf-tree-sensor.json" -StartPath $cwd
    if ($null -ne $configJsonPath) {
        try {
            $config = Get-Content -Raw -Path $configJsonPath | ConvertFrom-Json
            if ($null -ne $config) {
                if ($null -ne $config.appNames) {
                    foreach ($app in $config.appNames) {
                        $AllowedProcessNames.Add($app)
                        if (-not $MatchedBy.Contains("processName")) { $MatchedBy.Add("processName") }
                    }
                }
                if ($null -ne $config.windowTitleContains) {
                    foreach ($title in $config.windowTitleContains) {
                        $AllowedWindowTitles.Add($title)
                        if (-not $MatchedBy.Contains("windowTitle")) { $MatchedBy.Add("windowTitle") }
                    }
                }
                if ($null -ne $config.preferredWindowTitleContains) {
                    $PreferredWindowTitles = $config.preferredWindowTitleContains
                }
                if ($null -ne $config.ignoreWindowTitleContains) {
                    foreach ($ignore in $config.ignoreWindowTitleContains) {
                        $IgnoredWindowTitles.Add($ignore)
                    }
                }
                if ($null -ne $config.defaultMaxDepth) {
                    $ConfigDefaultMaxDepth = [int]$config.defaultMaxDepth
                }
            }
        } catch {
            # Fail silently
        }
    }
    
    # 2. If nothing configured or files need scanning, find csproj/sln
    if ($AllowedProcessNames.Count -eq 0 -and $AllowedWindowTitles.Count -eq 0) {
        $projectRoot = Find-ProjectRoot -StartPath $cwd
        $csprojFiles = Get-ChildItem -Path $projectRoot -Filter "*.csproj" -Recurse -ErrorAction SilentlyContinue
        
        foreach ($file in $csprojFiles) {
            try {
                $content = Get-Content -Raw -Path $file.FullName -ErrorAction SilentlyContinue
                if ($null -eq $content) { continue }
                if ($content -match "<UseWPF>\s*[Tt]rue\s*</UseWPF>" -or $content -match "Microsoft\.NET\.Sdk\.WindowsDesktop") {
                    $assemblyName = $null
                    if ($content -match "<AssemblyName>\s*(.*?)\s*</AssemblyName>") {
                        $assemblyName = $Matches[1]
                    } else {
                        $assemblyName = $file.BaseName
                    }
                    if (-not [string]::IsNullOrWhiteSpace($assemblyName)) {
                        $AllowedProcessNames.Add($assemblyName)
                        if (-not $MatchedBy.Contains("processName")) { $MatchedBy.Add("processName") }
                        
                        # Infer window titles from assembly name: e.g. QuotaTank.WPF -> QuotaTank, Quota-Tank
                        $baseName = $assemblyName -replace "\.WPF$", "" -replace "\.App$", ""
                        $AllowedWindowTitles.Add($baseName)
                        if (-not $MatchedBy.Contains("windowTitle")) { $MatchedBy.Add("windowTitle") }
                        
                        # Add camelCase split
                        $splitName = $baseName -replace '([a-z])([A-Z])', '$1 $2'
                        if ($splitName -ne $baseName) {
                            $AllowedWindowTitles.Add($splitName)
                        }
                        # Add hyphenated split
                        $dashName = $baseName -replace '([a-z])([A-Z])', '$1-$2'
                        if ($dashName -ne $baseName) {
                            $AllowedWindowTitles.Add($dashName)
                        }
                    }
                }
            } catch {}
        }
    }
}

# Determine effective MaxDepth
$EffectiveMaxDepth = $MaxDepth
if ($null -ne $ConfigDefaultMaxDepth -and -not $PSBoundParameters.ContainsKey('MaxDepth')) {
    $EffectiveMaxDepth = $ConfigDefaultMaxDepth
}

# NOTE: Redaction is intentionally deferred. The sensor does not currently read
# ValuePattern values, so there are no sensitive user inputs to redact. If value
# reading is added later, implement redaction at the ValuePattern read site.

function New-TargetSpec {
    [ordered]@{
        strategy = $StrategyUsed
        processId = if ($ProcessId -gt 0) { $ProcessId } else { $null }
        processNames = if ($AllowedProcessNames.Count -gt 0) { @($AllowedProcessNames) } else { $null }
        windowTitles = if ($AllowedWindowTitles.Count -gt 0) { @($AllowedWindowTitles) } else { $null }
        automationIdContains = if ([string]::IsNullOrWhiteSpace($AutomationIdContains)) { $null } else { $AutomationIdContains }
        nameContains = if ([string]::IsNullOrWhiteSpace($NameContains)) { $null } else { $NameContains }
    }
}

function Write-SensorJson($Payload, $ExitCode) {
    $json = $Payload | ConvertTo-Json -Depth 100
    if (-not [string]::IsNullOrWhiteSpace($OutputPath)) {
        $parent = Split-Path -Parent $OutputPath
        if (-not [string]::IsNullOrWhiteSpace($parent)) {
            New-Item -ItemType Directory -Force -Path $parent | Out-Null
        }
        Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8
    }
    else {
        Write-Output $json
    }
    exit $ExitCode
}

function New-Failure($Code, $Message, $Candidates = @()) {
    $err = [ordered]@{
        code = $Code
        message = $Message
    }
    $fail = [ordered]@{
        sensor = "WpfTreeSensor"
        schemaVersion = "0.1"
        capturedAtLocal = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
        target = New-TargetSpec
        status = "failed"
        error = $err
    }
    if ($Candidates.Count -gt 0) {
        $fail["candidates"] = @($Candidates)
    }
    return [pscustomobject]$fail
}

function Test-Contains($Value, $Needle) {
    if ([string]::IsNullOrWhiteSpace($Needle)) {
        return $true
    }
    if ($null -eq $Value) {
        return $false
    }
    return ([string]$Value).IndexOf($Needle, [System.StringComparison]::OrdinalIgnoreCase) -ge 0
}

function Get-CurrentOrNull($Element) {
    try {
        return $Element.Current
    }
    catch {
        return $null
    }
}

# Top-level window retrieval and filtering
$processCache = @{}
function Get-CachedProcessName($id) {
    if (-not $processCache.ContainsKey($id)) {
        $p = Get-Process -Id $id -ErrorAction SilentlyContinue
        $processCache[$id] = if ($null -ne $p) { $p.ProcessName } else { "" }
    }
    return $processCache[$id]
}

function Find-SubtreeRoot($Window, $Warnings) {
    if ([string]::IsNullOrWhiteSpace($AutomationIdContains) -and [string]::IsNullOrWhiteSpace($NameContains)) {
        return $Window
    }

    $matches = @()
    $nodes = $Window.FindAll([System.Windows.Automation.TreeScope]::Descendants, [System.Windows.Automation.Condition]::TrueCondition)
    foreach ($node in $nodes) {
        $current = Get-CurrentOrNull $node
        if ($null -eq $current) {
            continue
        }
        if (-not (Test-Contains $current.AutomationId $AutomationIdContains)) {
            continue
        }
        if (-not (Test-Contains $current.Name $NameContains)) {
            continue
        }
        $matches += $node
    }

    if ($matches.Count -eq 1) {
        return $matches[0]
    }
    if ($matches.Count -gt 1) {
        throw "Subtree selector matched $($matches.Count) controls. Narrow -AutomationIdContains or -NameContains."
    }

    throw "No subtree control matched the supplied selector."
}

function Get-BoundingRectangle($Current) {
    $rect = $Current.BoundingRectangle
    if ($rect.IsEmpty) {
        return $null
    }
    return [ordered]@{
        x = [math]::Round($rect.X, 2)
        y = [math]::Round($rect.Y, 2)
        width = [math]::Round($rect.Width, 2)
        height = [math]::Round($rect.Height, 2)
    }
}

function Get-SupportedPatterns($Element) {
    $patterns = @(
        @{ name = "InvokePattern"; pattern = [System.Windows.Automation.InvokePattern]::Pattern },
        @{ name = "ValuePattern"; pattern = [System.Windows.Automation.ValuePattern]::Pattern },
        @{ name = "SelectionPattern"; pattern = [System.Windows.Automation.SelectionPattern]::Pattern },
        @{ name = "SelectionItemPattern"; pattern = [System.Windows.Automation.SelectionItemPattern]::Pattern },
        @{ name = "TogglePattern"; pattern = [System.Windows.Automation.TogglePattern]::Pattern },
        @{ name = "ExpandCollapsePattern"; pattern = [System.Windows.Automation.ExpandCollapsePattern]::Pattern },
        @{ name = "ScrollPattern"; pattern = [System.Windows.Automation.ScrollPattern]::Pattern },
        @{ name = "ScrollItemPattern"; pattern = [System.Windows.Automation.ScrollItemPattern]::Pattern },
        @{ name = "RangeValuePattern"; pattern = [System.Windows.Automation.RangeValuePattern]::Pattern },
        @{ name = "WindowPattern"; pattern = [System.Windows.Automation.WindowPattern]::Pattern }
    )

    $supported = @()
    foreach ($entry in $patterns) {
        try {
            $null = $Element.GetCurrentPattern($entry.pattern)
            $supported += $entry.name
        }
        catch {
        }
    }
    return $supported
}

function Convert-ElementToNode($Element, $Depth, $MaxDepth, $Warnings) {
    $current = Get-CurrentOrNull $Element
    if ($null -eq $current) {
        $Warnings.Add("Skipped a stale or inaccessible UI Automation element.")
        return $null
    }

    $controlType = $null
    if ($null -ne $current.ControlType) {
        $controlType = $current.ControlType.ProgrammaticName -replace "^ControlType\.", ""
    }

    $node = [ordered]@{
        name = $current.Name
        automationId = $current.AutomationId
        controlType = $controlType
        className = $current.ClassName
        isEnabled = $current.IsEnabled
        isOffscreen = $current.IsOffscreen
        isSelected = $false
        toggleState = $null
        children = @()
    }

    # Query SelectionItemPattern
    try {
        $selPattern = $Element.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)
        $node["isSelected"] = $selPattern.Current.IsSelected
    } catch {}

    # Query TogglePattern
    try {
        $togPattern = $Element.GetCurrentPattern([System.Windows.Automation.TogglePattern]::Pattern)
        $node["toggleState"] = $togPattern.Current.ToggleState.ToString()
    } catch {}

    if ($IncludeBoundingRectangles -or $Summarize) {
        $node["boundingRectangle"] = Get-BoundingRectangle $current
    }
    if ($IncludePatterns -or $Summarize) {
        $node["patterns"] = @(Get-SupportedPatterns $Element)
    }

    if ($Depth -lt $MaxDepth) {
        $children = @()
        $child = $script:ControlWalker.GetFirstChild($Element)
        while ($null -ne $child) {
            $childNode = Convert-ElementToNode $child ($Depth + 1) $MaxDepth $Warnings
            if ($null -ne $childNode) {
                $children += $childNode
            }
            $child = $script:ControlWalker.GetNextSibling($child)
        }
        $node["children"] = @($children)
    }

    return [pscustomobject]$node
}

# Helper to flatten the parsed tree for summary processing
function Get-FlatNodes($Node) {
    $list = New-Object System.Collections.Generic.List[PSCustomObject]
    $list.Add($Node)
    if ($null -ne $Node.children) {
        foreach ($child in $Node.children) {
            $childNodes = @(Get-FlatNodes $child)
            foreach ($cn in $childNodes) {
                $list.Add($cn)
            }
        }
    }
    return $list
}

# Heuristics view solver
function Resolve-ProbableView($FlatNodes, $TopWindowName) {
    $viewScores = @{}
    $viewEvidence = @{}
    
    function Add-Score($ViewName, $Score, $Evidence) {
        if ([string]::IsNullOrWhiteSpace($ViewName)) { return }
        $clean = $ViewName -replace "(View|Page|Dialog|Window|Content|Control|Panel)$", ""
        if ([string]::IsNullOrWhiteSpace($clean)) { return }
        $clean = (Get-Culture).TextInfo.ToTitleCase($clean.ToLower())
        
        if (-not $viewScores.ContainsKey($clean)) {
            $viewScores[$clean] = 0
            $viewEvidence[$clean] = New-Object System.Collections.Generic.List[string]
        }
        $viewScores[$clean] += $Score
        $viewEvidence[$clean].Add($Evidence)
    }

    # 1. Window title heuristics
    $titleWords = $TopWindowName -split '[\s\-\(\)\[\]]'
    foreach ($word in $titleWords) {
        if ($word -match "^[A-Z][a-zA-Z]{2,15}$" -and $word -notmatch "^(WPF|App|Application|Client|System|Window|Desktop|Main|Host)$") {
            Add-Score $word 3 "Window title contains '$word'"
        }
    }

    # Iterate through flat nodes
    foreach ($node in $FlatNodes) {
        $name = $node.name
        $autoId = $node.automationId
        $class = $node.className
        $type = $node.controlType
        
        # 2. Selected tab item or child element
        if ($node.isSelected) {
            Add-Score $name 5 "Selected tab item is '$name'"
        }
        
        # 3. Automation ID heuristics
        if (-not [string]::IsNullOrWhiteSpace($autoId)) {
            if ($autoId -match "([a-zA-Z0-9]+)(View|Page|Dialog|Content)$") {
                $candidate = $Matches[1]
                if ($candidate -notmatch "^(Main|Root|Host|Parent|Container|App)$") {
                    Add-Score $candidate 4 "Control with AutomationId '$autoId' is visible"
                }
            }
        }
        
        # 4. Dialog title / child window presence
        if ($type -eq "Window" -and $name -ne $TopWindowName -and -not $node.isOffscreen) {
            Add-Score $name 6 "Visible child window/dialog '$name' is active"
        }
        
        # 5. Prominent heading
        if ($type -eq "Text" -and -not $node.isOffscreen -and -not [string]::IsNullOrWhiteSpace($name)) {
            if ($autoId -match "Title|Header|Heading|Banner") {
                Add-Score $name 2 "Prominent heading text is '$name'"
            }
        }
    }
    
    # Find top score
    $topView = $null
    $maxScore = 0
    foreach ($key in $viewScores.Keys) {
        if ($viewScores[$key] -gt $maxScore) {
            $maxScore = $viewScores[$key]
            $topView = $key
        }
    }
    
    if ($null -ne $topView) {
        $confidence = "low"
        if ($maxScore -ge 8) { $confidence = "high" }
        elseif ($maxScore -ge 4) { $confidence = "medium" }
        
        return [ordered]@{
            name = $topView
            confidence = $confidence
            evidence = @($viewEvidence[$topView])
        }
    }
    
    return [ordered]@{
        name = "Unknown"
        confidence = "none"
        evidence = @("No view heuristics matched")
    }
}

function Get-RejectedCandidateList($CandidatesRejected) {
    $list = @()
    foreach ($r in $CandidatesRejected) {
        $list += [ordered]@{
            name = $r.name
            processName = $r.processName
            processId = $r.processId
        }
    }
    return $list
}

try {
    Add-Type -AssemblyName UIAutomationClient
    Add-Type -AssemblyName UIAutomationTypes

    $warnings = New-Object System.Collections.Generic.List[string]
    $desktop = [System.Windows.Automation.AutomationElement]::RootElement
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    
    $matches = @()
    $candidatesRejected = New-Object System.Collections.Generic.List[PSCustomObject]
    
    do {
        $windows = $desktop.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
        $matchedWindows = New-Object System.Collections.Generic.List[System.Windows.Automation.AutomationElement]
        
        foreach ($window in $windows) {
            $current = Get-CurrentOrNull $window
            if ($null -eq $current) { continue }
            
            $windowPid = $current.ProcessId
            $pName = Get-CachedProcessName $windowPid
            $title = $current.Name
            
            # Check filters
            $isMatch = $true
            if ($ProcessId -gt 0 -and $windowPid -ne $ProcessId) { $isMatch = $false }
            
            $processMatch = $false
            $titleMatch = $false
            
            if ($AllowedProcessNames.Count -gt 0) {
                foreach ($apName in $AllowedProcessNames) {
                    $cleanAp = if ($apName -like "*.exe") { $apName.Substring(0, $apName.Length - 4) } else { $apName }
                    if ($pName -ieq $cleanAp) { $processMatch = $true; break }
                }
            }
            
            if ($AllowedWindowTitles.Count -gt 0) {
                foreach ($awt in $AllowedWindowTitles) {
                    if (Test-Contains $title $awt) { $titleMatch = $true; break }
                }
            }
            
            # ProjectAuto uses OR: match if process name OR window title matches.
            # Explicit targeting uses AND: all specified filters must match.
            if ($AllowedProcessNames.Count -gt 0 -or $AllowedWindowTitles.Count -gt 0) {
                if ($ProjectAuto) {
                    if (-not $processMatch -and -not $titleMatch) { $isMatch = $false }
                } else {
                    if ($AllowedProcessNames.Count -gt 0 -and -not $processMatch) { $isMatch = $false }
                    if ($AllowedWindowTitles.Count -gt 0 -and -not $titleMatch) { $isMatch = $false }
                }
            }
            
            # Check ignored window titles
            if ($IgnoredWindowTitles.Count -gt 0) {
                $isIgnored = $false
                foreach ($iwt in $IgnoredWindowTitles) {
                    if (Test-Contains $title $iwt) {
                        $isIgnored = $true
                        $candidatesRejected.Add([pscustomobject]@{
                            name = $title
                            processName = $pName
                            processId = $windowPid
                            reason = "Ignored title pattern '$iwt'"
                        })
                        break
                    }
                }
                if ($isIgnored) { $isMatch = $false }
            }
            
            if ($isMatch) {
                $matchedWindows.Add($window)
            }
        }
        
        if ($matchedWindows.Count -gt 0) {
            $matches = @($matchedWindows)
            break
        }
        Start-Sleep -Milliseconds 250
    } while ((Get-Date) -lt $deadline)

    # ListWindows mode (Write-SensorJson calls exit, so subsequent code is not reached)
    if ($ListWindows) {
        $windowList = @()
        $targetWindows = if ($ProcessId -eq 0 -and $AllowedProcessNames.Count -eq 0 -and $AllowedWindowTitles.Count -eq 0) {
            # No filters: enumerate all desktop windows fresh (don't rely on loop variable)
            $desktop.FindAll([System.Windows.Automation.TreeScope]::Children, [System.Windows.Automation.Condition]::TrueCondition)
        } else {
            $matches
        }
        
        foreach ($w in $targetWindows) {
            $current = Get-CurrentOrNull $w
            if ($null -eq $current) { continue }
            $windowPid = $current.ProcessId
            $windowList += [pscustomobject][ordered]@{
                name = $current.Name
                processId = $windowPid
                processName = Get-CachedProcessName $windowPid
                className = $current.ClassName
                automationId = $current.AutomationId
                isOffscreen = $current.IsOffscreen
            }
        }
        
        $result = [pscustomobject][ordered]@{
            sensor = "WpfTreeSensor"
            schemaVersion = "0.1"
            capturedAtLocal = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
            status = "success"
            mode = "listWindows"
            windows = $windowList
        }
        Write-SensorJson $result 0
    }

    # Standard / Summary capture mode
    # Note: only reached when -ListWindows was not used, since Write-SensorJson calls exit
    if ($matches.Count -eq 0) {
        Write-SensorJson (New-Failure "TargetWindowNotFound" "No matching top-level window was found.") 1
    }

    # Resolve ambiguity with preferred window title
    if ($matches.Count -gt 1 -and -not [string]::IsNullOrWhiteSpace($PreferredWindowTitles)) {
        $preferredMatches = @()
        foreach ($match in $matches) {
            $current = Get-CurrentOrNull $match
            if ($null -ne $current -and (Test-Contains $current.Name $PreferredWindowTitles)) {
                $preferredMatches += $match
            }
        }
        if ($preferredMatches.Count -eq 1) {
            $matches = $preferredMatches
        }
    }

    if ($matches.Count -gt 1) {
        $candidates = @()
        foreach ($m in $matches) {
            $current = Get-CurrentOrNull $m
            if ($null -ne $current) {
                $candidates += [ordered]@{
                    name = $current.Name
                    processName = Get-CachedProcessName $current.ProcessId
                    processId = $current.ProcessId
                }
            }
        }
        Write-SensorJson (New-Failure "TargetWindowAmbiguous" "Matched multiple top-level windows." $candidates) 1
    }

    $window = $matches[0]
    $root = Find-SubtreeRoot $window $warnings
    $windowCurrent = Get-CurrentOrNull $window
    $windowProcessName = Get-CachedProcessName $windowCurrent.ProcessId
    
    # Walk tree
    $script:ControlWalker = [System.Windows.Automation.TreeWalker]::ControlViewWalker
    $tree = Convert-ElementToNode $root 0 $EffectiveMaxDepth $warnings
    
    if ($Summarize) {
        $flatNodes = Get-FlatNodes $tree
        
        $headings = [System.Collections.Generic.List[string]]::new()
        $visibleButtons = [System.Collections.Generic.List[string]]::new()
        $selectedStates = [System.Collections.Generic.List[PSCustomObject]]::new()
        $modalDialogPresent = $false
        
        foreach ($node in $flatNodes) {
            $name = $node.name
            $type = $node.controlType
            $autoId = $node.automationId
            $class = $node.className
            $isOff = $node.isOffscreen
            
            # Headings
            if ($type -eq "Text" -or $type -eq "Header" -or $type -eq "HeaderItem") {
                if (-not $isOff -and -not [string]::IsNullOrWhiteSpace($name)) {
                    if ($type -eq "Header" -or $type -eq "HeaderItem" -or $autoId -match "Title|Header|Heading|Banner" -or $class -like "*Title*") {
                        if ($name.Length -lt 80 -and -not $headings.Contains($name)) {
                            $headings.Add($name)
                        }
                    }
                }
            }
            
            # Visible buttons
            if ($type -eq "Button" -and -not $isOff -and -not [string]::IsNullOrWhiteSpace($name)) {
                if (-not $visibleButtons.Contains($name)) {
                    $visibleButtons.Add($name)
                }
            }
            
            # Selected states
            if ($node.isSelected) {
                $selectedStates.Add([pscustomobject][ordered]@{
                    name = $name
                    type = $type
                    state = "Selected"
                })
            }
            if ($null -ne $node.toggleState -and $node.toggleState -ne "Off") {
                $selectedStates.Add([pscustomobject][ordered]@{
                    name = $name
                    type = $type
                    state = $node.toggleState
                })
            }
            
            # Modal / Dialog presence
            if (($type -eq "Window" -or $type -eq "Dialog" -or $class -like "*Dialog*" -or $class -like "*Window*") -and $name -ne $windowCurrent.Name -and -not $isOff) {
                $modalDialogPresent = $true
            }
        }
        
        # Probable current view
        $currentView = Resolve-ProbableView $flatNodes $windowCurrent.Name
        
        $rejectedList = @(Get-RejectedCandidateList $candidatesRejected)
        
        $result = [pscustomobject][ordered]@{
            sensor = "WpfTreeSensor"
            schemaVersion = "0.1"
            capturedAtLocal = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
            status = "success"
            mode = "summary"
            selection = [ordered]@{
                strategy = $StrategyUsed
                matchedBy = @($MatchedBy)
                candidatesRejected = $rejectedList
            }
            topLevelWindow = [ordered]@{
                name = $windowCurrent.Name
                processId = $windowCurrent.ProcessId
                processName = $windowProcessName
            }
            currentView = $currentView
            headings = @($headings)
            visibleButtons = @($visibleButtons)
            selectedStates = @($selectedStates)
            modalDialogPresent = $modalDialogPresent
            warnings = @($warnings)
        }
        
        Write-SensorJson $result 0
    }
    else {
        # Full tree mode
        $rejectedList = @(Get-RejectedCandidateList $candidatesRejected)
        
        $result = [pscustomobject][ordered]@{
            sensor = "WpfTreeSensor"
            schemaVersion = "0.1"
            capturedAtLocal = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss zzz")
            target = [ordered]@{
                processId = $windowCurrent.ProcessId
                processName = $windowProcessName
                windowTitle = $windowCurrent.Name
            }
            selection = [ordered]@{
                strategy = $StrategyUsed
                matchedBy = @($MatchedBy)
                candidatesRejected = $rejectedList
            }
            status = "success"
            warnings = @($warnings)
            root = $tree
        }
        
        Write-SensorJson $result 0
    }
}
catch {
    $message = $_.Exception.Message
    if ($null -ne $_.InvocationInfo -and $_.InvocationInfo.ScriptLineNumber -gt 0) {
        $message = "$message (line $($_.InvocationInfo.ScriptLineNumber))"
    }
    Write-SensorJson (New-Failure "SensorError" $message) 1
}
